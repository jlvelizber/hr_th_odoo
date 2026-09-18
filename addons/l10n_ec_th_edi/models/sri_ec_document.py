from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SriEcDocument(models.Model):
    _name = "sri.ec.document"
    _description = "Comprobante electronico SRI (trazabilidad)"
    _inherit = ["mail.thread"]
    _order = "create_date desc, id desc"

    name = fields.Char(string="Referencia", required=True, copy=False, readonly=True, default=lambda self: _("Nuevo"))
    move_id = fields.Many2one("account.move", string="Factura", required=True, ondelete="cascade", index=True)
    partner_id = fields.Many2one(related="move_id.partner_id", store=True)
    access_key = fields.Char(string="Clave de acceso", size=49, copy=False, tracking=True)
    state = fields.Selection(
        [
            ("draft", "Borrador"),
            ("xml_ready", "XML listo"),
            ("signed", "Firmado"),
            ("received", "RECIBIDA"),
            ("authorized", "AUT"),
            ("returned", "DEVUELTA"),
            ("rejected", "NAT"),
            ("error", "Error"),
        ],
        default="draft",
        tracking=True,
    )
    reception_message = fields.Text(string="Mensaje recepcion")
    authorization_message = fields.Text(string="Mensaje autorizacion")
    xml_unsigned = fields.Text(string="XML (borrador)")
    company_id = fields.Many2one(related="move_id.company_id", store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("Nuevo")) == _("Nuevo"):
                vals["name"] = self.env["ir.sequence"].next_by_code("sri.ec.document") or _("Nuevo")
        return super().create(vals_list)

    def action_prepare_draft_xml(self):
        for doc in self:
            if doc.move_id.move_type not in ("out_invoice", "out_refund"):
                raise UserError(_("Solo facturas de cliente."))
            doc.write(
                {
                    "state": "xml_ready",
                    "xml_unsigned": "<!-- Pendiente: generar XML factura 1.1.0 conforme XSD SRI -->",
                }
            )
        return True

    def action_mark_signed(self):
        self.write({"state": "signed"})

    def action_simulate_send(self):
        """Placeholder Fase 3: integrar SOAP recepcion/autorizacion offline."""
        for doc in self.filtered(lambda d: d.state == "signed"):
            doc.write({"state": "received", "reception_message": "Simulacion: RECIBIDA (configurar certificado y SOAP)."})
        return True
