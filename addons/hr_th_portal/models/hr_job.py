from odoo import models


class HrJob(models.Model):
    _inherit = ["hr.job", "portal.mixin"]

    def _compute_access_url(self):
        super()._compute_access_url()
        for job in self.filtered("client_partner_id"):
            job.access_url = "/my/th/jobs/%s" % job.id
