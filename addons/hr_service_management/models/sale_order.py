from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    service_contract_id = fields.Many2one("hr.service.contract", string="Contrato TH")
