from odoo.tests import tagged
from odoo.tests.common import TransactionCase


class CommonReference(TransactionCase):
    def setUp(self):
        pass


@tagged("-at_install", "post_install", "alfaleads_documents", "test_refs")
class TestBaseReference(CommonReference):
    def setUp(self):
        super().setUp()



@tagged("-at_install", "post_install", "alfaleads_documents", "test_refs")
class TestDocTypeReference(CommonReference):
    def setUp(self):
        super().setUp()




@tagged("-at_install", "post_install", "alfaleads_documents", "test_refs")
class TestTransferredToArchiveRef(CommonReference):
    def setUp(self):
        super().setUp()



@tagged("-at_install", "post_install", "alfaleads_documents", "test_refs")
class TestCounterpartyTypeRef(CommonReference):
    def setUp(self):
        super().setUp()
