# -*- coding: utf-8 -*-

DEFAULT_LANG = "es_EC"
FALLBACK_LANG = "es_419"


def ensure_default_lang(env, lang_code=None):
    """Activa es_EC (o fallback) y lo aplica a usuarios, compañías y sitio web."""
    lang_code = lang_code or env["ir.config_parameter"].sudo().get_param(
        "hr_th.default_lang", DEFAULT_LANG
    )
    Lang = env["res.lang"].sudo()
    lang = Lang.search([("code", "=", lang_code), ("active", "=", True)], limit=1)
    if not lang:
        if Lang._activate_lang(lang_code):
            lang = Lang.search([("code", "=", lang_code)], limit=1)
    if not lang and lang_code != FALLBACK_LANG:
        if Lang._activate_lang(FALLBACK_LANG):
            lang = Lang.search([("code", "=", FALLBACK_LANG)], limit=1)
    if not lang:
        return False

    env["res.users"].sudo().with_context(active_test=False).search([]).write(
        {"lang": lang.code}
    )
    env["res.company"].sudo().search([]).partner_id.write({"lang": lang.code})
    if "website" in env:
        env["website"].sudo().search([]).write({"default_lang_id": lang.id})
    env["ir.config_parameter"].sudo().set_param("hr_th.default_lang", lang.code)
    return True


def post_init_hook(env):
    ensure_default_lang(env)
