from odoo import api, models

from odoo.addons.hr_service_management.hooks import DEFAULT_LANG


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def _get_default_lang(self):
        param = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("hr_th.default_lang", DEFAULT_LANG)
        )
        if self.env["res.lang"].sudo().search(
            [("code", "=", param), ("active", "=", True)], limit=1
        ):
            return param
        return super()._get_default_lang() if hasattr(super(), "_get_default_lang") else DEFAULT_LANG

    @api.model_create_multi
    def create(self, vals_list):
        default_lang = self._get_default_lang()
        for vals in vals_list:
            vals.setdefault("lang", default_lang)
        return super().create(vals_list)
