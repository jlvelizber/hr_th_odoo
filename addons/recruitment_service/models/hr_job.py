from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrJob(models.Model):
    _inherit = "hr.job"

    client_partner_id = fields.Many2one(
        "res.partner",
        string="Cliente",
        domain="[('is_company', '=', True)]",
        tracking=True,
    )
    service_contract_id = fields.Many2one(
        "hr.service.contract",
        string="Contrato de servicio",
        domain="[('partner_id', '=', client_partner_id), ('service_kind', '=', 'recruitment'), ('state', '=', 'active')]",
    )
    profile_template_id = fields.Many2one("hr.job.profile.template", string="Perfil plantilla")
    th_project_id = fields.Many2one("project.project", string="Proyecto de selección", copy=False)

    @api.onchange("client_partner_id")
    def _onchange_client_partner_id(self):
        self.service_contract_id = False

    @api.onchange("profile_template_id")
    def _onchange_profile_template_id(self):
        if self.profile_template_id and not self.description:
            self.description = self.profile_template_id.description

    def action_create_selection_project(self):
        self.ensure_one()
        if self.th_project_id:
            raise UserError(_("Esta vacante ya tiene un proyecto de selección."))
        if not self.client_partner_id:
            raise UserError(_("Indique el cliente antes de crear el proyecto."))
        project = self.env["project.project"].create(
            {
                "name": _("Selección: %s — %s") % (self.name, self.client_partner_id.name),
                "partner_id": self.client_partner_id.id,
                "service_contract_id": self.service_contract_id.id if self.service_contract_id else False,
            }
        )
        self.th_project_id = project.id
        self._create_selection_tasks(project)
        return {
            "type": "ir.actions.act_window",
            "res_model": "project.project",
            "view_mode": "form",
            "res_id": project.id,
        }

    def _create_selection_tasks(self, project):
        Task = self.env["project.task"]
        if self.profile_template_id and self.profile_template_id.task_line_ids:
            for line in self.profile_template_id.task_line_ids:
                Task.create(
                    {
                        "name": line.name,
                        "project_id": project.id,
                        "description": line.description,
                    }
                )
            return
        templates = self.env["hr.service.task.template"].search(
            [("template_key", "=", "recruitment")],
            order="sequence, id",
        )
        for line in templates:
            Task.create({"name": line.name, "project_id": project.id})

    def action_open_selection_project(self):
        self.ensure_one()
        if not self.th_project_id:
            raise UserError(_("No hay proyecto de selección."))
        return {
            "type": "ir.actions.act_window",
            "res_model": "project.project",
            "view_mode": "form",
            "res_id": self.th_project_id.id,
        }
