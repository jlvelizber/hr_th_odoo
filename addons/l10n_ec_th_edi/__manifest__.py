{
    "name": "Facturacion electronica SRI (TH)",
    "version": "17.0.1.0.0",
    "category": "Accounting/Localizations/EDI",
    "summary": "Trazabilidad SRI offline y preparacion de comprobantes (base Fase 3)",
    "author": "Consultora TH",
    "license": "LGPL-3",
    "depends": [
        "account",
        "l10n_ec",
        "hr_service_management",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/l10n_ec_th_edi_security.xml",
        "data/ir_sequence_data.xml",
        "views/res_company_views.xml",
        "views/account_move_views.xml",
        "views/sri_ec_document_views.xml",
        "views/l10n_ec_th_edi_menus.xml",
    ],
    "installable": True,
    "application": False,
}
