from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrEcPayrollPayslip(models.Model):
    _name = "hr.ec.payroll.payslip"
    _description = "Rol de pago (borrador calculado)"
    _order = "period_id, employee_id"

    period_id = fields.Many2one(
        "hr.ec.payroll.period",
        required=True,
        ondelete="cascade",
        index=True,
    )
    partner_id = fields.Many2one(related="period_id.partner_id", store=True)
    employee_id = fields.Many2one("hr.employee", required=True, index=True)
    line_ids = fields.One2many("hr.ec.payroll.payslip.line", "payslip_id", string="Líneas")
    wage_base = fields.Monetary(currency_field="currency_id", string="Salario base")
    total_earnings = fields.Monetary(currency_field="currency_id", compute="_compute_totals", store=True)
    total_deductions = fields.Monetary(currency_field="currency_id", compute="_compute_totals", store=True)
    net_pay = fields.Monetary(currency_field="currency_id", compute="_compute_totals", store=True)
    currency_id = fields.Many2one(related="period_id.company_id.currency_id", store=True)
    state = fields.Selection(
        [("draft", "Borrador"), ("computed", "Calculado"), ("done", "Validado")],
        default="draft",
    )
    company_id = fields.Many2one(related="period_id.company_id", store=True)

    _sql_constraints = [
        (
            "period_employee_uniq",
            "unique(period_id, employee_id)",
            "Ya existe un rol para este colaborador en el período.",
        )
    ]

    @api.depends("line_ids.amount", "line_ids.category", "wage_base")
    def _compute_totals(self):
        for slip in self:
            earnings = sum(slip.line_ids.filtered(lambda l: l.category == "earning").mapped("amount"))
            deductions = sum(slip.line_ids.filtered(lambda l: l.category == "deduction").mapped("amount"))
            slip.total_earnings = earnings + slip.wage_base
            slip.total_deductions = deductions
            slip.net_pay = slip.total_earnings - slip.total_deductions


class HrEcPayrollPayslipLine(models.Model):
    _name = "hr.ec.payroll.payslip.line"
    _description = "Línea de rol de pago"
    _order = "sequence, id"

    payslip_id = fields.Many2one("hr.ec.payroll.payslip", required=True, ondelete="cascade")
    sequence = fields.Integer(default=10)
    code = fields.Char(string="Código")
    name = fields.Char(required=True)
    category = fields.Selection(
        [("earning", "Ingreso"), ("deduction", "Descuento"), ("info", "Informativo")],
        required=True,
        default="earning",
    )
    amount = fields.Monetary(currency_field="currency_id")
    currency_id = fields.Many2one(related="payslip_id.currency_id")
