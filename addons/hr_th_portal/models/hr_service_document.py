from odoo import models


class HrServiceDocument(models.Model):
    _inherit = ["hr.service.document", "portal.mixin"]

    def _compute_access_url(self):
        super()._compute_access_url()
        for doc in self:
            doc.access_url = "/my/th/documents/%s" % doc.id
