from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrServiceContract(models.Model):
    _name = "hr.service.contract"
    _description = "Contrato de servicio TH"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_start desc, id desc"

    name = fields.Char(
        string="Referencia",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _("Nuevo"),
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Cliente",
        required=True,
        domain="[('is_company', '=', True)]",
        tracking=True,
    )
    product_id = fields.Many2one(
        "product.product",
        string="Servicio",
        required=True,
        domain="[('type', '=', 'service')]",
        tracking=True,
    )
    service_kind = fields.Selection(
        selection=[
            ("payroll", "Nómina"),
            ("recruitment", "Reclutamiento"),
            ("hr_management", "Gestión TH"),
            ("advisory", "Asesoría laboral"),
            ("admin", "Administrativo"),
            ("other", "Otro"),
        ],
        string="Tipo de servicio",
        tracking=True,
    )
    service_mode = fields.Selection(
        selection=[
            ("recurrent", "Recurrente"),
            ("one_shot", "Puntual"),
        ],
        string="Modalidad",
        default="recurrent",
        required=True,
        tracking=True,
    )
    periodicity = fields.Selection(
        selection=[
            ("monthly", "Mensual"),
            ("quarterly", "Trimestral"),
            ("annual", "Anual"),
            ("once", "Única vez"),
        ],
        string="Periodicidad",
        default="monthly",
    )
    user_id = fields.Many2one(
        "res.users",
        string="Responsable",
        default=lambda self: self.env.user,
        tracking=True,
    )
    company_id = fields.Many2one(
        "res.company",
        string="Compañía",
        required=True,
        default=lambda self: self.env.company,
    )
    date_start = fields.Date(string="Inicio", tracking=True)
    date_end = fields.Date(string="Fin", tracking=True)
    state = fields.Selection(
        selection=[
            ("draft", "Borrador"),
            ("active", "Activo"),
            ("done", "Finalizado"),
            ("cancel", "Cancelado"),
        ],
        string="Estado",
        default="draft",
        tracking=True,
    )
    price_unit = fields.Float(string="Precio acordado")
    currency_id = fields.Many2one(
        "res.currency",
        related="company_id.currency_id",
        store=True,
    )
    sale_order_id = fields.Many2one("sale.order", string="Pedido de venta", copy=False)
    project_id = fields.Many2one("project.project", string="Proyecto operativo", copy=False)
    notes = fields.Html(string="Observaciones")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("Nuevo")) == _("Nuevo"):
                vals["name"] = self.env["ir.sequence"].next_by_code("hr.service.contract") or _("Nuevo")
        return super().create(vals_list)

    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.product_id and not self.service_kind:
            code = self.product_id.default_code or ""
            mapping = {
                "PAYROLL": "payroll",
                "RECRUIT": "recruitment",
            }
            self.service_kind = mapping.get(code.upper(), "other")

    def action_confirm(self):
        for contract in self:
            if contract.state != "draft":
                continue
            contract.state = "active"
        return True

    def action_done(self):
        self.write({"state": "done"})

    def action_cancel(self):
        self.write({"state": "cancel"})

    def action_draft(self):
        self.write({"state": "draft"})

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

    def action_open_sale_order(self):
        self.ensure_one()
        if not self.sale_order_id:
            raise UserError(_("No hay pedido de venta vinculado."))
        return {
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "view_mode": "form",
            "res_id": self.sale_order_id.id,
        }

    def action_create_sale_order(self):
        self.ensure_one()
        if self.state != "active":
            raise UserError(_("Active el contrato antes de generar el pedido de venta."))
        if self.sale_order_id:
            raise UserError(_("Este contrato ya tiene un pedido de venta."))
        price = self.price_unit or self.product_id.list_price
        order = self.env["sale.order"].create(
            {
                "partner_id": self.partner_id.id,
                "service_contract_id": self.id,
                "user_id": self.user_id.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_id.id,
                            "product_uom_qty": 1.0,
                            "price_unit": price,
                            "name": self.product_id.display_name,
                        },
                    )
                ],
            }
        )
        self.sale_order_id = order.id
        return self.action_open_sale_order()

    def action_open_payroll_period_wizard(self):
        self.ensure_one()
        if self.service_kind != "payroll":
            raise UserError(_("Esta acción aplica solo a contratos de nómina."))
        return {
            "type": "ir.actions.act_window",
            "name": _("Nuevo período de nómina"),
            "res_model": "hr.service.payroll.period.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_contract_id": self.id},
        }

    def action_view_payroll_projects(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Períodos de nómina"),
            "res_model": "project.project",
            "view_mode": "kanban,tree,form",
            "domain": [
                ("service_contract_id", "=", self.id),
                ("th_is_payroll_run", "=", True),
            ],
            "context": {"default_service_contract_id": self.id},
        }

    def action_create_project(self):
        self.ensure_one()
        if self.project_id:
            raise UserError(_("Este contrato ya tiene un proyecto vinculado."))
        project = self.env["project.project"].create(
            {
                "name": "%s — %s" % (self.partner_id.name, self.product_id.name),
                "partner_id": self.partner_id.id,
                "user_id": self.user_id.id,
                "service_contract_id": self.id,
            }
        )
        self.project_id = project.id
        template_key = self.service_kind or "other"
        self._create_tasks_from_template(project, template_key)
        return {
            "type": "ir.actions.act_window",
            "res_model": "project.project",
            "view_mode": "form",
            "res_id": project.id,
        }

    def _create_tasks_from_template(self, project, template_key):
        Task = self.env["project.task"]
        templates = self.env["hr.service.task.template"].search(
            [("template_key", "=", template_key)],
            order="sequence, id",
        )
        if not templates:
            templates = self.env["hr.service.task.template"].search(
                [("template_key", "=", "other")],
                order="sequence, id",
            )
        for line in templates:
            Task.create(
                {
                    "name": line.name,
                    "project_id": project.id,
                    "user_ids": [(6, 0, [self.user_id.id])] if self.user_id else False,
                    "description": line.description,
                }
            )


class HrServiceTaskTemplate(models.Model):
    _name = "hr.service.task.template"
    _description = "Plantilla de tareas por tipo de servicio"
    _order = "template_key, sequence, id"

    name = fields.Char(required=True)
    template_key = fields.Selection(
        selection=[
            ("payroll", "Nómina"),
            ("recruitment", "Reclutamiento"),
            ("hr_management", "Gestión TH"),
            ("advisory", "Asesoría laboral"),
            ("admin", "Administrativo"),
            ("other", "Otro"),
        ],
        required=True,
    )
    sequence = fields.Integer(default=10)
    description = fields.Html()
