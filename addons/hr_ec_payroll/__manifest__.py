{
    "name": "Nómina operativa Ecuador (TH)",
    "version": "17.0.1.0.0",
    "category": "Human Resources/Payroll",
    "summary": "Períodos de nómina por cliente, novedades y estados (sin motor legal completo)",
    "author": "Consultora TH",
    "license": "LGPL-3",
    "depends": [
        "hr_service_management",
        "hr",
    ],
    "data": [
        "security/hr_ec_payroll_security.xml",
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "data/hr_ec_payroll_input_type_data.xml",
        "views/hr_ec_payroll_period_views.xml",
        "views/hr_ec_payroll_input_views.xml",
        "views/hr_ec_payroll_menus.xml",
        "views/res_partner_views.xml",
        "views/hr_service_contract_views.xml",
        "report/hr_ec_payroll_reports.xml",
    ],
    "demo": [
        "demo/demo_payroll.xml",
    ],
    "installable": True,
    "application": False,
}
