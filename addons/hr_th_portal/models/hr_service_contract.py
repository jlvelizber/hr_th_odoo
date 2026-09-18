from odoo import models


class HrServiceContract(models.Model):
    _inherit = ["hr.service.contract", "portal.mixin"]

    def _compute_access_url(self):
        super()._compute_access_url()
        for contract in self:
            contract.access_url = "/my/th/contracts/%s" % contract.id
