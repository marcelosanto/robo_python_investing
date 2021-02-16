from bs4 import BeautifulSoup
import requests
import json

headers = requests.utils.default_headers()
headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68'})

data = requests.get(
    'http://br.investing.com/economic-calendar/', headers=headers)

result = []

if data.status_code == requests.codes.ok:
    info = BeautifulSoup(data.text, 'html.parser')

    blocos = (
        (info.find('table', {'id': 'economicCalendarData'})).find('tbody')).findAll('tr', {'class': 'js-event-item'})

    for blocos_2 in blocos:
        impacto = str((blocos_2.find('td', {'class': 'sentiment'})).get(
            'data-img_key').replace('bull', ''))
        horario = str(blocos_2.get('data-event-datetime')).replace('/', '-')
        moeda = (blocos_2.find(
            'td', {'class': 'left flagCur noWrap'})).text.strip()
        result.append({'par': moeda, 'horario': horario, 'impacto': impacto})


def escrever_json(lista):
    with open('meu_arquivo.json', 'w') as f:
        json.dump(lista, f)


for info in result:
    print('<----', '\nPARIDADE: ', info['par'], '\nHORARIO: ',
          info['horario'], '\nIMPACTO: ', info['impacto'], '\n---->\n')

escrever_json(result)
