from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')
foundation_year = 1920
current_year = datetime.datetime.now().year
past_years = current_year - foundation_year

df_wines = pandas.read_excel('wine.xlsx', sheet_name='Лист1', na_values='None', keep_default_na=False)
wines = df_wines.to_dict(orient='records')
categorized_wines = defaultdict(list)
for wine in wines:
    categorized_wines[wine["Категория"]].append(wine)
rendered_page = template.render(year=past_years, data_wine=categorized_wines)


with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
