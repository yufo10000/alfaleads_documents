{
    "name": "Alfaleads documents",
    "summary": """
        Alfaleads extension to Documents
    """,
    "author": "Roman Marchenko",
    "category": "Productivity/Documents",
    "license": "AGPL-3",
    "application": True,
    "version": "16.0.1.1",
    "depends": ["documents", "web", "alfaleads_crm", "alfaleads_utils"],
    "data": [
        # DATA
        "data/document_types_data.xml",
        # SECURITY
        "security/security.xml",
        "security/ir.model.access.csv",
        # VIEWS
        "views/templates.xml",
        "views/documents_views.xml",
        "views/res_partner_views.xml",
        "views/contracts_view.xml",
        "views/refs_views.xml",
        "views/accounting_views.xml",
    ],
    "demo": [
        "demo/documents.folder.csv",
        "demo/documents.document.csv",
        "demo/ir.attachment.csv",
        "demo/alfaleads_documents.counterparty_type.csv",
        "demo/res.partner.csv",
        "demo/alfaleads_documents.transferred_to_archive.csv",
        "demo/alfaleads_documents.contract.csv",
    ],
    "assets": {
        "web.assets_backend": [
            "alfaleads_documents/static/src/xml/tree_view_buttons.xml",
            "alfaleads_documents/static/src/js/documents_list.js",
            "alfaleads_documents/static/src/js/alfaleads_documents_search_panel_model_extension.js",
            "alfaleads_documents/static/src/js/alfaleads_documents_documents_inspector.js",
            "alfaleads_documents/static/src/js/ms_viewer_widget.js",
        ],
        "web.assets_qweb": [
            "alfaleads_documents/static/src/xml/search_panel.xml",
            "alfaleads_documents/static/src/xml/documents_inspector.xml",
        ],
    },
}
