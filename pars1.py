#https://edu.tatar.ru/user/diary/day?for=1678309200 11
#https://edu.tatar.ru/user/diary/day?for=1678136400 10
#https://edu.tatar.ru/user/diary/day?for=1678050000 9
#https://edu.tatar.ru/user/diary/day?for=1678136400 7
#https://edu.tatar.ru/user/diary/day?for=1678050000 6
#https://edu.tatar.ru/user/diary/day?for=1677877200 4

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# Загрузка HTML-страницы

# Создание объекта BeautifulSoup для парсинга HTML-кода
#print(page.text)


#soup = bs(page.content, 'html.parser')
#log = input('Введите логин ')
#pas = input('Введите пароль ')


class Iterpals(object):
    url = 'https://edu.tatar.ru/logon'


    def auth(self):
        session = requests.Session()
        url = self.url + ''
        params = {
            'main_login2':u'4480018566',
            'main_password2':u'p_vrSR6X'
        }
        r = session.post(url, params)
        print(r.text)


if __name__ == "__main__":
    iterals = Iterpals()
    iterals.auth()