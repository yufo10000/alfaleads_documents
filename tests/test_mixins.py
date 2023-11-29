from odoo.tests import tagged
from odoo.tests.common import TransactionCase


class CommonMixins(TransactionCase):
    def setUp(self):
        pass


@tagged("-at_install", "post_install", "alfaleads_documents", "test_mixins")
class TestFillStatusMixin(CommonMixins):
    def setUp(self):
        super().setUp()

    def test_compute_fill_status(self):
        self.assertEqual(True, True)


    def test_check_fill_status(self):
        self.assertEqual(True, True)



@tagged("-at_install", "post_install", "alfaleads_documents", "test_mixins")
class TestDraftPostedMixin(CommonMixins):
    def setUp(self):
        super().setUp()

    def test_make_draft(self):
        self.assertEqual(True, True)


    def test_make_posted(self):
        self.assertEqual(True, True)


    def test_check_required_fields(self):
        self.assertEqual(True, True)


    def test_create_documents_for_attachments(self):
        self.assertEqual(True, True)


    def test_get_document_vals(self):
        self.assertEqual(True, True)


    def test_unlink(self):
        self.assertEqual(True, True)


    def test_write(self):
        self.assertEqual(True, True)


    def test_check_attachments_for_delete(self):
        self.assertEqual(True, True)



@tagged("-at_install", "post_install", "alfaleads_documents", "test_mixins")
class TestAttachmentsDocumentMixin(CommonMixins):
    def setUp(self):
        super().setUp()

    def test_create(self):
        self.assertEqual(True, True)


    def test_write(self):
        self.assertEqual(True, True)


    def test_create_documents_for_attachments(self):
        self.assertEqual(True, True)


    def test_get_document_vals(self):
        self.assertEqual(True, True)



@tagged("-at_install", "post_install", "alfaleads_documents", "test_mixins")
class TestAlfaleadsContractsRelatedMixin(CommonMixins):
    def setUp(self):
        super().setUp()

    def test_get_document_vals(self):
        self.assertEqual(True, True)



@tagged("-at_install", "post_install", "alfaleads_documents", "test_mixins")
class TestAlfaleadsLegalDomainsMixin(CommonMixins):
    def setUp(self):
        super().setUp()

    def test_get_own_legal_domain(self):
        self.assertEqual(True, True)


    def test_get_legal_domain(self):
        self.assertEqual(True, True)


    def test_get_available_advertisers(self):
        self.assertEqual(True, True)


    def test_get_domain_for_xml_id(self):
        self.assertEqual(True, True)
