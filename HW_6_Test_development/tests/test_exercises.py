from unittest import TestCase, mock
from source.quadratic_equation import discriminant, solution
from source.votes import vote
from source.secretary_app import check_document_existance, get_doc_owner_name, get_doc_shelf, add_new_shelf, add_new_doc


class TestSecretaryApp(TestCase):
    """
    Класс для тестирования "Секретаря" (secretary_app.py)
    """
    def setUp(self):
        """
        Setup метод. Настройка тестового окружения путем инициализации тестовых переменных.
        Этот метод инициализирует следующие переменные:
        - `true_user_doc_number`: строка, представляющая корректный номер документа пользователя.
        - `false_user_doc_number`: строка, представляющая некорректный номер документа пользователя.
        - `true_shelf_number`: строка, представляющая корректный номер полки.
        - `false_shelf_number`: строка, представляющая некорректный номер полки.
        Этот метод вызывается перед каждым выполнением тестового метода.
        """
        self.true_user_doc_number = "10006"
        self.false_user_doc_number = "3924-02"
        self.true_shelf_number = '3'
        self.false_shelf_number = '5'

    def tearDown(self):
        """
        Teardown метод. Удаляет атрибуты `true_user_doc_number`, `false_user_doc_number`,
        `true_shelf_number` и `false_shelf_number` из текущего экземпляра класса.
        Эта функция вызывается после выполнения каждого метода теста.
        """
        del self.true_user_doc_number
        del self.false_user_doc_number
        del self.true_shelf_number
        del self.false_shelf_number

    def test_check_document_existance(self):
        """
        Тестирование функции проверки существования документа (check_document_existance).
        Тестируются случаи с корректными и некорректными номерами документов пользователя.
        Проверяется, что функция возвращает True для корректных и False для некорректных номеров.
        """
        true_result = check_document_existance(self.true_user_doc_number)
        false_result = check_document_existance(self.false_user_doc_number)
        self.assertTrue(true_result)
        self.assertFalse(false_result)

    def test_get_doc_owner_name(self):
        """
        Тестирование функции получения имени владельца документа (`get_doc_owner_name`).
        Этот тестовый случай проверяет поведение функции `get_doc_owner_name`,
        проверяя, возвращает ли она правильное имя владельца для действительного номера документа
        и `None` для недействительного номера документа.
        """
        self.assertMultiLineEqual("Аристарх Павлов", get_doc_owner_name(self.true_user_doc_number))
        self.assertIsNone(get_doc_owner_name(self.false_user_doc_number))

    def test_add_new_shelf(self):
        """
        Тестирует функцию добавления новой полки (`add_new_shelf`). Тестируются случаи с корректными и
        некорректными номерами полок. Функция должна возвращать кортеж, содержащий номер полки и булево значение,
        указывающее, была ли полка успешно добавлена.
        """
        self.assertTupleEqual((self.true_shelf_number, False), add_new_shelf(self.true_shelf_number))
        self.assertTupleEqual((self.false_shelf_number, True), add_new_shelf(self.false_shelf_number))

    def test_get_doc_shelf(self):
        """
        Тестирование функции `get_doc_shelf`. Тестируется поведение функции при заданном действительном номере
        документа пользователя. Также проверяется поведение функции при заданном недействительном номере документа
        пользователя, ожидаемо сравнивая результат с `None`.
        """
        self.assertEqual('2', get_doc_shelf(self.true_user_doc_number))
        self.assertIsNone(get_doc_shelf(self.false_user_doc_number))

    @mock.patch('builtins.input', side_effect=("5455 028765", "driver license", "Василий Иванов", "4"))
    def test_add_new_doc(self, mock_input):
        """
        Тестирование функции добавления нового документа add_new_doc.
        Эта тестовая функция мокает функцию input, чтобы имитировать ввод данных пользователем во время выполнения
        функции add_new_doc. Затем вызывается функция add_new_doc, и результат сравнивается с ожидаемым значением
        (номером добавленной полки).
        Параметры:
            - mock_input: Мок функции input.
        """
        result = add_new_doc()
        expected = "4"
        self.assertEqual(expected, result)


class TestVotes(TestCase):
    """
    Класс для тестирования функции по подсчету победителя голосования vote.
    """
    def setUp(self):
        """
        Setup метод. Инициализирует атрибут votes_list кортежем списков, представляющих различные тестовые случаи
        для функции vote. Каждый список содержит последовательность голосов.
        Атрибут expected_list инициализируется списком ожидаемых результатов для каждого тестового случая.
        Ожидаемые результаты представляют собой победителя голосования большинства для каждого тестового случая.
        Метод вызывается перед каждым тестовым случаем.
        """
        self.votes_list = ([1, 1, 1, 2, 3], [1, 2, 3, 2, 2], [],)
        self.expected_list = [1, 2, 0]

    def tearDown(self):
        """
        Teardown метод. Удаляет атрибуты votes_list и expected_list из текущего экземпляра класса.
        Этот метод вызывается после выполнения каждого тестового случая.
        """
        del self.votes_list
        del self.expected_list

    def test_vote(self):
        """
        Тестирует функцию vote, перебирая список тестовых случаев и сравнивая ожидаемый и фактический результаты.
        Эта функция использует менеджер контекста subTest, чтобы запускать отдельные тестовые случаи.
        Она перебирает тестовые случаи и сравнивает результат выполнения функции vote с ожидаемым результатом.
        """
        for i, test_case in enumerate(self.votes_list):
            with self.subTest(i):
                self.assertEqual(self.expected_list[i], vote(test_case), msg=f"Test #{i+1} in vote function failed")


class TestQuadraticEquation(TestCase):
    """
    Класс для тестирования квадратичной функции.
    """
    def setUp(self):
        """
        Setup метод. Позволяет настроить тестовое окружение, инициализировав атрибуты parameters_list
        (список кортежей параметров a, b, c), discrim_expected (дискриминант функции) и соответствующие
        корни квадратичного уравнения solution_expected.
        """
        self.parameters_list = [(1, -2, 4), (-1, 2, 0), (1, 0, 0)]
        self.discrim_expected = [-12, 4, 0]
        self.solution_expected = [None, (0, 2), 0]

    def tearDown(self):
        """
        Teardown метод. Удаляет атрибуты parameters_list, discrim_expected и solution_expected.
        Этот метод вызывается после каждого тестового случая.
        """
        del self.parameters_list
        del self.discrim_expected
        del self.solution_expected

    def test_discriminant(self):
        """
        Тестирует функцию нахождения дискриминанта квадратного уравнения discriminant, итерируясь по списку
        тестовых наборов параметров a, b, c. Этот тест использует менеджер контекста subTest, чтобы запускать
        отдельные подтесты для каждого тестового случая. Сравнивает результат выполнения функции discriminant
        с ожидаемым результатом.
        """
        for i, (a, b, c) in enumerate(self.parameters_list):
            with self.subTest(i):
                self.assertEqual(self.discrim_expected[i], discriminant(a, b, c))

    def test_solution(self):
        """
        Тестирует функцию solution для вычисления корней квадратного уравнения, итерируясь по списку тестовых
        параметров a, b, c. Использует менеджер контекста subTest, чтобы запускать отдельные подтесты для
        каждого тестового случая. Сравнивает результат выполнения функции solition с ожидаемым результатом:
        None в случае отсутствия корней, кортеж корней уравнения в случае двух корней, 0 в случае одного корня.
        """
        for i, (a, b, c) in enumerate(self.parameters_list):
            with self.subTest(i):
                self.assertEqual(self.solution_expected[i], solution(a, b, c))
