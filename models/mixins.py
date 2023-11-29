from odoo import api, fields, models
from odoo.exceptions import UserError

FILL_STATUS_SELECTION = [
    ("in_progress", "Partial filled"),
    ("done", "Full filled"),
]

ACTIVITY_STATUS_SELECTION = [
    ("in_progress", "Not Active"),
    ("done", "Active"),
]


class FillStatusMixin(models.BaseModel):
    _name = "alfaleads_documents.fill_status_mixin"
    _description = "fill_status computed field mixin"
    _abstract = True

    _fill_status_required_fields = []

    fill_status = fields.Selection(
        selection=FILL_STATUS_SELECTION,
        string="Fill status",
        compute="_compute_fill_status",
    )

    def _compute_fill_status(self):
        for rec in self:
            rec.fill_status = self._check_fill_status(rec)

    @classmethod
    def _check_fill_status(cls, record):
        status = "done"
        for field in cls._fill_status_required_fields:
            if not getattr(record, field):
                status = "in_progress"
                break

        return status


class DraftPostedMixin(models.BaseModel):
    _name = "alfaleads_documents.draft_posted_mixin"
    _description = "Draft/Posted Mixin"
    _inherit = "alfaleads_utils.check_required_fields_mixin"
    _abstract = True
    POSTED_REQUIRED_FIELDS = []

    state = fields.Selection(
        [("draft", "Draft"), ("posted", "Posted")], string="State", default="draft"
    )

    def make_draft(self):
        self.ensure_one()
        self.document_ids.sudo().unlink()
        self.state = "draft"
        self.write({"state": "draft"})

    def make_posted(self):
        self.ensure_one()
        self.check_required_fields(self.POSTED_REQUIRED_FIELDS)
        self.state = "posted"
        self.write({"state": "posted"})
        self._create_documents_for_attachments()

    def _create_documents_for_attachments(self):
        for attachment in self.attachment_ids:
            exists = self.env["documents.document"].search(
                [("attachment_id", "=", attachment.id), ("active", "in", [False, True])]
            )
            if not exists:
                self.env["documents.document"].create(
                    [
                        self._get_document_vals(self, attachment),
                    ]
                )

    @classmethod
    def _get_document_vals(cls, obj, attachment):
        pass

    def unlink(self):
        for rec in self:
            if rec.state == "posted":
                raise UserError("You can't delete object in status POSTED")
        super().unlink()

    def write(self, vals):
        for record in self:
            if record.state == "posted":
                record._check_attachments_for_delete(vals)

        return super().write(vals)

    def _check_attachments_for_delete(self, vals, raise_error=True):
        result = True
        exists_attachments_ids = set(self.attachment_ids.ids)
        new_attachments = vals.get("attachment_ids")
        if new_attachments:
            new_attachments_ids = set(new_attachments[0][2])
            if len(exists_attachments_ids - new_attachments_ids):
                result = False

        if not result and raise_error:
            raise UserError("You can't delete attachments in status POSTED")

        return result


# Deprecated class for backwards compatibility and accounting documents
class AttachmentsDocumentMixin(models.BaseModel):
    _name = "alfaleads_documents.attachment_mixin"
    _description = "Attachment Mixin"
    _abstract = True

    @api.model_create_multi
    def create(self, vals_list):
        objects = super().create(vals_list)
        self._create_documents_for_attachments(objects)
        return objects

    def write(self, vals):
        new_attachments = vals.get("attachment_ids")
        if new_attachments and not new_attachments[0][2]:
            raise UserError("You can't delete attachments from here")

        result = super().write(vals)
        if result and vals.get("attachment_ids"):
            self._create_documents_for_attachments(self)
        return result

    def _create_documents_for_attachments(self, objects):
        for obj in objects:
            documents = self.env["documents.document"].search(
                [
                    ("accounting_id", "=", obj.id),
                ]
            )
            for attachment in obj.attachment_ids.filtered(
                lambda x: x not in documents.mapped("attachment_id")
            ):
                self.env["documents.document"].create(
                    [
                        self._get_document_vals(obj, attachment),
                    ]
                )

            for document in documents.filtered(
                lambda x: x.attachment_id not in obj.attachment_ids
            ):
                shared_documents = self.env["documents.share"].search_count(
                    [
                        "|",
                        ("folder_id", "=", document.folder_id.id),
                        ("document_ids", "in", [document.id]),
                    ]
                )
                if not shared_documents:
                    document.unlink()

    @classmethod
    def _get_document_vals(cls, obj, attachment):
        pass


class AlfaleadsContractsRelatedMixin(models.BaseModel):
    _name = "alfaleads_documents.contract_related_mixin"
    _description = "Contract Related Mixin"
    _abstract = True

    @classmethod
    def _get_document_vals(cls, obj, attachment):
        return {
            "attachment_id": attachment.id,
            "res_id": obj.id,
            "res_model": cls._name,
            "active": True,
            "type": "binary",
            "partner_id": (
                obj.contract_id.counterparty_legal_id.id
                if obj.contract_id.counterparty_legal_id
                else None
            ),
            "folder_id": obj.contract_id.folder_id.id,
            "contract_id": obj.contract_id.id,
        }


class AlfaleadsLegalDomainsMixin(models.BaseModel):
    _name = "alfaleads_documents.legal_domains_mixin"
    _description = "Legal domains mixin"
    _abstract = True

    @api.model
    def _get_own_legal_domain(self):
        return self._get_domain_for_xml_id("alfaleads_crm.res_partner_type_own_legal")

    advisability_legal_id = fields.Many2one(
        comodel_name="res.partner",
        string="Own legal",
        domain=_get_own_legal_domain,
    )

    @api.model
    def _get_legal_domain(self):
        return self._get_domain_for_xml_id("alfaleads_crm.res_partner_type_legal")

    counterparty_legal_id = fields.Many2one(
        comodel_name="res.partner",
        string="Counterparty legal",
        domain=_get_legal_domain,
    )
    slang_id = fields.Many2one(
        comodel_name="res.partner",
        string="Slang",
        domain="[('id', 'in', slang_list_ids)]",
    )
    slang_list_ids = fields.Many2many(
        comodel_name="res.partner", compute="_get_available_advertisers"
    )

    @api.depends("counterparty_legal_id")
    def _get_available_advertisers(self):
        for rec in self:
            rec.slang_list_ids = rec.counterparty_legal_id.advertisers_ids

    def _get_domain_for_xml_id(self, xml_id):
        try:
            obj = self.env.ref(xml_id)
            return [("partner_type_id", "=", obj.id)]
        except ValueError:
            return []
