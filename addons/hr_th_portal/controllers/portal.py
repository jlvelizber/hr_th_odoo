import base64

from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class ThCustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if request.env.user.share:
            Contract = request.env["hr.service.contract"]
            Document = request.env["hr.service.document"]
            Period = request.env["hr.ec.payroll.period"]
            Job = request.env["hr.job"]
            if "th_contract_count" in counters:
                values["th_contract_count"] = Contract.search_count([])
            if "th_document_count" in counters:
                values["th_document_count"] = Document.search_count([])
            if "th_payroll_period_count" in counters:
                values["th_payroll_period_count"] = Period.search_count([])
            if "th_job_count" in counters:
                values["th_job_count"] = Job.search_count([("client_partner_id", "!=", False)])
        return values

    @http.route(["/my/th/contracts", "/my/th/contracts/page/<int:page>"], type="http", auth="user", website=True)
    def portal_th_contracts(self, page=1, **kw):
        Contract = request.env["hr.service.contract"]
        total = Contract.search_count([])
        pager = portal_pager(
            url="/my/th/contracts",
            total=total,
            page=page,
            step=20,
        )
        contracts = Contract.search([], limit=20, offset=pager["offset"], order="date_start desc")
        return request.render(
            "hr_th_portal.portal_th_contracts",
            {"contracts": contracts, "page_name": "th_contracts", "pager": pager},
        )

    @http.route(["/my/th/contracts/<int:contract_id>"], type="http", auth="user", website=True)
    def portal_th_contract_detail(self, contract_id, access_token=None, **kw):
        contract = self._document_check_access("hr.service.contract", contract_id, access_token=access_token)
        return request.render(
            "hr_th_portal.portal_th_contract_detail",
            {"contract": contract, "page_name": "th_contracts"},
        )

    @http.route(["/my/th/documents", "/my/th/documents/page/<int:page>"], type="http", auth="user", website=True)
    def portal_th_documents(self, page=1, **kw):
        Document = request.env["hr.service.document"]
        total = Document.search_count([])
        pager = portal_pager(url="/my/th/documents", total=total, page=page, step=20)
        documents = Document.search([], limit=20, offset=pager["offset"], order="section_id, id")
        return request.render(
            "hr_th_portal.portal_th_documents",
            {"documents": documents, "page_name": "th_documents", "pager": pager},
        )

    @http.route(
        ["/my/th/documents/<int:document_id>"],
        type="http",
        auth="user",
        website=True,
        methods=["GET", "POST"],
        csrf=True,
    )
    def portal_th_document_detail(self, document_id, access_token=None, **post):
        document = self._document_check_access("hr.service.document", document_id, access_token=access_token)
        if request.httprequest.method == "POST":
            document.check_access_rights("write")
            document.check_access_rule("write")
            upload = request.httprequest.files.get("ufile")
            if upload and upload.filename:
                document.write(
                    {
                        "file_data": base64.b64encode(upload.read()),
                        "file_name": upload.filename,
                        "state": "uploaded",
                    }
                )
            return request.redirect("/my/th/documents/%s" % document.id)
        return request.render(
            "hr_th_portal.portal_th_document_detail",
            {"document": document, "page_name": "th_documents"},
        )

    @http.route(["/my/th/payroll", "/my/th/payroll/page/<int:page>"], type="http", auth="user", website=True)
    def portal_th_payroll(self, page=1, **kw):
        Period = request.env["hr.ec.payroll.period"]
        total = Period.search_count([])
        pager = portal_pager(url="/my/th/payroll", total=total, page=page, step=20)
        periods = Period.search([], limit=20, offset=pager["offset"], order="date_start desc")
        return request.render(
            "hr_th_portal.portal_th_payroll",
            {"periods": periods, "page_name": "th_payroll", "pager": pager},
        )

    @http.route(["/my/th/payroll/<int:period_id>"], type="http", auth="user", website=True)
    def portal_th_payroll_detail(self, period_id, access_token=None, **kw):
        period = self._document_check_access("hr.ec.payroll.period", period_id, access_token=access_token)
        return request.render(
            "hr_th_portal.portal_th_payroll_detail",
            {"period": period, "page_name": "th_payroll"},
        )

    @http.route(["/my/th/jobs", "/my/th/jobs/page/<int:page>"], type="http", auth="user", website=True)
    def portal_th_jobs(self, page=1, **kw):
        Job = request.env["hr.job"]
        domain = [("client_partner_id", "!=", False)]
        total = Job.search_count(domain)
        pager = portal_pager(url="/my/th/jobs", total=total, page=page, step=20)
        jobs = Job.search(domain, limit=20, offset=pager["offset"])
        return request.render(
            "hr_th_portal.portal_th_jobs",
            {"jobs": jobs, "page_name": "th_jobs", "pager": pager},
        )

    @http.route(["/my/th/jobs/<int:job_id>"], type="http", auth="user", website=True)
    def portal_th_job_detail(self, job_id, **kw):
        job = self._document_check_access("hr.job", job_id)
        return request.render(
            "hr_th_portal.portal_th_job_detail",
            {"job": job, "page_name": "th_jobs"},
        )
