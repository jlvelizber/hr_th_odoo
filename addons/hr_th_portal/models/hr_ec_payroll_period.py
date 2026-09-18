from odoo import models


class HrEcPayrollPeriod(models.Model):
    _inherit = "hr.ec.payroll.period"

    def get_portal_url(self, **kwargs):
        self.ensure_one()
        return "/my/th/payroll/%s" % self.id
