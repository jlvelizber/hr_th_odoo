from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    service_contract_id = fields.Many2one("hr.service.contract", string="Contrato de servicio", index=True)
    th_is_payroll_run = fields.Boolean(
        string="Período de nómina",
        help="Proyecto operativo mensual de nómina (Fase 1: checklist, sin cálculo legal).",
        index=True,
    )
    th_payroll_period = fields.Date(
        string="Mes de nómina",
        help="Primer día del mes al que corresponde el período.",
        index=True,
    )
    th_payroll_state = fields.Selection(
        selection=[
            ("pending", "Pendiente"),
            ("collecting", "En recopilación"),
            ("processing", "En proceso"),
            ("review", "En revisión"),
            ("approved", "Aprobada"),
            ("delivered", "Entregada"),
            ("closed", "Cerrada"),
        ],
        string="Estado nómina",
        tracking=True,
    )


class ProjectTask(models.Model):
    _inherit = "project.task"

    service_contract_id = fields.Many2one(
        related="project_id.service_contract_id",
        store=True,
        string="Contrato de servicio",
    )
