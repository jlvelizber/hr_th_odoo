from odoo import api, fields, models


class HrThSummary(models.TransientModel):
    _name = "hr.th.summary"
    _description = "Resumen operativo TH"

    filter_partner_id = fields.Many2one(
        "res.partner",
        string="Cliente",
        domain="[('is_company', '=', True)]",
    )
    filter_user_id = fields.Many2one("res.users", string="Responsable")

    active_client_count = fields.Integer(compute="_compute_counts")
    active_service_count = fields.Integer(compute="_compute_counts")
    open_job_count = fields.Integer(compute="_compute_counts")
    applicant_count = fields.Integer(compute="_compute_counts")
    payroll_project_count = fields.Integer(compute="_compute_counts")
    open_task_count = fields.Integer(compute="_compute_counts")
    overdue_task_count = fields.Integer(compute="_compute_counts")
    missing_document_count = fields.Integer(compute="_compute_counts")
    draft_invoice_count = fields.Integer(compute="_compute_counts")

    def _domain_contract(self):
        domain = [("state", "=", "active")]
        if self.filter_partner_id:
            domain.append(("partner_id", "=", self.filter_partner_id.id))
        if self.filter_user_id:
            domain.append(("user_id", "=", self.filter_user_id.id))
        return domain

    def _domain_project_th(self):
        domain = [("service_contract_id", "!=", False)]
        if self.filter_partner_id:
            domain.append(("partner_id", "=", self.filter_partner_id.id))
        if self.filter_user_id:
            domain.append(("user_id", "=", self.filter_user_id.id))
        return domain

    def _domain_tasks(self, extra=None):
        domain = [
            ("project_id", "!=", False),
            ("state", "not in", ("1_done", "1_canceled")),
        ]
        if self.filter_partner_id:
            domain.append(("project_id.partner_id", "=", self.filter_partner_id.id))
        if self.filter_user_id:
            domain.append(("user_ids", "in", self.filter_user_id.id))
        if extra:
            domain.extend(extra)
        return domain

    @api.depends("filter_partner_id", "filter_user_id")
    def _compute_counts(self):
        Partner = self.env["res.partner"]
        Contract = self.env["hr.service.contract"]
        Task = self.env["project.task"]
        Document = self.env["hr.service.document"]
        Move = self.env["account.move"]
        Project = self.env["project.project"]

        for rec in self:
            client_domain = [("is_company", "=", True), ("th_client_status", "=", "active")]
            if rec.filter_partner_id:
                client_domain.append(("id", "=", rec.filter_partner_id.id))

            rec.active_client_count = Partner.search_count(client_domain)
            rec.active_service_count = Contract.search_count(rec._domain_contract())

            open_jobs = 0
            applicants = 0
            if "hr.job" in self.env:
                job_domain = [("no_of_recruitment", ">", 0)]
                if rec.filter_partner_id:
                    job_domain.append(("client_partner_id", "=", rec.filter_partner_id.id))
                open_jobs = self.env["hr.job"].search_count(job_domain)
            if "hr.applicant" in self.env:
                app_domain = [("active", "=", True)]
                if rec.filter_partner_id:
                    app_domain.append(("client_partner_id", "=", rec.filter_partner_id.id))
                applicants = self.env["hr.applicant"].search_count(app_domain)

            payroll_domain = [("th_is_payroll_run", "=", True), ("th_payroll_state", "not in", ("closed",))]
            payroll_domain.extend(
                [x for x in rec._domain_project_th() if x[0] != "service_contract_id"]
            )
            rec.payroll_project_count = Project.search_count(payroll_domain)

            rec.open_task_count = Task.search_count(rec._domain_tasks())
            rec.overdue_task_count = Task.search_count(
                rec._domain_tasks([("date_deadline", "<", fields.Date.today())])
            )

            doc_domain = [("state", "=", "missing")]
            if rec.filter_partner_id:
                doc_domain.append(("partner_id", "=", rec.filter_partner_id.id))
            rec.missing_document_count = Document.search_count(doc_domain)

            inv_domain = [
                ("move_type", "in", ("out_invoice", "out_refund")),
                ("state", "=", "draft"),
            ]
            if rec.filter_partner_id:
                inv_domain.append(("partner_id", "=", rec.filter_partner_id.id))
            rec.draft_invoice_count = Move.search_count(inv_domain)

            rec.open_job_count = open_jobs
            rec.applicant_count = applicants

    def action_refresh_summary(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "hr.th.summary",
            "view_mode": "form",
            "target": "current",
            "res_id": self.id,
        }

    def _action_window(self, name, res_model, domain=None, context=None):
        return {
            "type": "ir.actions.act_window",
            "name": name,
            "res_model": res_model,
            "view_mode": "tree,form,kanban",
            "domain": domain or [],
            "context": context or {},
        }

    def _apply_partner_user_domain(self, domain, partner_field="partner_id", user_field=False):
        result = list(domain)
        if self.filter_partner_id:
            result.append((partner_field, "=", self.filter_partner_id.id))
        if self.filter_user_id and user_field:
            result.append((user_field, "=", self.filter_user_id.id))
        return result

    def action_open_active_clients(self):
        domain = [("is_company", "=", True), ("th_client_status", "=", "active")]
        return self._action_window(
            "Clientes activos",
            "res.partner",
            self._apply_partner_user_domain(domain, partner_field="id"),
            {"default_is_company": True},
        )

    def action_open_active_services(self):
        return self._action_window(
            "Servicios activos",
            "hr.service.contract",
            self._domain_contract(),
        )

    def action_open_open_jobs(self):
        if "hr.job" not in self.env:
            return False
        domain = [("no_of_recruitment", ">", 0)]
        if self.filter_partner_id:
            domain.append(("client_partner_id", "=", self.filter_partner_id.id))
        return self._action_window("Vacantes abiertas", "hr.job", domain)

    def action_open_applicants(self):
        if "hr.applicant" not in self.env:
            return False
        domain = [("active", "=", True)]
        if self.filter_partner_id:
            domain.append(("client_partner_id", "=", self.filter_partner_id.id))
        return self._action_window("Candidatos en proceso", "hr.applicant", domain)

    def action_open_payroll_projects(self):
        domain = [("th_is_payroll_run", "=", True), ("th_payroll_state", "not in", ("closed",))]
        if self.filter_partner_id:
            domain.append(("partner_id", "=", self.filter_partner_id.id))
        if self.filter_user_id:
            domain.append(("user_id", "=", self.filter_user_id.id))
        return self._action_window("Nóminas en proceso", "project.project", domain)

    def action_open_open_tasks(self):
        return self._action_window("Tareas abiertas", "project.task", self._domain_tasks())

    def action_open_overdue_tasks(self):
        return self._action_window(
            "Tareas vencidas",
            "project.task",
            self._domain_tasks([("date_deadline", "<", fields.Date.today())]),
        )

    def action_open_missing_documents(self):
        domain = [("state", "=", "missing")]
        if self.filter_partner_id:
            domain.append(("partner_id", "=", self.filter_partner_id.id))
        return self._action_window("Documentos pendientes", "hr.service.document", domain)

    def action_open_draft_invoices(self):
        domain = [
            ("move_type", "in", ("out_invoice", "out_refund")),
            ("state", "=", "draft"),
        ]
        if self.filter_partner_id:
            domain.append(("partner_id", "=", self.filter_partner_id.id))
        return self._action_window("Facturas borrador", "account.move", domain)
