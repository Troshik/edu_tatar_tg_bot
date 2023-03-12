import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
import configparser

# Загрузка логина и пароля из конфигурационного файла
config = configparser.ConfigParser()
config.read('config.ini')
username = config['user']['username']
password = config['user']['password']

# Функция для авторизации на сайте
def login(username, password):
    login_url = 'https://edu.tatar.ru/laishevo/login'
    session = requests.Session()
    login_page = session.get(login_url)
    soup = BeautifulSoup(login_page.content, 'html.parser')
    csrf_token = soup.find('input', {'name': '_csrf_token'}).get('value')
    payload = {
        '_csrf_token': csrf_token,
        '_username': username,
        '_password': password
    }
    login_request = session.post(login_url, data=payload)
    if login_request.status_code == 200:
        return session
    else:
        messagebox.showerror("Ошибка", "Неправильный логин или пароль")
        return None

# Функция для загрузки страницы расписания
def load_schedule(session):
    schedule_url = 'https://edu.tatar.ru/laishevo/org6906/page4685368.htm/show/3'
    schedule_page = session.get(schedule_url)
    soup = BeautifulSoup(schedule_page.content, 'html.parser')
    return soup

# Функция для обработки и вывода данных
def process_data(soup):
    schedule_table = soup.find('table', attrs={'class': 'gr-table'}) # Получение таблицы расписания
    rows = schedule_table.find_all('tr') # Получение всех строк таблицы

    # Создание списка данных для вывода
    data = []
    for row in rows:
        # Получение ячеек текущей строки
        cells = row.find_all('td')

        # Извлечение данных из ячеек
        cell_data = []
        for cell in cells:
            cell_data.append(cell.text.strip())

        # Добавление данных ячеек в список данных
        data.append(cell_data)

    # Вывод данных в виде таблицы
    table_str = ""
    for row in data:
        table_str += "|".join(row) + "\n"
    messagebox.showinfo("Расписание занятий", table_str)

# Функция для обработки нажатия на кнопку "Показать расписание"
def show_schedule():
    # Авторизация на сайте
    session = login(username_entry.get(), password_entry.get())
    if session is not None:
        # Загрузка страницы расписания
        soup = load_schedule(session)
        # Обработка и вывод данных
        process_data(soup)

# Создание глав
