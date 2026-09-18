from odoo import models


class HrEcPayrollPeriod(models.Model):
    _inherit = ["hr.ec.payroll.period", "portal.mixin"]

    def _compute_access_url(self):
        super()._compute_access_url()
        for period in self:
            period.access_url = "/my/th/payroll/%s" % period.id
