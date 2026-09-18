{
    "name": "Portal cliente TH",
    "version": "17.0.1.0.0",
    "category": "Human Resources",
    "summary": "Portal multicliente: contratos, documentos, nómina y vacantes por empresa",
    "author": "Consultora TH",
    "license": "LGPL-3",
    "depends": [
        "portal",
        "website",
        "website_payment",
        "hr_service_management",
        "hr_ec_payroll",
        "recruitment_service",
    ],
    "data": [
        "security/hr_th_portal_security.xml",
        "security/ir.model.access.csv",
        "views/res_partner_views.xml",
        "views/portal_templates.xml",
    ],
    "demo": [
        "demo/demo_portal.xml",
    ],
    "installable": True,
    "application": False,
}
