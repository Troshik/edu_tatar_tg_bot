import requests
import re
from bs4 import BeautifulSoup


week_days1 = ['Понедельник', 'Вторник', 'Среда']
week_days2 = ['Четверг', 'Пятница', 'Суббота']

url_active = 'https://edu.tatar.ru/user/diary/week'


def auth(login, par, pr='https://edu.tatar.ru/user/diary/week'):
    session = requests.Session()
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://edu.tatar.ru',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-GPC': '1',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://edu.tatar.ru/login/',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    data = {
        'main_login2': f'{login}',
        'main_password2': f'{par}',}
    response = session.post('https://edu.tatar.ru/logon', headers=headers, data=data, allow_redirects=True)
    pr_res = session.get(pr, headers=headers)
    return pr_res


def marks(log, par, ur='https://edu.tatar.ru/user/diary/week'):
    result = []
    pr_res = auth(log, par, ur)
    soup = BeautifulSoup(pr_res.text, "html.parser")
    marks = soup.find_all(class_='tt-mark')
    mark = []
    for data in marks:
        if data.find('div') is not None:
            mark.append(data.text)

    subjects = soup.find_all(class_='tt-subj')
    subject = []
    for data in subjects:
        if data.find('div') is not None:
            subject.append(data.text)

    hometasks = soup.find_all(class_='tt-task')
    hometask = []
    for data in hometasks:
        if data.find('div') is not None:
            hometask.append(data.text)

    dates = []
    day_numb = 1
    less = 8
    days = soup.find_all(class_='tt-days')
    for w in days:
        if w.find('div') is not None:
            dates.append(w.text)

    d = soup.find_all(class_="tt-days-mo")
    if d != []:
        week = 1
    else:
        week = 2

    for i in range(len(subject) - 1):
        if less == 8:
            result.append(dates[day_numb].strip() + ', ' + week_days1[day_numb - 1] if week == 1
                          else week_days2[day_numb - 1])
            less = 0
            if day_numb < 3:
                day_numb += 1
            else:
                day_numb = 1

        if subject[i].strip() != '':
            result.append(subject[i].strip())
            result.append("Д/З: " + hometask[i].strip())
            result.append("Оценка: " + mark[i].strip() if mark[i] != '\n\n' else '-')
            result.append('')
        less += 1
    return '\n'.join(result)


def next_w(log, par, url='https://edu.tatar.ru/user/diary/week'):
    global url_active
    pr_res = auth(log, par, url)
    soup = BeautifulSoup(pr_res.text, "html.parser")
    next_week = soup.find_all(class_="g-button-blue")
    new_url = str(next_week[1]['href'])
    url_active = new_url
    return marks(log, par, url_active)


def last_w(log, par, url='https://edu.tatar.ru/user/diary/week'):
    global url_active
    pr_res = auth(log, par, url)
    soup = BeautifulSoup(pr_res.text, "html.parser")
    next_week = soup.find_all(class_="g-button-blue")
    new_url = str(next_week[0]['href'])
    url_active = new_url
    return marks(log, par, url_active)