import requests
from bs4 import BeautifulSoup
import fake_user_agent
url = 'https://edu.tatar.ru/logon'
#user = fake_user_agent.user_agent().random
headers = {
    #'user-agent':user
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.4.779 Yowser/2.5 Safari/537.36'
}
data = {
    'main_login2':'4480018566',
    'main_password2':'p_vrSR6X'
}
session = requests.Session()
#session.headers.update(headers)
response = session.post(url, data=data, headers=headers)

pr = 'https://edu.tatar.ru/user/diary/day?for=1678309200'
pr_res = session.get(pr, headers=headers).text
print(pr_res)