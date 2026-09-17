from odoo import api, fields, models, _
from odoo.exceptions import UserError

_MONTHS_ES = (
    "",
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
)


class HrServicePayrollPeriodWizard(models.TransientModel):
    _name = "hr.service.payroll.period.wizard"
    _description = "Crear período mensual de nómina"

    contract_id = fields.Many2one(
        "hr.service.contract",
        string="Contrato de nómina",
        required=True,
        domain="[('service_kind', '=', 'payroll'), ('state', '=', 'active')]",
    )
    period_date = fields.Date(
        string="Mes",
        required=True,
        help="Use el primer día del mes (ej. 01/09/2026).",
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        today = fields.Date.context_today(self)
        if isinstance(today, str):
            today = fields.Date.from_string(today)
        res.setdefault("period_date", today.replace(day=1))
        if self.env.context.get("default_contract_id"):
            res.setdefault("contract_id", self.env.context["default_contract_id"])
        return res

    @api.constrains("period_date")
    def _check_period_first_day(self):
        for wiz in self:
            if wiz.period_date and wiz.period_date.day != 1:
                raise UserError(_("Indique el primer día del mes para el período de nómina."))

    def _period_label(self, period_date):
        return "%s %s" % (_MONTHS_ES[period_date.month], period_date.year)

    def action_create_payroll_project(self):
        self.ensure_one()
        contract = self.contract_id
        if contract.service_kind != "payroll":
            raise UserError(_("El contrato seleccionado no es de nómina."))
        period = self.period_date
        existing = self.env["project.project"].search(
            [
                ("service_contract_id", "=", contract.id),
                ("th_payroll_period", "=", period),
            ],
            limit=1,
        )
        if existing:
            raise UserError(
                _("Ya existe un período de nómina para %s.") % self._period_label(period)
            )
        project = self.env["project.project"].create(
            {
                "name": _("Nómina — %s — %s")
                % (contract.partner_id.name, self._period_label(period)),
                "partner_id": contract.partner_id.id,
                "user_id": contract.user_id.id,
                "service_contract_id": contract.id,
                "th_is_payroll_run": True,
                "th_payroll_period": period,
                "th_payroll_state": "collecting",
            }
        )
        contract._create_tasks_from_template(project, "payroll")
        return {
            "type": "ir.actions.act_window",
            "name": _("Período de nómina"),
            "res_model": "project.project",
            "view_mode": "form",
            "res_id": project.id,
        }
