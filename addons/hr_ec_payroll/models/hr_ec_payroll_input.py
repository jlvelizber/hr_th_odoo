from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrEcPayrollInput(models.Model):
    _name = "hr.ec.payroll.input"
    _description = "Novedad de nómina"
    _inherit = ["mail.thread"]
    _order = "period_id, employee_id, id"

    name = fields.Char(string="Descripción", required=True, tracking=True)
    period_id = fields.Many2one(
        "hr.ec.payroll.period",
        string="Período",
        required=True,
        ondelete="cascade",
        index=True,
    )
    partner_id = fields.Many2one(
        related="period_id.partner_id",
        store=True,
        string="Cliente",
    )
    employee_id = fields.Many2one(
        "hr.employee",
        string="Colaborador",
        required=True,
        domain="[('is_client_worker', '=', True), ('client_partner_id', '=', partner_id)]",
        tracking=True,
    )
    input_type_id = fields.Many2one(
        "hr.ec.payroll.input.type",
        string="Tipo",
        required=True,
        ondelete="restrict",
    )
    date = fields.Date(string="Fecha")
    quantity = fields.Float(string="Cantidad / horas", digits=(16, 2))
    amount = fields.Monetary(string="Valor", currency_field="currency_id")
    currency_id = fields.Many2one(
        related="period_id.company_id.currency_id",
        store=True,
    )
    state = fields.Selection(
        selection=[
            ("draft", "Borrador"),
            ("confirmed", "Confirmada"),
            ("cancelled", "Anulada"),
        ],
        default="draft",
        required=True,
        tracking=True,
    )
    notes = fields.Text(string="Notas")

    @api.constrains("period_id")
    def _check_period_not_closed(self):
        for rec in self:
            if rec.period_id.state == "closed":
                raise UserError(_("No se pueden modificar novedades de un período cerrado."))

    def action_confirm(self):
        self.write({"state": "confirmed"})

    def action_cancel(self):
        self.write({"state": "cancelled"})

    def action_draft(self):
        self.write({"state": "draft"})
