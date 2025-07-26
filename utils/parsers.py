import requests
from bs4 import BeautifulSoup

from constants import program_urls

def get_programs_info(urls=program_urls):
    programs = []
    for _url in urls:
        program_info = {}

        response = requests.get(_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        body = soup.find('main')

        program_info['name'] = body.find('h1', class_='Information_information__header__fab3I').text

        cards_info = {}
        itable = body.find('div', class_='Information_table__fDHmi')
        for card in itable.find_all('div', class_='Information_card__rshys'):
            _name = card.find('div', class_='Information_card__header__6PpVf').text
            _value = card.find('div', class_='Information_card__text__txwcx').text
            cards_info[_name] = _value
        program_info['details'] = cards_info

        about_program = body.find('div', class_='AboutProgram_aboutProgram__textBlock__LpASa')
        program_info['description'] = about_program.find('span',
                                                         class_='AboutProgram_aboutProgram__description__Bf9LA').text
        programs.append(program_info)
    return programs