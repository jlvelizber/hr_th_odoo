from odoo import fields, models


class HrEcPayrollInputType(models.Model):
    _name = "hr.ec.payroll.input.type"
    _description = "Tipo de novedad de nómina"
    _order = "sequence, name"

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    category = fields.Selection(
        selection=[
            ("earning", "Ingreso"),
            ("deduction", "Descuento"),
            ("time", "Tiempo / ausencia"),
            ("other", "Otro"),
        ],
        required=True,
        default="other",
    )
    active = fields.Boolean(default=True)
