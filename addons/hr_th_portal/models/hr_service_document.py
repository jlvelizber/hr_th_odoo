from odoo import models


class HrServiceDocument(models.Model):
    _inherit = "hr.service.document"

    def get_portal_url(self, **kwargs):
        self.ensure_one()
        return "/my/th/documents/%s" % self.id
