import requests
import time
from urllib.parse import urljoin
from settings.config import BASE_URL, MAIN_PARAMS, HEADERS, KEYWORDS
from http import HTTPStatus
from bs4 import BeautifulSoup
import json


def get_html_content(url: str, headers=None, params=None) -> str:
    """
    Извлекает HTML-содержимое по заданному URL.
    Параметры:
        url (str): URL, из которого извлекается HTML-содержимое.
        headers (dict): Дополнительные заголовки запроса.
        params (dict): Query-параметры запроса.
    Возвращает:
        str: Извлеченное HTML-содержимое.
    Выбрасывает:
        Exception: Если возникает ошибка при извлечении HTML-содержимого.
    """
    html_content = ''
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == HTTPStatus.OK:
            response.encoding = 'UTF-8'
            html_content = response.text
    except Exception as error:
        print(f"{error} while getting html content")
    return html_content


def get_vacancies_cards(content: str) -> list[dict]:
    """
    Парсит HTML-содержимое для извлечения информации о вакансиях и возвращает список словарей,
    содержащих иформацию о вакансиях.
    Параметры:
        content: HTML-содержимое для парсинга.
    Возвращает:
        Список словарей, содержащих детали вакансий. Каждый словарь имеет следующие ключи:
           'title' (str): Название вакансии.
           'salary' (str или None): Заработная плата вакансии. None если отсутствует.
           'company' (str): Название компании.
           'location' (str): Местоположение вакансии (город).
           'link' (str): Ссылка на страницу вакансии.
    Исключения:
        AttributeError: Если не удается найти какие-либо теги в HTML-содержимом.
        Exception: Если происходит любое другое исключение.
    """
    soup = BeautifulSoup(content, 'lxml')
    page_cards = []
    vacancies_main_block = soup.find('main', attrs={'class': 'vacancy-serp-content'})
    page_vacancies = vacancies_main_block.find('div', attrs={'id': 'a11y-main-content'})
    vacancies_cards = page_vacancies.find_all('div', attrs={'class': 'vacancy-card--z_UXteNo7bRGzxWVcL7y'})
    for card in vacancies_cards:
        try:
            vacancy_title_block = card.find('h2', attrs={'class': 'bloko-header-section-2'})
            link_block = vacancy_title_block.find('a', attrs={'class': 'bloko-link'})
            vacancy_compensation_block = card.find('div', attrs={'class': 'compensation-labels--uUto71l5gcnhU2I8TZmz'})
            salary_block = vacancy_compensation_block.find('span', attrs={'class': 'bloko-text'})
            vacancy_info_block = card.find('div', attrs={'class': 'info-section--N695JG77kqwzxWAnSePt'})
            vacancy_title = vacancy_title_block.text
            vacancy_link = link_block['href']
            vacancy_salary = str(salary_block.text) if salary_block else None
            if vacancy_salary:
                vacancy_salary = vacancy_salary.replace('\u202f', ' ').replace('\xa0', ' ')
            company_name = str(vacancy_info_block.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text)
            company_name = company_name.replace('\xa0', ' ')
            vacancy_location = vacancy_info_block.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
        except AttributeError:
            print(f"Error. Can't find tag by attrs. Skipping...")
            continue
        except Exception as e:
            print(f"Error: {e}. Skipping...")
            continue
        page_cards.append({
            'title': vacancy_title,
            'salary': vacancy_salary,
            'company': company_name,
            'location': vacancy_location,
            'link': vacancy_link
        })
    return page_cards


def get_next_page_link(page_url: str, headers: dict = None):
    """
    Получает ссылку на следующую страницу на основе предоставленного URL страницы и необязательных заголовков.
    Параметры:
        page_url: URL текущей страницы.
        headers: Заголовки для включения в запрос. По умолчанию None.
    Возвращает:
        str: URL следующей страницы. Пустая строка, если ссылка на следующую страницу не найдена.
    """
    page_content = get_html_content(page_url, headers)
    next_page_link = ''
    soup = BeautifulSoup(page_content, 'lxml')
    try:
        vacancies_main_block = soup.find('main', attrs={'class': 'vacancy-serp-content'})
        pager_block = vacancies_main_block.find('div', attrs={'class': 'pager'})
        next_page_block = pager_block.find('a', attrs={'data-qa': 'pager-next'})
        next_page_link = urljoin('https://spb.hh.ru/', next_page_block['href'])
    except AttributeError:
        print(f"Error. Can't find tag by attrs")
    return next_page_link


def get_vacancies_by_pages(start_page_url: str, pages_num: int = 1, headers=None, params=None):
    """
    Генерирует вакансии, переходя через несколько страниц и возвращает карточки вакансий.
    Параметры:
    start_page_url: URL начальной страницы.
    pages_num: Количество страниц для перехода. По умолчанию 1.
    headers: Заголовки для использования в запросах. По умолчанию None.
    params: Query-параметры для передачи в запрос. По умолчанию None.
    Выдает:
    list[dict]: Список словарей, содержащих информацию о карточках вакансий.
    Примечание:
    Функция ожидает 1 секунду перед очередным запросом страницы, чтобы избежать перегрузки сервера.
    """
    page_content = get_html_content(start_page_url, headers, params)
    has_next_page = True
    for page in range(pages_num):
        print(f"Move to page #{page+1}")
        time.sleep(1)
        if not has_next_page:
            break
        vacancy_cards = get_vacancies_cards(page_content)
        next_page_link = get_next_page_link(start_page_url, headers=headers)
        if next_page_link:
            page_content = get_html_content(next_page_link, headers=headers)
        else:
            has_next_page = False
        yield vacancy_cards


def keyword_found(text: str, keywords: list[str]) -> bool:
    """
    Функция, которая проверяет, есть ли в предоставленном тексте хотя бы одно из ключевых слов из списка.
    Параметры:
        text: Строка, представляющая входной текст для поиска ключевых слов.
        keywords: Список строк, содержащий ключевые слова для поиска во входном тексте.
    Возвращает:
        bool: True, если хотя бы одно ключевое слово найдено, False в противном случае.
    """
    for keyword in keywords:
        keyword = keyword.lower()
        text = text.lower().strip()
        if text.find(keyword) != -1:
            return True
    return False


def get_vacancy_description(link: str, headers: dict = None, params: dict = None) -> str:
    """
    Получает описание вакансии по указанной ссылке
    Параметры:
        link: URL страницы вакансии.
        headers: Заголовки, используемые в HTTP-запросе. По умолчанию None.
        params: Query-параметры, используемые в HTTP-запросе. По умолчанию None
    Возвращает:
        str: Описание вакансии. Если описание не найдено, возвращается пустую строку
    Выбрасывает:
        AttributeError: Если тег с атрибутом 'data-qa', равным 'vacancy-description', не найден
    Примечание:
        Функция ожидает 1 секунду перед выполнением HTTP-запроса, чтобы избежать перегрузки сервера.
    """
    time.sleep(1)
    vacancy_description = ''
    content = get_html_content(link, headers=headers, params=params)
    if content:
        soup = BeautifulSoup(content, 'lxml')
        try:
            vacancy_description = soup.find('div', attrs={'data-qa': 'vacancy-description'}).text
        except AttributeError as e:
            print(f"Error: {e}. Can't find tag by attrs")
    return vacancy_description


def filter_by_currancy(vacancy_card: dict, currancy: str = '$') -> bool:
    """
    Отбор карточек вакансии по валюте.
    Параметры:
        vacancy_card: Словарь, представляющий карточку вакансии. Должен иметь ключ 'salary' со строковым значением.
        currancy: Валюта для фильтрации. Значение по умолчанию: '$'.
    Возвращает:
        bool: True, если зарплата карточки вакансии содержит указанную валюту, в противном случае False.
    """
    if vacancy_card['salary']:
        if currancy in vacancy_card['salary']:
            return True
    return False


def save_json(data, filename):
    """
    Сохраняет предоставленные данные в файл JSON.
    Параметры:
        data: Данные для сохранения в файл JSON.
        filename: Имя файла JSON, в котором будут сохранены данные
    Возвращает:
        None
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)
    except FileExistsError:
        print("File already exists")
        return
    except PermissionError:
        print("Permission denied")
        return
    except Exception as error:
        print(f"{error} while saving json")
        return


def main():
    suitable_cards = []
    filtered_cards = []
    vacancies_stats = {'viewed': 0, 'suitable': 0, 'suitable_filtered': 0}
    cards_count = 0
    for page_cards in get_vacancies_by_pages(BASE_URL, 2, HEADERS, MAIN_PARAMS):
        for card in page_cards:
            cards_count += 1
            print(f"Processing vacancies card #{cards_count}...", end=' ')
            vacancy_description = get_vacancy_description(card['link'], headers=HEADERS)
            vacancies_stats['viewed'] += 1
            if keyword_found(vacancy_description, KEYWORDS):
                suitable_cards.append(card)
                vacancies_stats['suitable'] += 1
                if filter_by_currancy(card):
                    vacancies_stats['suitable_filtered'] += 1
                    filtered_cards.append(card)
            print("done!")
    print("Viewed vacancies: ", vacancies_stats['viewed'])
    print("Suitable vacancies: ", vacancies_stats['suitable'])
    print("Suitable filtered vacancies: ", vacancies_stats['suitable_filtered'])
    if suitable_cards:
        save_json(suitable_cards, 'suitable_vacancies.json')
    if filtered_cards:
        save_json(filtered_cards, 'suitable_filtered_vacancies.json')


if __name__ == '__main__':
    main()
