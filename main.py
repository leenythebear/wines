from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas


def load_template(template_path):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template(template_path)
    return template


def calc_years_count(foundation_year=1920):
    current_year = datetime.datetime.now().year
    past_years = current_year - foundation_year
    return past_years


def get_wines_data(file_path):
    df_wines = pandas.read_excel(file_path, sheet_name='Лист1', na_values='None', keep_default_na=False)
    wines = df_wines.to_dict(orient='records')
    categorized_wines = defaultdict(list)
    for wine in wines:
        categorized_wines[wine["Категория"]].append(wine)
    return categorized_wines


def render_page(template, past_years, categorized_wines):
    rendered_page = template.render(year=past_years, data_wine=categorized_wines)
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


if __name__ == "__main__":
    html_template = load_template('template.html')
    years_count = calc_years_count()
    file_path = input("Укажите путь к файлу: ")
    wines_grouped_by_categories = get_wines_data(file_path)
    render_page(html_template, years_count, wines_grouped_by_categories)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
