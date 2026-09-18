from odoo import api, fields, models


class HrThSummary(models.TransientModel):
    _inherit = "hr.th.summary"

    open_payroll_period_count = fields.Integer(compute="_compute_payroll_kpis")
    payslip_draft_count = fields.Integer(compute="_compute_payroll_kpis")

    @api.depends("filter_partner_id", "filter_user_id")
    def _compute_payroll_kpis(self):
        Period = self.env["hr.ec.payroll.period"]
        Payslip = self.env["hr.ec.payroll.payslip"]
        for rec in self:
            period_domain = [("state", "!=", "closed")]
            if rec.filter_partner_id:
                period_domain.append(("partner_id", "=", rec.filter_partner_id.id))
            if rec.filter_user_id:
                period_domain.append(("user_id", "=", rec.filter_user_id.id))
            rec.open_payroll_period_count = Period.search_count(period_domain)
            slip_domain = [("state", "in", ("draft", "computed"))]
            if rec.filter_partner_id:
                slip_domain.append(("partner_id", "=", rec.filter_partner_id.id))
            rec.payslip_draft_count = Payslip.search_count(slip_domain)

    def action_open_ec_payroll_periods(self):
        domain = [("state", "!=", "closed")]
        if self.filter_partner_id:
            domain.append(("partner_id", "=", self.filter_partner_id.id))
        if self.filter_user_id:
            domain.append(("user_id", "=", self.filter_user_id.id))
        return self._action_window("Períodos nómina (registro)", "hr.ec.payroll.period", domain)

    def action_open_payslips(self):
        domain = [("state", "in", ("draft", "computed"))]
        if self.filter_partner_id:
            domain.append(("partner_id", "=", self.filter_partner_id.id))
        return self._action_window("Roles de pago", "hr.ec.payroll.payslip", domain)
