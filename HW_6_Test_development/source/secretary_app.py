documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
    {"type": "driver license", "number": "5455 028765", "name": "Василий Иванов"},
]

directories = {
    '1': ['2207 876234', '11-2', '5455 028765'],
    '2': ['10006'],
    '3': []
}


def check_document_existance(user_doc_number):
    """
    Функция проверки существования документа
    Параметры: user_doc_number (string)
    Возвращает: True - если документ существует, False - если нет
    """
    doc_founded = False
    for current_document in documents:
        doc_number = current_document['number']
        if doc_number == user_doc_number:
            doc_founded = True
            break
    return doc_founded


def get_doc_owner_name(user_doc_number):
    """
    Функция возвращает имя владельца документа по его номеру
    Параметры: номер документа user_doc_number (string)
    Возращает: имя владельца документа (string), если документ не найден, возвращает None
    """
    doc_exist = check_document_existance(user_doc_number)
    if doc_exist:
        for current_document in documents:
            doc_number = current_document['number']
            if doc_number == user_doc_number:
                return current_document['name']


def get_doc_shelf(user_doc_number):
    """
    Функция возвращает полку, на которой хранится документ с заданным номером
    Параметры: номер документа user_doc_number (string)
    Возращает: полку, на которой хранится документ (string) если документ не найден, возвращает None
    """
    doc_exist = check_document_existance(user_doc_number)
    if doc_exist:
        for directory_number, directory_docs_list in directories.items():
            if user_doc_number in directory_docs_list:
                return directory_number


def add_new_shelf(shelf_number=''):
    """
    Функция добавления новой полки
    Параметры: номер полки shelf_number (string)
    Возвращает: кортеж с номером полки(string) и True, если полка добавлена, иначе False
    Создает новую полку в случае, если ее не существует
    """
    if not shelf_number:
        shelf_number = input('Введите номер полки - ')
    if shelf_number not in directories.keys():
        directories[shelf_number] = []
        return shelf_number, True
    return shelf_number, False


def append_doc_to_shelf(doc_number, shelf_number):
    """
    Функция добавления документа в полку
    Параметры: номер документа doc_number (string), номер полки shelf_number (string)
    Возвращает: None
    """
    add_new_shelf(shelf_number)
    directories[shelf_number].append(doc_number)


def add_new_doc():
    """
    Функция добавления нового документа по введенным номеру документа, типу документа,
    имени владельца и номеру полки.
    Возвращает: номер полки (string)
    """
    new_doc_number = input('Введите номер документа - ')
    new_doc_type = input('Введите тип документа - ')
    new_doc_owner_name = input('Введите имя владельца документа - ')
    new_doc_shelf_number = input('Введите номер полки для хранения - ')
    new_doc = {
        "type": new_doc_type,
        "number": new_doc_number,
        "name": new_doc_owner_name
    }
    documents.append(new_doc)
    append_doc_to_shelf(new_doc_number, new_doc_shelf_number)
    return new_doc_shelf_number
