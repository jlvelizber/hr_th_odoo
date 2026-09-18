from odoo import fields, models, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    th_portal_access_count = fields.Integer(compute="_compute_th_portal_access_count")

    def _compute_th_portal_access_count(self):
        Users = self.env["res.users"]
        for partner in self:
            if not partner.is_company:
                partner.th_portal_access_count = 0
                continue
            contacts = partner.child_ids | partner
            partner.th_portal_access_count = Users.search_count(
                [
                    ("partner_id", "in", contacts.ids),
                    ("share", "=", True),
                ]
            )

    def action_th_grant_portal(self):
        self.ensure_one()
        wizard = (
            self.env["portal.wizard"]
            .with_context(
                active_model="res.partner",
                active_ids=self.ids,
                default_partner_ids=self.ids,
            )
            .create({})
        )
        return wizard._action_open_modal()
