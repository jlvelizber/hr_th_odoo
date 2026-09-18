from odoo import models


class HrServiceContract(models.Model):
    _inherit = "hr.service.contract"

    def get_portal_url(self, **kwargs):
        self.ensure_one()
        return "/my/th/contracts/%s" % self.id
