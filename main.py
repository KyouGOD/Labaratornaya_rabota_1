import requests
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def parser(url):

    def mycommentdef(a, i):
        comment = ''
        count = 0
        for txt in a:
            if count%2 == 1:
                for txtdivision in txt:
                    comment += txtdivision.text + ' '  # формирует +- аккуратный комментарий
            count += 1
        data['features&comments'][i] += (comment.replace('\xa0', ' '))
        i += 1
        return i

    page = requests.get(url, headers={'User-Agent': UserAgent().chrome})
    soup = BeautifulSoup(page.text, "html.parser")
    pricepars = soup.findAll('div', class_='property__price')
    addresspars = soup.findAll('a', class_='location slim')
    floorpars = soup.findAll('div', class_='property__building')
    squarepars = soup.findAll('div', class_='property__area')

    data = {'prices': [], 'addresses': [], 'property type': [], 'floor': [], 'square': [], 'features&comments': [], 'urls': []}

    for link in addresspars:
        data['urls'].append(link.get('href'))  # находит ссылку на объявление
        data['addresses'].append(link.contents[1])  # находит адрес жилья
        data['property type'].append(link.find('span', class_='main-param').contents[0])  # находит тип жилья

    for price in pricepars:
        comment = ''
        count = 0
        for txt in price:
            if count%2 == 1:
                comment += txt.text + " "  # формирует элементы в словаре для ключа features&comments
            count += 1
        data['features&comments'].append(comment.replace('','(цена недавно выросла)').replace('', '(цена недавно снизилась)').replace('\xa0', ' '))
        data['prices'].append(price.find('span', class_='main-param').text.replace('\xa0', ''))  # находит арендную плату за 1 месяц

    i = 0
    for floor in floorpars:
        a = floor
        i = mycommentdef(a, i)
        data['floor'].append(floor.find('span', class_='main-param').text.replace('Этаж: ', ''))

    i = 0
    for square in squarepars:
        a = square
        i = mycommentdef(a, i)
        if square.find('span', class_='main-param') is None:  # обрабатывает объявления, где не указана площадь
            data['square'].append('Не указана')
            continue
        data['square'].append(square.find('span', class_='main-param').text.replace('\xa0', ''))  # находит площадь жилья
    pd.DataFrame(data).to_excel('test.xlsx')


url = 'https://omsk.mlsn.ru/arenda-nedvizhimost/'
parser(url)
