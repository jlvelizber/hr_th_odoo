from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    is_client_worker = fields.Boolean(
        string="Colaborador de cliente",
        help="Marcar si la persona trabaja para un cliente de la consultora, no para la consultora.",
    )
    client_partner_id = fields.Many2one(
        "res.partner",
        string="Cliente empleador",
        domain="[('is_company', '=', True)]",
    )
    th_document_ids = fields.One2many(
        "hr.service.document",
        "employee_id",
        string="Expediente documental",
    )

    def action_th_init_documents(self):
        for employee in self:
            self.env["hr.service.document"]._init_structure("employee", employee=employee)
        return True

    @api.onchange("is_client_worker")
    def _onchange_is_client_worker(self):
        if not self.is_client_worker:
            self.client_partner_id = False
