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
        if self.is_company:
            partners = self.child_ids.filtered(lambda p: p.type in ("contact", "other")) | self
        else:
            partners = self
        wizard = self.env["portal.wizard"].create({"partner_ids": [(6, 0, partners.ids)]})
        return wizard._action_open_modal()
