# -*- coding: utf-8 -*-
import datetime
import logging

from odoo import api, fields, models

from .mixins import ACTIVITY_STATUS_SELECTION, FILL_STATUS_SELECTION

logger = logging.getLogger(__name__)

SUPPORTED_MIMETYPES = {
    # Word
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "office.live",
    "application/msword": "office.live",
    "application/rtf": "office.live",
    # Excel
    "application/vnd.ms-excel": "office.live",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "office.live",
    "text/csv": "office.live",
    # PDF
    "application/pdf": "pdfjs",
}


class AlfaleadsDocument(models.Model):
    _inherit = "documents.document"

    preview_supported = fields.Boolean(
        "Preview supported", compute="_preview_supported"
    )
    viewer_type = fields.Char("Viewer type", compute="_viewer_type")
    partner_id = fields.Many2one(string="A.D. Counterparty legal")

    #  Contract relation section
    contract_id = fields.Many2one(
        "alfaleads_documents.contract", string="Contracts", ondelete="cascade"
    )
    contract_appendix_id = fields.Many2one(
        "alfaleads_documents.appendix", string="Appendix", ondelete="cascade"
    )
    contract_add_agreement_id = fields.Many2one(
        "alfaleads_documents.add_agreement", string="Agreement", ondelete="cascade"
    )

    contracts_fill_status = fields.Selection(
        selection=FILL_STATUS_SELECTION,
        compute="_compute_contract_fields",
        string="Fill status",
        compute_sudo=True,
    )

    # contracts filters special section
    contract_reg_date = fields.Date(
        related="contract_id.reg_date", string="Contract Reg Date"
    )
    contract_reg_no = fields.Char(
        related="contract_id.reg_number", string="Contract Reg No"
    )
    contract_manager_name = fields.Char(
        related="contract_id.manager_id.name", string="Manager  User"
    )
    contract_department_name = fields.Char(
        related="contract_id.department_id.name", string="Department"
    )
    contract_activity_status = fields.Selection(
        related="contract_id.activity_status",
        string="Contract activity status",
    )
    contract_counterparty_type_id = fields.Many2one(
        related="contract_id.counterparty_type_id", string="Contract counterparty type"
    )
    contract_own_legal_name = fields.Char(
        related="contract_id.advisability_legal_id.name", string="Own legal name"
    )
    contract_slang_name = fields.Char(
        related="contract_id.slang_id.name", string="Slang name"
    )
    contract_transferred_to_archive_name = fields.Char(
        related="contract_id.transferred_to_archive_id.name",
        string="Transferred to archive name",
    )
    contract_period_from = fields.Date(related="contract_id.date_start")
    contract_period_until = fields.Date(related="contract_id.date_end")
    contract_open_ended = fields.Boolean(related="contract_id.open_ended")
    contract_counterparty_country_name = fields.Char(
        related="contract_id.counterparty_country_id.name"
    )
    contract_name = fields.Text(related="contract_id.contract_details")
    # end fo contracts filters special section

    contracts_payment_term = fields.Char(
        "Payment term",
        compute="_compute_contract_fields",
        compute_sudo=True,
    )
    contracts_counterparty_legal_id = fields.Many2one(
        comodel_name="res.partner",
        compute="_compute_contract_fields",
        string="Legal",
        store=True,
        compute_sudo=True,
    )
    contracts_counterparty_type_id = fields.Many2one(
        comodel_name="alfaleads_documents.counterparty_type",
        compute="_compute_contract_fields",
        string="Counterparty type",
        compute_sudo=True,
    )
    contracts_activity_status = fields.Selection(
        selection=ACTIVITY_STATUS_SELECTION,
        compute="_compute_contract_fields",
        string="Activity status",
        compute_sudo=True,
    )
    contracts_slang_id = fields.Many2one(
        "res.partner",
        compute="_compute_contract_fields",
        string="Slang",
        compute_sudo=True,
    )
    contracts_comment = fields.Text(
        compute="_compute_contract_fields",
        string="Comment",
        compute_sudo=True,
    )
    #  end of Contract relation section

    #  Accounting relation section
    accounting_id = fields.Many2one(
        "alfaleads_documents.accounting_document",
        string="Accounting documents",
        ondelete="cascade",
    )
    acc_contract_id_name = fields.Char(related="acc_contract_id.name")
    acc_document_type_id = fields.Many2one(related="accounting_id.document_type_id")
    acc_document_no = fields.Char(related="accounting_id.document_no")
    acc_document_date = fields.Date(related="accounting_id.document_date")
    acc_counterparty_legal_id = fields.Many2one(
        related="accounting_id.counterparty_legal_id"
    )
    acc_slang_id = fields.Many2one(
        related="accounting_id.slang_id", string="Accounting slang"
    )
    acc_transferred_to_archive_id = fields.Many2one(
        related="accounting_id.transferred_to_archive_id"
    )
    acc_advisability_legal_id = fields.Many2one(
        related="accounting_id.advisability_legal_id"
    )
    acc_comment = fields.Text(
        related="accounting_id.comment", string="Accounting comment"
    )
    acc_fill_status = fields.Selection(
        related="accounting_id.fill_status", string="Accounting fill status"
    )
    acc_contract_id = fields.Many2one(related="accounting_id.contract_id")
    acc_contract_title = fields.Char(
        related="accounting_id.contract_id.reg_number", string="Contract No."
    )
    #  end of Accounting relation section

    def unlink(self):
        return models.BaseModel.unlink(self)

    def _compute_contract_fields(self):
        for rec in self:
            if rec.res_model == "alfaleads_documents.contract" and rec.contract_id:
                rec.contracts_fill_status = rec.contract_id.fill_status
                rec.contracts_activity_status = rec.contract_id.activity_status
                rec.contracts_payment_term = rec.contract_id.payment_term
                rec.contracts_counterparty_type_id = (
                    rec.contract_id.counterparty_type_id
                )
                rec.contracts_counterparty_legal_id = (
                    rec.contract_id.counterparty_legal_id
                )
                rec.contracts_slang_id = rec.contract_id.slang_id
                rec.contracts_comment = rec.contract_id.comment
            elif (
                rec.res_model == "alfaleads_documents.appendix"
                and rec.contract_appendix_id
            ):
                rec.contracts_fill_status = rec.contract_appendix_id.fill_status
                rec.contracts_activity_status = (
                    rec.contract_appendix_id.contract_id.activity_status
                )
                rec.contracts_payment_term = rec.contract_appendix_id.payment_term
                rec.contracts_counterparty_type_id = (
                    rec.contract_appendix_id.contract_id.counterparty_type_id
                )
                rec.contracts_counterparty_legal_id = (
                    rec.contract_appendix_id.contract_id.counterparty_legal_id
                )
                rec.contracts_slang_id = rec.contract_appendix_id.contract_id.slang_id
                rec.contracts_comment = rec.contract_appendix_id.comment
            elif (
                rec.res_model == "alfaleads_documents.add_agreement"
                and rec.contract_add_agreement_id
            ):
                rec.contracts_fill_status = rec.contract_add_agreement_id.fill_status
                rec.contracts_activity_status = (
                    rec.contract_add_agreement_id.contract_id.activity_status
                )
                rec.contracts_payment_term = rec.contract_add_agreement_id.payment_term
                rec.contracts_counterparty_type_id = (
                    rec.contract_add_agreement_id.contract_id.counterparty_type_id
                )
                rec.contracts_counterparty_legal_id = (
                    rec.contract_add_agreement_id.contract_id.counterparty_legal_id
                )
                rec.contracts_slang_id = (
                    rec.contract_add_agreement_id.contract_id.slang_id
                )
                rec.contracts_comment = rec.contract_add_agreement_id.comment
            else:
                rec.contracts_fill_status = ""
                rec.contracts_activity_status = ""
                rec.contracts_payment_term = ""
                rec.contracts_counterparty_type_id = None
                rec.contracts_counterparty_legal_id = None
                rec.contracts_slang_id = None
                rec.contracts_comment = ""

    @api.depends("mimetype")
    def _preview_supported(self):
        for record in self:
            record.preview_supported = record.mimetype in SUPPORTED_MIMETYPES

    @api.depends("mimetype")
    def _viewer_type(self):
        for record in self:
            record.viewer_type = SUPPORTED_MIMETYPES.get(record.mimetype, "")

    @api.model
    def share_for_preview(self, doc_id, folder_id):
        tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).date()
        vals = {
            "type": "ids",
            "document_ids": [
                (
                    6,
                    0,
                    [
                        doc_id,
                    ],
                )
            ],
            "folder_id": folder_id,
            "date_deadline": tomorrow,
        }
        share = self.env["documents.share"].create(vals)
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        return (
            f"{base_url}/document/tmp_preview/{share.id}/{share.access_token}/{doc_id}"
        )

    @api.model
    def create_contract(self):
        create_view_id = self.env.ref("alfaleads_documents_contract_view_form").id
        return {
            "name": "Create contract",
            "type": "ir.actions.act_window",
            "res_model": "alfaleads_documents.contract",
            "view_mode": "from",
            "views": [(create_view_id, "form")],
            "res_id": False,
            "target": "new",
        }
