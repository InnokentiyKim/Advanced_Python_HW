import requests
import time
from settings.config import BASE_URL, MAIN_PARAMS, HEADERS, KEYWORDS
from http import HTTPStatus
from bs4 import BeautifulSoup


def get_html_content(url, headers=None, params=None) -> str:
    html_content = ''
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == HTTPStatus.OK:
            response.encoding = 'UTF-8'
            html_content = response.text
    except:
        print("Error occured while getting html content")
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
            vacancy_salary = vacancy_salary.replace('\u202f000', ' ').replace('\xa0', ' ')
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
    for word in keywords:
        word = word.lower()
        if word in text.lower().strip():
            return True
    return False


def get_vacancy_description(link, headers=None, params=None) -> str:
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


def main():
    start_page_content = get_html_content(BASE_URL, headers=HEADERS, params=MAIN_PARAMS)
    vacancy_cards = get_vacancies_cards(start_page_content)
    for card in vacancy_cards:
        vacancy_description = get_vacancy_description(card['link'], headers=HEADERS)
        if keyword_found(vacancy_description, KEYWORDS):
            if filter_by_currancy(card):
                print("Keywords found and curracy is $")
            else:
                print("Keywords found but curracy is not $")
        else:
            print("Keywords not found")
        print(card)
        time.sleep(1)


if __name__ == '__main__':
    main()




