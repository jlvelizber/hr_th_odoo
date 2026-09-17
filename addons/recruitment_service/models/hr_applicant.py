from odoo import fields, models, _


class HrApplicant(models.Model):
    _inherit = "hr.applicant"

    client_partner_id = fields.Many2one(
        "res.partner",
        string="Cliente",
        related="job_id.client_partner_id",
        store=True,
        readonly=True,
    )
    th_interview_score = fields.Float(string="Puntuación", help="Evaluación simple del proceso.")
    th_interview_notes = fields.Text(string="Notas de entrevista")

    def action_schedule_interview(self):
        self.ensure_one()
        activity_type = self.env.ref("mail.mail_activity_data_meeting", raise_if_not_found=False)
        ctx = {
            "default_res_model": "hr.applicant",
            "default_res_id": self.id,
            "default_summary": _("Entrevista: %s") % (self.partner_name or self.name),
        }
        if activity_type:
            ctx["default_activity_type_id"] = activity_type.id
        return {
            "type": "ir.actions.act_window",
            "name": _("Programar entrevista"),
            "res_model": "mail.activity.schedule",
            "view_mode": "form",
            "target": "new",
            "context": ctx,
        }
