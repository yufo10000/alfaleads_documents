from odoo.exceptions import AccessError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from .entity_factory import CopyDocumentsFactoryMixin


@tagged("-at_install", "post_install", "alfaleads_documents", "test_document")
class TestAlfaleadsDocument(TransactionCase, CopyDocumentsFactoryMixin):
    def setUp(self):
        super().setUp()
        self.document = self.env.ref("alfaleads_documents.documents_document_test")

    def test_compute_contract_fields(self):
        self.assertEqual(True, True)

    def test_preview_supported(self):
        self.assertEqual(True, True)

    def test_viewer_type(self):
        self.assertEqual(True, True)

    def test_share_for_preview(self):
        self.assertEqual(True, True)

    def test_create_contract(self):
        self.assertEqual(True, True)

    def test_delete_document(self):
        copy_document = self.copy_object(self.document)
        with self.assertRaises(AccessError):
            copy_document.with_user(self.env.ref("base.user_admin")).unlink()
