import requests
from bs4 import BeautifulSoup
import pandas as pd

# Загрузка HTML-страницы
page = requests.get("https://edu.tatar.ru/laishevo/org6906/page4685368.htm/show/3")

# Создание объекта BeautifulSoup для парсинга HTML-кода
soup = BeautifulSoup(page.content, 'html.parser')

# Извлечение данных из HTML-кода с помощью BeautifulSoup
schedule_table = soup.find_all('table')[0]  # Получение таблицы расписания
rows = schedule_table.find_all('tr')  # Получение всех строк таблицы

# Обработка и вывод данных
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

# Создание объекта DataFrame из списка данных
df = pd.DataFrame(data[1:], columns=data[0])

# Вывод таблицы данных
print(df)
