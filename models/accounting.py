from odoo import api, fields, models


class AccountingDocument(models.Model):
    _inherit = [
        "alfaleads_documents.fill_status_mixin",
        "alfaleads_documents.attachment_mixin",
        "alfaleads_documents.legal_domains_mixin",
        "alfaleads_utils.rewrite_res_id_on_create_after_attachment_mixin",
    ]
    _name = "alfaleads_documents.accounting_document"
    _description = "Accounting documents"

    _fill_status_required_fields = [
        "document_type_id",
        "document_date",
        "counterparty_legal_id",
        "slang_id",
        "transferred_to_archive_id",
        "advisability_legal_id",
    ]

    document_ids = fields.One2many(
        comodel_name="documents.document",
        string="Documents",
        inverse_name="accounting_id",
    )

    name = fields.Char("Document title", compute="_compute_doc_title")
    counterparty_legal_id = fields.Many2one(string="Accounting Counterparty legal")
    contract_id = fields.Many2one(
        "alfaleads_documents.contract",
        string="Related Contract",
        domain="""[
                ('state', 'in', ['posted']),
                ('counterparty_legal_id', '=', counterparty_legal_id),
                ('counterparty_legal_id', '!=', None)
            ]""",
        ondelete="restrict",
    )
    document_type_id = fields.Many2one(
        "alfaleads_documents.ref_doc_type", required=True
    )
    document_no = fields.Char("Document No.")
    document_date = fields.Date("Document date", required=True)
    transferred_to_archive_id = fields.Many2one(
        "alfaleads_documents.transferred_to_archive", string="Transferred to archive"
    )
    comment = fields.Text("Comment")
    folder_id = fields.Many2one(
        "documents.folder",
        string="Workspace",
        ondelete="restrict",
        required=True,
        index=True,
    )
    attachment_ids = fields.Many2many(
        comodel_name="ir.attachment",
        string="Attachments",
        required=True,
    )

    @api.depends("document_type_id.name", "document_date", "document_no")
    def _compute_doc_title(self):
        for record in self:
            doc_no = f" No {record.document_no}" if record.document_no else ""
            record.name = (
                f"{record.document_type_id.name}{doc_no} dated {record.document_date}"
            )

    @classmethod
    def _get_document_vals(cls, obj, attachment):
        return {
            "attachment_id": attachment.id,
            "res_id": obj.id,
            "res_model": cls._name,
            "active": True,
            "type": "binary",
            "partner_id": obj.counterparty_legal_id.id
            if obj.counterparty_legal_id
            else None,
            "folder_id": obj.folder_id.id,
            "accounting_id": obj.id,
        }

    @api.onchange("counterparty_legal_id")
    def _onchange_counterparty_legal_id(self):
        self.contract_id = False
