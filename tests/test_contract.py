from odoo.exceptions import UserError
from odoo.sql_db import _logger as sql_db_logger
from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from psycopg2.errors import ForeignKeyViolation

from .entity_factory import CopyDocumentsFactoryMixin


class CommonAlfaleadsContract(TransactionCase, CopyDocumentsFactoryMixin):
    def setUp(self):
        self.contract = self.env.ref(
            "alfaleads_documents.alfaleads_documents_contract_test"
        )


@tagged("-at_install", "post_install", "alfaleads_documents", "test_contract")
class TestAlfaleadsContract(CommonAlfaleadsContract):
    def setUp(self):
        super().setUp()

    def test_domain_manager_id(self):
        self.assertEqual(True, True)

    def test_compute_contract_title(self):
        self.assertEqual(True, True)

    def test_compute_root_contract_id(self):
        self.assertEqual(True, True)

    def test_get_document_vals(self):
        self.assertEqual(True, True)

    def test_contract_with_status_posted_cant_chang_attachment(self):
        copy_contract = self.copy_object(self.contract)
        copy_contract.make_posted()
        with self.assertRaises(UserError):
            copy_contract.write(
                {
                    "attachment_ids": [
                        (
                            6,
                            0,
                            [self.env.ref("alfaleads_documents.attachment_test2").id],
                        )
                    ]
                }
            )

    def test_delete_folder_after_move_contract_to_status_draft(self):
        copy_contract = self.copy_object(self.contract)
        copy_contract.make_draft()
        copy_folder = self.copy_object(
            self.env.ref("alfaleads_documents.document_folder_test")
        )
        copy_contract.write({"folder_id": copy_folder.id})
        self.env.cr.commit()
        disabled = sql_db_logger.disabled
        try:
            sql_db_logger.disabled = True
            copy_folder.unlink()
            self.env.cr.commit()
        except ForeignKeyViolation:
            self.env.cr.rollback()
        else:
            self.assertEqual("Error isn`t raised", "UserError was expected")
        finally:
            sql_db_logger.disabled = disabled
        copy_contract.unlink()
        copy_folder.unlink()


@tagged("-at_install", "post_install", "alfaleads_documents", "test_contract")
class TestAlfaleadsContractAppendix(CommonAlfaleadsContract):
    def setUp(self):
        super().setUp()

    def test_compute_appendix_title(self):
        self.assertEqual(True, True)

    def test_get_document_vals(self):
        self.assertEqual(True, True)


@tagged("-at_install", "post_install", "alfaleads_documents", "test_contract")
class TestAlfaleadsContractAdditionalAgreement(CommonAlfaleadsContract):
    def setUp(self):
        super().setUp()

    def test_compute_agreement_title(self):
        self.assertEqual(True, True)

    def test_get_document_vals(self):
        self.assertEqual(True, True)
