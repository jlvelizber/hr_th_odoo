from odoo import fields, models, _


class AccountMove(models.Model):
    _inherit = "account.move"

    sri_ec_document_ids = fields.One2many("sri.ec.document", "move_id", string="Comprobantes SRI")
    sri_ec_document_count = fields.Integer(compute="_compute_sri_ec_document_count")

    def _compute_sri_ec_document_count(self):
        for move in self:
            move.sri_ec_document_count = len(move.sri_ec_document_ids)

    def action_create_sri_document(self):
        self.ensure_one()
        doc = self.env["sri.ec.document"].create({"move_id": self.id})
        return {
            "type": "ir.actions.act_window",
            "res_model": "sri.ec.document",
            "view_mode": "form",
            "res_id": doc.id,
        }

    def action_view_sri_documents(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("SRI"),
            "res_model": "sri.ec.document",
            "view_mode": "tree,form",
            "domain": [("move_id", "=", self.id)],
        }
