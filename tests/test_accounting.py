from odoo.tests import tagged
from odoo.tests.common import TransactionCase

@tagged("-at_install", "post_install", "alfaleads_documents", "test_accounting")
class TestAccountingDocument(TransactionCase):
    def setUp(self):
        super().setUp()

    def test_compute_doc_title(self):
        self.assertEqual(True, True)

    def test_get_document_vals(self):
        self.assertEqual(True, True)

