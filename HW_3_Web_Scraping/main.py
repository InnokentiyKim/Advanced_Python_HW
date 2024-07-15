import requests
import time
from settings.config import BASE_URL, MAIN_PARAMS, HEADERS, KEYWORDS
from http import HTTPStatus
from bs4 import BeautifulSoup
import json


def get_html_content(url, headers=None, params=None) -> str:
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
    soup = BeautifulSoup(content, 'lxml')
    page_cards = []
    vacancies_main_block = soup.find('main', attrs={'class': 'vacancy-serp-content'})
    page_vacancies = vacancies_main_block.find('div', attrs={'id': 'a11y-main-content'})
    vacancies_cards = page_vacancies.find_all('div', attrs={'class': 'vacancy-card--z_UXteNo7bRGzxWVcL7y'})
    for card in vacancies_cards:
        vacancy_title_block = card.find('h2', attrs={'class': 'bloko-header-section-2'})
        vacancy_title = vacancy_title_block.text
        link_block = vacancy_title_block.find('a', attrs={'class': 'bloko-link'})
        vacancy_link = link_block['href']
        vacancy_compensation_block = card.find('div', attrs={'class': 'compensation-labels--uUto71l5gcnhU2I8TZmz'})
        salary_block = vacancy_compensation_block.find('span', attrs={'class': 'bloko-text'})
        vacancy_salary = str(salary_block.text) if salary_block else None
        if vacancy_salary:
            vacancy_salary = vacancy_salary.replace('\u202f', ' ').replace('\xa0', ' ')
        vacancy_info_block = card.find('div', attrs={'class': 'info-section--N695JG77kqwzxWAnSePt'})
        company_name = str(vacancy_info_block.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text)
        company_name = company_name.replace('\xa0', ' ')
        vacancy_location = vacancy_info_block.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
        page_cards.append({
            'title': vacancy_title,
            'salary': vacancy_salary,
            'company': company_name,
            'location': vacancy_location,
            'link': vacancy_link
        })
    return page_cards


def keyword_found(text: str, keywords: list[str]) -> bool:
    for keyword in keywords:
        keyword = keyword.lower()
        text = text.lower().strip()
        if text.find(keyword) != -1:
            return True
    return False


def get_vacancy_description(link, headers=None, params=None) -> str:
    time.sleep(1)
    vacancy_description = ''
    content = get_html_content(link, headers=headers, params=params)
    if content:
        soup = BeautifulSoup(content, 'lxml')
        vacancy_description = soup.find('div', attrs={'data-qa': 'vacancy-description'}).text
    return vacancy_description


def filter_by_currancy(vacancy_card, currancy='$') -> bool:
    if vacancy_card['salary']:
        if currancy in vacancy_card['salary']:
            return True
    return False


def save_json(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(file)
    except FileExistsError:
        print("File already exists")
    except Exception as error:
        print(f"{error} while saving json")


def main():
    start_page_content = get_html_content(BASE_URL, headers=HEADERS, params=MAIN_PARAMS)
    vacancy_cards = get_vacancies_cards(start_page_content)
    filtered_cards = {}
    vacancies_stats = {'viewed': 0, 'suitable': 0, 'suitable_filtered': 0}
    for card in vacancy_cards:
        vacancy_description = get_vacancy_description(card['link'], headers=HEADERS)
        vacancies_stats['viewed'] += 1
        if keyword_found(vacancy_description, KEYWORDS):
            if filter_by_currancy(card):
                print("Keywords found and curracy is $")
                vacancies_stats['suitable_filtered'] += 1
            else:
                print("Keywords found but curracy is not $")
                vacancies_stats['suitable'] += 1
        else:
            print("Keywords not found")
        print(card)
        time.sleep(1)
    print("Viewed vacancies: ", vacancies_stats['viewed'])
    print("Suitable vacancies: ", vacancies_stats['suitable'])
    print("Suitable filtered vacancies: ", vacancies_stats['suitable_filtered'])



if __name__ == '__main__':
    main()
