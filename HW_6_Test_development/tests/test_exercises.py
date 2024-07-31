from unittest import TestCase, mock
from source.quadratic_equation import discriminant, solution
from source.votes import vote
from source.secretary_app import check_document_existance, get_doc_owner_name, get_doc_shelf, add_new_shelf, add_new_doc


class TestSecretaryApp(TestCase):
    def setUp(self):
        self.true_user_doc_number = "10006"
        self.false_user_doc_number = "3924-02"
        self.true_shelf_number = '3'
        self.false_shelf_number = '5'

    def tearDown(self):
        del self.true_user_doc_number
        del self.false_user_doc_number
        del self.true_shelf_number
        del self.false_shelf_number

    def test_check_document_existance(self):
        true_result = check_document_existance(self.true_user_doc_number)
        false_result = check_document_existance(self.false_user_doc_number)
        self.assertTrue(true_result)
        self.assertFalse(false_result)

    def test_get_doc_owner_name(self):
        self.assertMultiLineEqual("Аристарх Павлов", get_doc_owner_name(self.true_user_doc_number))
        self.assertIsNone(get_doc_owner_name(self.false_user_doc_number))

    def test_add_new_shelf(self):
        self.assertTupleEqual((self.true_shelf_number, False), add_new_shelf(self.true_shelf_number))
        self.assertTupleEqual((self.false_shelf_number, True), add_new_shelf(self.false_shelf_number))

    def test_get_doc_shelf(self):
        self.assertEqual('2', get_doc_shelf(self.true_user_doc_number))
        self.assertIsNone(get_doc_shelf(self.false_user_doc_number))

    @mock.patch('builtins.input', side_effect=("5455 028765", "driver license", "Василий Иванов", "4"))
    def test_add_new_doc(self, input):
        result = add_new_doc()
        expected = "4"
        self.assertEqual(expected, result)


class TestVotes(TestCase):
    def setUp(self):
        self.votes_list = ([1, 1, 1, 2, 3], [1, 2, 3, 2, 2], [],)
        self.expected_list = [1, 2, 0]

    def tearDown(self):
        del self.votes_list
        del self.expected_list

    def test_vote(self):
        for i, test_case in enumerate(self.votes_list):
            with self.subTest(i):
                self.assertEqual(self.expected_list[i], vote(test_case), msg=f"Test #{i+1} in vote function failed")


class TestQuadraticEquation(TestCase):
    def setUp(self):
        self.parameters_list = [(1, -2, 4), (-1, 2, 0), (1, 0, 0)]
        self.discrim_expected = [-12, 4, 0]
        self.solution_expected = [None, (0, 2), 0]

    def tearDown(self):
        del self.parameters_list
        del self.discrim_expected
        del self.solution_expected

    def test_discriminant(self):
        for i, (a, b, c) in enumerate(self.parameters_list):
            with self.subTest(i):
                self.assertEqual(self.discrim_expected[i], discriminant(a, b, c))

    def test_solution(self):
        for i, (a, b, c) in enumerate(self.parameters_list):
            with self.subTest(i):
                self.assertEqual(self.solution_expected[i], solution(a, b, c))
