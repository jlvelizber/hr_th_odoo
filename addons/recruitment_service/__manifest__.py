{
    "name": "Reclutamiento para clientes TH",
    "version": "17.0.2.0.0",
    "category": "Human Resources/Recruitment",
    "summary": "Vacantes y perfiles plantilla ligados a clientes externos",
    "author": "Consultora TH",
    "license": "LGPL-3",
    "depends": [
        "hr_service_management",
        "hr_recruitment",
        "calendar",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/hr_recruitment_stage_data.xml",
        "data/recruitment_task_template_data.xml",
        "views/hr_job_profile_template_views.xml",
        "views/hr_job_views.xml",
        "views/hr_applicant_views.xml",
        "views/recruitment_service_menus.xml",
    ],
    "demo": [
        "demo/demo_recruitment.xml",
    ],
    "installable": True,
    "application": False,
}
