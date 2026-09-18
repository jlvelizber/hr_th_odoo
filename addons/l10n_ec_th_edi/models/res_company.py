from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    sri_th_ambiente = fields.Selection(
        [("1", "Pruebas"), ("2", "Produccion")],
        string="Ambiente SRI",
        default="1",
    )
    sri_th_emission_type = fields.Selection(
        [("1", "Normal (offline)")],
        string="Tipo emision",
        default="1",
    )
    sri_th_certificate_note = fields.Char(
        string="Certificado .p12 (ruta segura)",
        help="No versionar el archivo. Usar ruta fuera del repositorio o vault.",
    )
    sri_th_enabled = fields.Boolean(string="Habilitar flujo SRI TH")
