from http.server import HTTPServer, SimpleHTTPRequestHandler
from collections import defaultdict
import datetime
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas

COMPANY_FOUNDATION_YEAR = 1920

def get_age_company() -> int:
    this_year = datetime.datetime.now().year
    company_age = this_year - COMPANY_FOUNDATION_YEAR
    return company_age

def get_correct_word(year: int) -> str:
    tenths = year % 10
    hundredths = year % 100
    if tenths == 1 and hundredths != 11:
        word = 'год'
    elif 1 < tenths < 5 and not 11 < hundredths < 15:
        word = 'года'
    else:
        word = 'лет'
    return word

def get_latest_data(list_data_files: list) -> str:
    last_file = None
    max_number = 0
    for name_file in list_data_files:
        name = name_file.split('.')[0]
        digit = 1 if len(name) == 4 else int(name[4:])
        if digit:
            max_number = digit if max_number < digit else max_number
            last_file = name_file
    return last_file

def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    company_age = get_age_company()
    correct_word = get_correct_word(company_age)
    
    list_of_data_files = os.listdir('wine_data/')
    try:
        last_file = get_latest_data(list_of_data_files)
    except (ValueError, IndexError):
        raise ValueError("Некорректное имя файла в директории wine_data/")

    path_to_wine_data = 'wine_data/{}'.format(last_file)
    wine_categories = pandas.read_excel(path_to_wine_data)['Категория'].tolist()
    wine_info = pandas.read_excel(path_to_wine_data,
                                    usecols=['Название', 'Сорт', 'Цена', 'Картинка', 'Акция'],
                                    keep_default_na=False
    ).to_dict(orient='record')

    wines_data = defaultdict(list)
    for category, wine in zip(wine_categories, wine_info):
        wines_data[category].append(wine)

    rendered_page = template.render(
        years_together="Уже {} {} с вами".format(company_age, correct_word),
        wines_data = wines_data,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()
