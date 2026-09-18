from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    th_wage = fields.Monetary(
        string="Salario base (cliente)",
        currency_field="th_wage_currency_id",
        help="Referencia para cálculo de rol; no sustituye asesoría legal.",
    )
    th_wage_currency_id = fields.Many2one(
        related="company_id.currency_id",
        string="Moneda salario",
    )
