from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    th_client_status = fields.Selection(
        selection=[
            ("prospect", "Prospecto"),
            ("active", "Activo"),
            ("paused", "En pausa"),
            ("inactive", "Inactivo"),
        ],
        string="Estado TH",
        tracking=True,
    )
    th_approx_headcount = fields.Integer(string="Colaboradores (aprox.)")
    th_commercial_name = fields.Char(string="Nombre comercial")
    th_service_contract_count = fields.Integer(compute="_compute_th_counts")
    th_active_service_count = fields.Integer(compute="_compute_th_counts")
    th_project_count = fields.Integer(compute="_compute_th_counts")
    th_client_employee_count = fields.Integer(compute="_compute_th_counts")
    th_document_count = fields.Integer(compute="_compute_th_counts")
    th_missing_document_count = fields.Integer(compute="_compute_th_counts")
    th_document_ids = fields.One2many("hr.service.document", "partner_id", string="Expediente documental")

    @api.depends("is_company")
    def _compute_th_counts(self):
        Contract = self.env["hr.service.contract"]
        Project = self.env["project.project"]
        Employee = self.env["hr.employee"]
        Document = self.env["hr.service.document"]
        for partner in self:
            if not partner.is_company:
                partner.th_service_contract_count = 0
                partner.th_active_service_count = 0
                partner.th_project_count = 0
                partner.th_client_employee_count = 0
                partner.th_document_count = 0
                partner.th_missing_document_count = 0
                continue
            contracts = Contract.search([("partner_id", "=", partner.id)])
            partner.th_service_contract_count = len(contracts)
            partner.th_active_service_count = len(contracts.filtered(lambda c: c.state == "active"))
            partner.th_project_count = Project.search_count(
                [
                    "|",
                    ("partner_id", "=", partner.id),
                    ("service_contract_id.partner_id", "=", partner.id),
                ]
            )
            partner.th_client_employee_count = Employee.search_count(
                [("client_partner_id", "=", partner.id), ("is_client_worker", "=", True)]
            )
            docs = Document.search([("partner_id", "=", partner.id)])
            partner.th_document_count = len(docs)
            partner.th_missing_document_count = len(docs.filtered(lambda d: d.state == "missing"))

    def action_view_th_applicants(self):
        self.ensure_one()
        if "hr.applicant" not in self.env:
            return False
        return {
            "type": "ir.actions.act_window",
            "name": "Candidatos",
            "res_model": "hr.applicant",
            "view_mode": "kanban,tree,form",
            "domain": [("client_partner_id", "=", self.id)],
        }

    def action_view_th_service_contracts(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Servicios",
            "res_model": "hr.service.contract",
            "view_mode": "tree,form,kanban",
            "domain": [("partner_id", "=", self.id)],
            "context": {"default_partner_id": self.id},
        }

    def action_view_th_projects(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Proyectos",
            "res_model": "project.project",
            "view_mode": "tree,form,kanban",
            "domain": [
                "|",
                ("partner_id", "=", self.id),
                ("service_contract_id.partner_id", "=", self.id),
            ],
            "context": {"default_partner_id": self.id},
        }

    def action_th_init_documents(self):
        for partner in self.filtered("is_company"):
            self.env["hr.service.document"]._init_structure("client", partner=partner)
        return True

    def action_view_th_documents(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Expediente documental",
            "res_model": "hr.service.document",
            "view_mode": "tree,form",
            "domain": [("partner_id", "=", self.id)],
            "context": {"default_partner_id": self.id},
        }

    def action_view_th_client_employees(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Colaboradores del cliente",
            "res_model": "hr.employee",
            "view_mode": "tree,form",
            "domain": [("client_partner_id", "=", self.id), ("is_client_worker", "=", True)],
            "context": {
                "default_client_partner_id": self.id,
                "default_is_client_worker": True,
            },
        }
