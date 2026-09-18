from odoo import api, models

from odoo.addons.hr_service_management.hooks import DEFAULT_LANG


class ResPartnerLang(models.Model):
    _inherit = "res.partner"

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if "lang" in fields_list and not res.get("lang"):
            code = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("hr_th.default_lang", DEFAULT_LANG)
            )
            if self.env["res.lang"].sudo().search(
                [("code", "=", code), ("active", "=", True)], limit=1
            ):
                res["lang"] = code
        return res
