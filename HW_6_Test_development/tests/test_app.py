import unittest
from unittest import TestCase
from source.app import documents, directories
from source.app import check_document_existance, get_doc_owner_name, get_all_doc_owners_names
from source.app import remove_doc_from_shelf, add_new_shelf, delete_doc, get_doc_shelf, add_new_doc


class TestApp(TestCase):
    def setUp(self):
        self.true_user_doc_number = "10006"
        self.false_user_doc_number = "3924-02"
        self.true_shelf_number = '3'
        self.false_shelf_number = '5'

    def tearDown(self):
        pass

    def test_check_document_existance(self):
        true_result = check_document_existance(self.true_user_doc_number)
        false_result = check_document_existance(self.false_user_doc_number)
        self.assertTrue(true_result)
        self.assertFalse(false_result)

    def test_get_doc_owner_name(self):
        self.assertEqual("Аристарх Павлов", get_doc_owner_name(self.true_user_doc_number))
        # self.assertIsNone(get_doc_owner_name(self.false_user_doc_number))

    def test_get_all_doc_owners_names(self):
        owners_names_set = set(list(["Василий Гупкин", "Геннадий Покемонов", "Аристарх Павлов"]))
        self.assertSetEqual(owners_names_set, get_all_doc_owners_names())
        # self.assertRaises()

    def test_add_new_shelf(self):
        self.assertTupleEqual((self.true_shelf_number, False), add_new_shelf(self.true_shelf_number))
        self.assertTupleEqual((self.false_shelf_number, True), add_new_shelf(self.false_shelf_number))

    def test_delete_doc(self):
        self.assertTupleEqual((self.true_user_doc_number, True), delete_doc(self.true_user_doc_number))
        # self.assertIsNone(delete_doc(self.false_user_doc_number))

    def test_get_doc_shelf(self):
        self.assertEqual('2', get_doc_shelf(self.true_user_doc_number))
        # self.assertIsNone(get_doc_shelf(self.false_user_doc_number))

    def test_add_new_doc(self):
        pass
