import calendar

from odoo import _, fields, models
from odoo.exceptions import UserError


class HrServicePayrollPeriodWizard(models.TransientModel):
    _inherit = "hr.service.payroll.period.wizard"

    def action_create_payroll_project(self):
        res = super().action_create_payroll_project()
        self.ensure_one()
        contract = self.contract_id
        period_start = self.period_date
        if period_start.day != 1:
            raise UserError(_("Use el primer día del mes para el período."))
        last_dom = calendar.monthrange(period_start.year, period_start.month)[1]
        last_day = period_start.replace(day=last_dom)
        Period = self.env["hr.ec.payroll.period"]
        existing = Period.search(
            [
                ("service_contract_id", "=", contract.id),
                ("date_start", "=", period_start),
            ],
            limit=1,
        )
        if not existing:
            project_id = False
            if res.get("res_id") and res.get("res_model") == "project.project":
                project_id = res["res_id"]
            Period.create(
                {
                    "partner_id": contract.partner_id.id,
                    "service_contract_id": contract.id,
                    "date_start": period_start,
                    "date_end": last_day,
                    "user_id": contract.user_id.id,
                    "project_id": project_id,
                    "state": "collecting",
                }
            )
        return res
