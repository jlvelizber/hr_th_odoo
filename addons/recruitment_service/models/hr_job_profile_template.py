from odoo import fields, models


class HrJobProfileTemplate(models.Model):
    _name = "hr.job.profile.template"
    _description = "Perfil plantilla de cargo"
    _order = "name"

    name = fields.Char(required=True)
    description = fields.Html(string="Descripción del puesto")
    requirements = fields.Html(string="Requisitos")
    active = fields.Boolean(default=True)
    task_line_ids = fields.One2many(
        "hr.job.profile.template.task",
        "template_id",
        string="Tareas del proceso",
    )


class HrJobProfileTemplateTask(models.Model):
    _name = "hr.job.profile.template.task"
    _description = "Tarea plantilla de reclutamiento"
    _order = "sequence, id"

    template_id = fields.Many2one(
        "hr.job.profile.template",
        required=True,
        ondelete="cascade",
    )
    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    description = fields.Html()
