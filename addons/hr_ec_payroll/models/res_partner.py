from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    th_payroll_period_count = fields.Integer(compute="_compute_th_payroll_counts")
    th_open_payroll_period_count = fields.Integer(compute="_compute_th_payroll_counts")

    def _compute_th_payroll_counts(self):
        Period = self.env["hr.ec.payroll.period"]
        for partner in self:
            if not partner.is_company:
                partner.th_payroll_period_count = 0
                partner.th_open_payroll_period_count = 0
                continue
            periods = Period.search([("partner_id", "=", partner.id)])
            partner.th_payroll_period_count = len(periods)
            partner.th_open_payroll_period_count = len(
                periods.filtered(lambda p: p.state != "closed")
            )

    def action_view_th_payroll_periods(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Períodos de nómina",
            "res_model": "hr.ec.payroll.period",
            "view_mode": "tree,form,kanban",
            "domain": [("partner_id", "=", self.id)],
            "context": {"default_partner_id": self.id},
        }
