from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrEcPayrollPeriod(models.Model):
    _name = "hr.ec.payroll.period"
    _description = "Período de nómina (cliente)"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_start desc, id desc"

    name = fields.Char(required=True, copy=False, readonly=True, default=lambda self: _("Nuevo"))
    partner_id = fields.Many2one(
        "res.partner",
        string="Cliente",
        required=True,
        domain="[('is_company', '=', True)]",
        tracking=True,
    )
    service_contract_id = fields.Many2one(
        "hr.service.contract",
        string="Contrato de nómina",
        domain="[('partner_id', '=', partner_id), ('service_kind', '=', 'payroll'), ('state', '=', 'active')]",
        tracking=True,
    )
    date_start = fields.Date(string="Desde", required=True, tracking=True)
    date_end = fields.Date(string="Hasta", required=True, tracking=True)
    state = fields.Selection(
        selection=[
            ("pending", "Pendiente"),
            ("collecting", "En recopilación"),
            ("processing", "En proceso"),
            ("review", "En revisión"),
            ("approved", "Aprobada"),
            ("delivered", "Entregada"),
            ("closed", "Cerrada"),
        ],
        default="pending",
        required=True,
        tracking=True,
    )
    user_id = fields.Many2one(
        "res.users",
        string="Responsable",
        default=lambda self: self.env.user,
        tracking=True,
    )
    project_id = fields.Many2one("project.project", string="Proyecto checklist", copy=False)
    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.company,
    )
    input_ids = fields.One2many("hr.ec.payroll.input", "period_id", string="Novedades")
    input_count = fields.Integer(compute="_compute_input_count")
    payslip_ids = fields.One2many("hr.ec.payroll.payslip", "period_id", string="Roles")
    payslip_count = fields.Integer(compute="_compute_payslip_count")
    notes = fields.Html(string="Observaciones")

    @api.depends("input_ids")
    def _compute_input_count(self):
        for period in self:
            period.input_count = len(period.input_ids)

    @api.depends("payslip_ids")
    def _compute_payslip_count(self):
        for period in self:
            period.payslip_count = len(period.payslip_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("Nuevo")) == _("Nuevo"):
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("hr.ec.payroll.period") or _("Nuevo")
                )
        return super().create(vals_list)

    @api.constrains("date_start", "date_end", "partner_id", "service_contract_id")
    def _check_period(self):
        for rec in self:
            if rec.date_start and rec.date_end and rec.date_end < rec.date_start:
                raise UserError(_("La fecha fin debe ser posterior al inicio."))
            duplicate = self.search_count(
                [
                    ("id", "!=", rec.id),
                    ("partner_id", "=", rec.partner_id.id),
                    ("date_start", "=", rec.date_start),
                    ("date_end", "=", rec.date_end),
                ]
            )
            if duplicate:
                raise UserError(_("Ya existe un período para ese cliente y rango de fechas."))

    def action_set_collecting(self):
        self.write({"state": "collecting"})

    def action_set_processing(self):
        self.write({"state": "processing"})

    def action_set_review(self):
        self.write({"state": "review"})

    def action_set_approved(self):
        self.write({"state": "approved"})

    def action_set_delivered(self):
        self.write({"state": "delivered"})

    def action_set_closed(self):
        self.write({"state": "closed"})

    def action_open_inputs(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Novedades"),
            "res_model": "hr.ec.payroll.input",
            "view_mode": "tree,form",
            "domain": [("period_id", "=", self.id)],
            "context": {
                "default_period_id": self.id,
                "default_partner_id": self.partner_id.id,
            },
        }

    def action_open_project(self):
        self.ensure_one()
        if not self.project_id:
            raise UserError(_("No hay proyecto vinculado."))
        return {
            "type": "ir.actions.act_window",
            "res_model": "project.project",
            "view_mode": "form",
            "res_id": self.project_id.id,
        }

    def action_open_payslips(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Roles de pago"),
            "res_model": "hr.ec.payroll.payslip",
            "view_mode": "tree,form",
            "domain": [("period_id", "=", self.id)],
            "context": {"default_period_id": self.id},
        }

    def action_compute_payslips(self):
        Payslip = self.env["hr.ec.payroll.payslip"]
        Line = self.env["hr.ec.payroll.payslip.line"]
        for period in self:
            if period.state == "closed":
                raise UserError(_("No se puede recalcular un período cerrado."))
            employees = self.env["hr.employee"].search(
                [
                    ("is_client_worker", "=", True),
                    ("client_partner_id", "=", period.partner_id.id),
                ]
            )
            company = period.company_id
            iess_rate = company.th_ec_iess_employee_rate or 0.0
            for employee in employees:
                slip = Payslip.search(
                    [("period_id", "=", period.id), ("employee_id", "=", employee.id)],
                    limit=1,
                )
                if not slip:
                    slip = Payslip.create(
                        {
                            "period_id": period.id,
                            "employee_id": employee.id,
                            "wage_base": employee.th_wage or 0.0,
                        }
                    )
                else:
                    slip.write({"wage_base": employee.th_wage or 0.0})
                slip.line_ids.unlink()
                seq = 10
                lines = []
                taxable_extra = 0.0
                for inp in period.input_ids.filtered(
                    lambda i: i.employee_id == employee and i.state == "confirmed"
                ):
                    cat = inp.input_type_id.category
                    amount = inp.amount or 0.0
                    if cat in ("earning", "other") and amount:
                        line_cat = "earning"
                        if cat == "earning" or inp.input_type_id.code in (
                            "bonus",
                            "commission",
                            "other_in",
                        ):
                            taxable_extra += amount
                    elif cat in ("deduction",) or inp.input_type_id.code in (
                        "deduction",
                        "advance",
                        "loan",
                        "other_out",
                    ):
                        line_cat = "deduction"
                    elif cat == "time":
                        line_cat = "info"
                    else:
                        line_cat = "earning" if amount >= 0 else "deduction"
                    lines.append(
                        {
                            "payslip_id": slip.id,
                            "sequence": seq,
                            "code": inp.input_type_id.code,
                            "name": inp.name,
                            "category": line_cat,
                            "amount": abs(amount) if line_cat == "deduction" else amount,
                        }
                    )
                    seq += 10
                iess_base = (slip.wage_base or 0.0) + taxable_extra
                if iess_rate and iess_base:
                    lines.append(
                        {
                            "payslip_id": slip.id,
                            "sequence": seq,
                            "code": "iess_personal",
                            "name": _("IESS personal (parametrizado)"),
                            "category": "deduction",
                            "amount": round(iess_base * iess_rate, 2),
                        }
                    )
                for vals in lines:
                    Line.create(vals)
                slip.state = "computed"
        return True
