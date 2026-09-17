from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrServiceDocumentSection(models.Model):
    _name = "hr.service.document.section"
    _description = "Sección documental TH"
    _order = "scope, sequence, name"

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True)
    scope = fields.Selection(
        selection=[
            ("client", "Cliente"),
            ("employee", "Colaborador"),
            ("project", "Proyecto"),
            ("payroll", "Nómina"),
        ],
        required=True,
        default="client",
    )
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)


class HrServiceDocument(models.Model):
    _name = "hr.service.document"
    _description = "Documento TH"
    _inherit = ["mail.thread"]
    _order = "section_id, id"

    name = fields.Char(string="Descripción", required=True, tracking=True)
    section_id = fields.Many2one(
        "hr.service.document.section",
        string="Sección",
        required=True,
        ondelete="restrict",
        tracking=True,
    )
    partner_id = fields.Many2one("res.partner", string="Cliente", ondelete="cascade", index=True)
    employee_id = fields.Many2one("hr.employee", string="Colaborador", ondelete="cascade", index=True)
    project_id = fields.Many2one("project.project", string="Proyecto", ondelete="cascade", index=True)
    service_contract_id = fields.Many2one(
        "hr.service.contract",
        string="Contrato de servicio",
        ondelete="set null",
    )
    state = fields.Selection(
        selection=[
            ("missing", "Pendiente"),
            ("uploaded", "Cargado"),
            ("verified", "Verificado"),
        ],
        string="Estado",
        default="missing",
        required=True,
        tracking=True,
    )
    file_data = fields.Binary(string="Archivo", attachment=True)
    file_name = fields.Char(string="Nombre archivo")
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
    )

    @api.constrains("partner_id", "employee_id", "project_id")
    def _check_single_parent(self):
        for doc in self:
            parents = sum(
                bool(x)
                for x in (doc.partner_id, doc.employee_id, doc.project_id)
            )
            if parents != 1:
                raise UserError(
                    _("Cada documento debe estar ligado a un solo registro padre (cliente, colaborador o proyecto).")
                )

    @api.onchange("file_data", "file_name")
    def _onchange_file_data(self):
        if self.file_data:
            self.state = "uploaded"

    def write(self, vals):
        if vals.get("file_data"):
            vals.setdefault("state", "uploaded")
        return super().write(vals)

    @api.model
    def _init_structure(self, scope, partner=None, employee=None, project=None):
        Section = self.env["hr.service.document.section"]
        sections = Section.search([("scope", "=", scope), ("active", "=", True)])
        if not sections:
            return self.env["hr.service.document"]
        vals_list = []
        for section in sections:
            domain = [("section_id", "=", section.id)]
            if partner:
                domain.append(("partner_id", "=", partner.id))
            elif employee:
                domain.append(("employee_id", "=", employee.id))
            elif project:
                domain.append(("project_id", "=", project.id))
            else:
                continue
            if self.search_count(domain):
                continue
            vals = {
                "name": section.name,
                "section_id": section.id,
                "state": "missing",
            }
            if partner:
                vals["partner_id"] = partner.id
            elif employee:
                vals["employee_id"] = employee.id
            elif project:
                vals["project_id"] = project.id
            vals_list.append(vals)
        return self.create(vals_list)
