from odoo import fields, models


class BaseReference(models.Model):
    _name = "alfaleads_documents.base_ref"
    _description = "Base reference document model"
    _inherit = [
        "alfaleads_utils.base_ref",
    ]

    folder_id = fields.Many2one(
        "documents.folder",
        string="Workspace",
        ondelete="restrict",
        index=True,
    )


class DocTypeReference(models.Model):
    _name = "alfaleads_documents.ref_doc_type"
    _inherit = [
        "alfaleads_documents.base_ref",
    ]
    _description = "Document types"


class TransferredToArchiveRef(models.Model):
    _name = "alfaleads_documents.transferred_to_archive"
    _inherit = [
        "alfaleads_documents.base_ref",
    ]
    _description = "Transferred to archive values"


class CounterpartyTypeRef(models.Model):
    _name = "alfaleads_documents.counterparty_type"
    _inherit = [
        "alfaleads_documents.base_ref",
    ]
    _description = "Counterparty type"
