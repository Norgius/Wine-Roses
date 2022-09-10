from http.server import HTTPServer, SimpleHTTPRequestHandler
from collections import defaultdict
from pathlib import Path
import datetime
import os


from pprint import pprint
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

def find_last_added_filename(file_names: list) -> str:
    filename = None
    max_number = 0
    for fullname in file_names:
        name = fullname.split('.')[0]
        number = 1 if len(name) == 4 else int(name[4:])
        if number:
            max_number = number if max_number < number else max_number
            filename = fullname
    return filename

def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    company_age = get_age_company()
    correct_word = get_correct_word(company_age)
    
    file_names = os.listdir('wine_data/')
    try:
        filename = find_last_added_filename(file_names)
    except (ValueError, IndexError):
        raise ValueError("Некорректное имя файла в директории wine_data/")

    filepath = Path.cwd() / 'wine_data' / filename
    file_read = pandas.read_excel(filepath, keep_default_na=False)

    wine_categories = file_read['Категория'].to_list()
    wines = file_read[:].loc[:, 'Название':].to_dict(orient='record')

    sorted_wines = defaultdict(list)
    for category, wine in zip(wine_categories, wines):
        sorted_wines[category].append(wine)

    rendered_page = template.render(
        years_together="Уже {} {} с вами".format(company_age, correct_word),
        sorted_wines = sorted_wines,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()
