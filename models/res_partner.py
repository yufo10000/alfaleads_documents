from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_legal_partner_type = fields.Boolean(compute="_compute_partner_type")
    is_advertiser_partner_type = fields.Boolean(compute="_compute_partner_type")
    legal_partner_type_id = fields.Many2oneReference(compute="_compute_partner_type")
    advertiser_partner_type_id = fields.Many2oneReference(
        compute="_compute_partner_type"
    )

    advertisers_ids = fields.Many2many(
        comodel_name="res.partner",
        relation="res_partner_available_relations",
        column1="legals",
        column2="advertisers",
        string="Advertisers",
    )

    legals_ids = fields.Many2many(
        comodel_name="res.partner",
        relation="res_partner_available_relations",
        column1="advertisers",
        column2="legals",
        string="Legals",
    )

    @api.depends("partner_type_id")
    def _compute_partner_type(self):
        try:
            legal_partner_type = self.env.ref("alfaleads_crm.res_partner_type_legal")
            advertiser_partner_type = self.env.ref(
                "alfaleads_crm.res_partner_type_advertiser"
            )
        except ValueError:
            legal_partner_type = None
            advertiser_partner_type = None
        for rec in self:
            rec.legal_partner_type_id = legal_partner_type
            rec.advertiser_partner_type_id = advertiser_partner_type
            rec.is_legal_partner_type = (
                rec.partner_type_id == legal_partner_type
                and legal_partner_type is not None
                and rec.id
            )
            rec.is_advertiser_partner_type = (
                rec.partner_type_id == advertiser_partner_type
                and advertiser_partner_type is not None
                and rec.id
            )
