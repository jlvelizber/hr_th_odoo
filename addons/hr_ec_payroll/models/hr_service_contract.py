from odoo import fields, models


class HrServiceContract(models.Model):
    _inherit = "hr.service.contract"

    payroll_period_count = fields.Integer(compute="_compute_payroll_period_count")

    def _compute_payroll_period_count(self):
        Period = self.env["hr.ec.payroll.period"]
        for contract in self:
            if contract.service_kind != "payroll":
                contract.payroll_period_count = 0
                continue
            contract.payroll_period_count = Period.search_count(
                [("service_contract_id", "=", contract.id)]
            )

    def action_view_payroll_periods(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Períodos de nómina",
            "res_model": "hr.ec.payroll.period",
            "view_mode": "tree,form,kanban",
            "domain": [("service_contract_id", "=", self.id)],
            "context": {
                "default_service_contract_id": self.id,
                "default_partner_id": self.partner_id.id,
            },
        }
