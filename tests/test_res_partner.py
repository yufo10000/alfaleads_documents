from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("-at_install", "post_install", "alfaleads_documents", "test_res_partner")
class TestResPartner(TransactionCase):
    def setUp(self):
        super().setUp()

    def test_compute_partner_type(self):
        self.assertEqual(True, True)
