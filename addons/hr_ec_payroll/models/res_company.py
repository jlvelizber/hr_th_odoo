from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    th_ec_iess_employee_rate = fields.Float(
        string="IESS personal (%)",
        default=0.0945,
        help="Parametrizable. Verificar normativa vigente antes de usar en producción.",
    )
    th_ec_iess_employer_rate = fields.Float(
        string="IESS patronal (%)",
        default=0.1115,
        help="Parametrizable. Verificar normativa vigente antes de usar en producción.",
    )
    th_ec_payroll_legal_notes = fields.Text(
        string="Notas normativas nómina",
        help="Referencias legales acordadas con asesoría laboral.",
    )
