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
event1 = 1920
event2 = datetime.datetime.now().year
delta = event2 - event1

df_wines = pandas.read_excel('wine3.xlsx', sheet_name='Лист1', na_values='None', keep_default_na=False)
dict_wine = df_wines.to_dict(orient='records')
data_wine = defaultdict(list)
for k in dict_wine:
    data_wine[k["Категория"]].append(k)
rendered_page = template.render(year=delta, data_wine=data_wine)


with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
