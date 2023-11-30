# For details, see https://alfatech2020.atlassian.net/browse/OD-919


def migrate(cr, version):
    cr.execute(
        """
            DELETE FROM ir_model WHERE model in (
                'alfaleads_documents.contract',
                'alfaleads_documents.ref_doc_type',
                'alfaleads_documents.transferred_to_archive',
                'alfaleads_documents.counterparty_type',
                'alfaleads_documents.accounting_document',
                'alfaleads_documents.base_ref',
                'alfaleads_documents.transferred_to_archive',
                'alfaleads_documents.counterparty_type',
                'alfaleads_documents.add_agreement',
                'alfaleads_documents.appendix',
                'alfaleads_documents.draft_posted_mixin',
                'alfaleads_documents.attachment_mixin',
                'alfaleads_documents.contract_related_mixin',
                'alfaleads_documents.legal_domains_mixin',
                'alfaleads_documents.fill_status_mixin'
            );
            DELETE FROM ir_ui_view WHERE name in (
                'alfaleads_documents.view.form',
                'accounting.list',
                'alfaleads.documents.accounting_search',
                'alfaleads_documents.view.form',
                'contracts.list',
                'draft.contracts.list',
                'draft.contracts.search',
                'contracts.list.search',
                'contracts.search',
                'alfaleads.documents.contract_search',
                'alfaleads.res.partner.form',
                'alfaleads.document kanban',
                'alfaleads.document list',
                'alfaleads.documents.search',
                'base_ref.form',
                'base_ref.list',
                'ref_doc_type.form',
                'ref_doc_type.list',
                'transferred_to_archive.form',
                'transferred_to_archive.list',
                'counterparty_type.form',
                'counterparty_type.list'
            );
            DELETE FROM ir_model_access WHERE name like '%alfaleads_documents%';
            DELETE FROM ir_asset WHERE path in (
                '/alfaleads_documents/static/src/js/alfaleads_documents_search_panel_model_extension.js',
                '/alfaleads_documents/static/src/js/alfaleads_documents_documents_inspector.js',
                '/alfaleads_documents/static/src/js/ms_viewer_widget.js'
            );
            DROP TABLE IF EXISTS
                alfaleads_documents_accounting_document,
                alfaleads_documents_accounting_document_ir_attachment_rel,
                alfaleads_documents_add_agreement,
                alfaleads_documents_add_agreement_ir_attachment_rel,
                alfaleads_documents_appendix,
                alfaleads_documents_appendix_ir_attachment_rel,
                alfaleads_documents_base_ref,
                alfaleads_documents_contract,
                alfaleads_documents_contract_ir_attachment_rel,
                alfaleads_documents_counterparty_type,
                alfaleads_documents_ref_doc_type,
                alfaleads_documents_transferred_to_archive
            CASCADE;
        """
    )
