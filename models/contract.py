# -*- coding: utf-8 -*-

from datetime import date

from odoo import api, fields, models

from .mixins import ACTIVITY_STATUS_SELECTION


class AlfaleadsContract(models.Model):
    _inherit = [
        "alfaleads_documents.fill_status_mixin",
        "alfaleads_documents.legal_domains_mixin",
        "alfaleads_documents.draft_posted_mixin",
        "alfaleads_utils.uuid_mixin",
        "alfaleads_utils.rewrite_res_id_on_create_after_attachment_mixin",
    ]
    _name = "alfaleads_documents.contract"
    _description = "Contract"

    _fill_status_required_fields = [
        "slang_id",
        "advisability_legal_id",
        "counterparty_legal_id",
        "contract_details",
        "subject",
        "amount",
        "currency_id",
        "payment_term",
        "date_start",
        "transferred_to_archive_id",
        "manager_id",
        "department_id",
        "attachment_ids",
    ]

    POSTED_REQUIRED_FIELDS = [
        "reg_number",
        "reg_date",
        "advisability_legal_id",
        "counterparty_legal_id",
        "counterparty_type_id",
        "contract_details",
        "folder_id",
        "attachment_ids",
    ]

    @api.model
    def _domain_manager_id(self):
        """
        Domain for manager_id field
        """
        return [
            (
                "partner_type_id",
                "=",
                self.env.ref("alfaleads_crm.res_partner_type_manager").id,
            )
        ]

    document_ids = fields.One2many(
        comodel_name="documents.document",
        string="Documents",
        inverse_name="contract_id",
    )

    name = fields.Char(
        "Contract title",
        compute="_compute_contract_title",
        store=True,
    )
    reg_number = fields.Char("Reg No.", states={"posted": [("readonly", True)]})
    reg_date = fields.Date("Reg date", states={"posted": [("readonly", True)]})

    accounting_ids = fields.One2many(
        comodel_name="alfaleads_documents.accounting_document",
        string="Accounting documents",
        inverse_name="contract_id",
    )
    activity_status = fields.Selection(
        selection=ACTIVITY_STATUS_SELECTION,
        string="Activity status",
        default="in_progress",
    )
    advisability_legal_id = fields.Many2one(states={"posted": [("readonly", True)]})
    counterparty_legal_id = fields.Many2one(
        "res.partner",
        string="Contract Counterparty legal",
        states={"posted": [("readonly", True)]},
    )
    counterparty_country_id = fields.Many2one(
        "res.country",
        string="Counterparty country",
        states={"posted": [("readonly", True)]},
    )
    counterparty_type_id = fields.Many2one(
        "alfaleads_documents.counterparty_type",
        string="Counterparty type",
        states={"posted": [("readonly", True)]},
    )
    slang_id = fields.Many2one(states={"posted": [("readonly", True)]})
    contract_details = fields.Text(
        "Contract name", states={"posted": [("readonly", True)]}
    )
    subject = fields.Text("Subject")
    amount = fields.Monetary(
        "Amount", currency_field="currency_id", states={"posted": [("readonly", True)]}
    )
    currency_id = fields.Many2one(
        "res.currency", string="Currency", states={"posted": [("readonly", True)]}
    )
    payment_term = fields.Text("Payment term")
    date_start = fields.Date(
        "Contract period from", states={"posted": [("readonly", True)]}
    )
    date_end = fields.Date(
        "Contract period until", states={"posted": [("readonly", True)]}
    )
    open_ended = fields.Boolean(
        "Open-ended contract", default=False, states={"posted": [("readonly", True)]}
    )
    transferred_to_archive_id = fields.Many2one(
        "alfaleads_documents.transferred_to_archive",
        string="Transferred to archive",
        states={"posted": [("readonly", True)]},
    )
    comment = fields.Text("Comment")
    manager_id = fields.Many2one(
        "res.partner", domain=_domain_manager_id, string="User manager"
    )
    department_id = fields.Many2one(
        comodel_name="affise.department", string="Department"
    )
    attachment_ids = fields.Many2many(
        comodel_name="ir.attachment",
        string="Attachments",
        states={"posted": [("readonly", True)]},
    )

    folder_id = fields.Many2one(
        "documents.folder",
        string="Workspace",
        ondelete="restrict",
        index=True,
        states={"posted": [("readonly", True)]},
    )

    contract_folder_path = fields.Char("Full Path", related="folder_id.full_path")
    appendix_ids = fields.One2many(
        comodel_name="alfaleads_documents.appendix",
        inverse_name="contract_id",
        string="Appendix",
    )
    add_agreement_ids = fields.One2many(
        comodel_name="alfaleads_documents.add_agreement",
        inverse_name="contract_id",
        string="Additional Agreement",
    )

    @api.depends("reg_number", "reg_date")
    def _compute_contract_title(self):
        for record in self:
            contract_num = (
                f"No. {record.reg_number}" if record.reg_number else f"ID {record.id}"
            )
            contract_date = f" dated {record.reg_date}" if record.reg_date else ""
            record.name = f"{contract_num}{contract_date}"

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
            "contract_id": obj.id,
        }

    @api.onchange("open_ended")
    def _onchange_open_ended(self):
        if self.open_ended:
            self.date_end = date(9999, 11, 30)
        else:
            self.date_end = False


class AlfaleadsContractAppendix(models.Model):
    _inherit = [
        "alfaleads_documents.fill_status_mixin",
        "alfaleads_documents.contract_related_mixin",
        "alfaleads_documents.draft_posted_mixin",
        "alfaleads_utils.rewrite_res_id_on_create_after_attachment_mixin",
    ]
    _name = "alfaleads_documents.appendix"
    _description = "Contract Appendix"

    _fill_status_required_fields = [
        "amount",
        "currency_id",
        "payment_term",
        "attachment_ids",
    ]

    POSTED_REQUIRED_FIELDS = [
        "attachment_ids",
        "contract_id",
    ]

    document_ids = fields.One2many(
        comodel_name="documents.document",
        string="Documents",
        inverse_name="contract_appendix_id",
    )

    name = fields.Char("Name", compute="_compute_appendix_title")
    appendix_no = fields.Char("Appendix No.")
    appendix_date = fields.Date("Appendix date")
    contract_id = fields.Many2one(
        "alfaleads_documents.contract",
        string="Contract",
        ondelete="restrict",
    )
    agreement_id = fields.Many2one(
        "alfaleads_documents.add_agreement",
        string="Additional agreement",
        domain="[('contract_id', '=', contract_id)]",
    )
    activity_status = fields.Selection(related="contract_id.activity_status")
    amount = fields.Monetary("Amount", currency_field="currency_id")
    currency_id = fields.Many2one("res.currency", string="Currency")
    payment_term = fields.Text("Payment term")
    comment = fields.Text("Appendix comment")
    attachment_ids = fields.Many2many(
        comodel_name="ir.attachment",
        string="Attachments",
    )

    appendix_name = fields.Char("Appendix name")

    @api.depends("appendix_no")
    def _compute_appendix_title(self):
        for record in self:
            record.name = (
                f"Appendix {record.appendix_no}"
                if record.appendix_no
                else f"Appendix ID {record.id}"
            )

    @classmethod
    def _get_document_vals(cls, obj, attachment):
        res = super()._get_document_vals(obj, attachment)
        res["contract_appendix_id"] = obj.id
        return res


class AlfaleadsContractAdditionalAgreement(models.Model):
    _inherit = [
        "alfaleads_documents.fill_status_mixin",
        "alfaleads_documents.contract_related_mixin",
        "alfaleads_documents.draft_posted_mixin",
        "alfaleads_utils.rewrite_res_id_on_create_after_attachment_mixin",
    ]
    _name = "alfaleads_documents.add_agreement"
    _description = "Additional agreement"

    _fill_status_required_fields = [
        "amount",
        "currency_id",
        "payment_term",
        "attachment_ids",
    ]

    POSTED_REQUIRED_FIELDS = [
        "attachment_ids",
        "contract_id",
    ]

    document_ids = fields.One2many(
        comodel_name="documents.document",
        string="Documents",
        inverse_name="contract_add_agreement_id",
    )

    contract_id = fields.Many2one(
        "alfaleads_documents.contract",
        string="Contract",
        ondelete="restrict",
    )
    name = fields.Char("Name", compute="_compute_agreement_title")
    agreement_no = fields.Char("Agreement No.")
    agreement_date = fields.Date("Agreement date")
    activity_status = fields.Selection(related="contract_id.activity_status")
    counterparty_type_id = fields.Many2one(related="contract_id.counterparty_type_id")
    counterparty_legal_id = fields.Many2one(related="contract_id.counterparty_legal_id")

    amount = fields.Monetary("Amount", currency_field="currency_id")
    currency_id = fields.Many2one("res.currency", string="Currency")
    payment_term = fields.Text("Payment term")
    comment = fields.Text("Agreement comment")
    attachment_ids = fields.Many2many(
        comodel_name="ir.attachment",
        string="Attachments",
    )

    agreement_name = fields.Char("Agreement name")

    @api.depends("agreement_no", "agreement_date")
    def _compute_agreement_title(self):
        for record in self:
            num = (
                f"No. {record.agreement_no}"
                if record.agreement_no
                else f"ID {record.id}"
            )
            date = f" dated {record.agreement_date}" if record.agreement_date else ""
            record.name = f"{num}{date}"

    @classmethod
    def _get_document_vals(cls, obj, attachment):
        res = super()._get_document_vals(obj, attachment)
        res["contract_add_agreement_id"] = obj.id
        return res
