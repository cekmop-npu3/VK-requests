import requests
from bs4 import BeautifulSoup as Bs
from payload import *


class Login:
    def __init__(self, login, password, basic_headers, login_headers, payload, payload2):
        self.url = 'https://oauth.vk.com/authorize?client_id=6121396&scope=274677727&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1'
        self.login_url = 'https://login.vk.com/?act=login&soft=1'
        self.login = login
        self.password = password
        self.b_headers = basic_headers
        self.l_headers = login_headers
        self.payload = payload
        self.payload2 = payload2
        self.payload['email'] = self.login
        self.payload['pass'] = self.password
        self.session = requests.Session()
        self._main()

    def _main(self):
        response = self.session.get(self.url, headers=self.b_headers)
        string = str(response.headers.get("set-cookie"))
        cookie = f'{string[string.index("remixstlid="):].split(";")[0]}; {string[string.index("remixlgck="):].split(";")[0]}'
        self.l_headers['cookie'] = cookie
        soup = Bs(response.text, 'lxml')
        for i in soup.find('div', class_='oauth_form_login').find_all('input')[:5]: self.payload[i.get('name')] = i.get('value')
        self._login()

    def _token(self, response):
        soup = Bs(response.text, 'lxml')
        href_str = str(soup.find('script', type='text/javascript').findNext())
        try:
            href = href_str[href_str.index('location.href = "') + len('location.href = "'):href_str.index('"+addr;')]
            response = self.session.get(href)
            print(response.url)
        except ValueError:
            print('------Incorrect 2fa------')
            self._2fa(response)

    def _2fa(self, response):
        if 'https://oauth.vk.com/login?act=authcheck' in response.url:
            soup = Bs(response.text, 'lxml')
            href = 'https://oauth.vk.com' + soup.find('div', class_='form_item').find('form').get('action')
            phone_mask = soup.find('div', class_='form_item').find('div', class_='fi_row').text.split('номер')[1].strip()[:-1]
            self.payload2['phone_mask'] = phone_mask
            self.payload2['code'] = input('2fa: ')
            response = self.session.post(href, data=payload2, headers=self.b_headers)
        self._token(response)

    def _login(self):
        response = self.session.post(self.login_url, data=self.payload, headers=self.l_headers)
        if 'https://oauth.vk.com/authorize' in response.url:
            soup = Bs(response.text, 'lxml')
            self._captcha(soup)
        else: self._2fa(response)

    def _captcha(self, soup):
        sid = soup.find_all('input')[-3].get('value')
        try:
            link = soup.find('img', class_='oauth_captcha').get('src')
            print(link)
            key = input('Captcha: ')
            self.payload['captcha_sid'] = sid
            self.payload['captcha_key'] = key
        except AttributeError:
            print('------Incorrect data------')
            self.payload['email'] = input('Login: ')
            self.payload['pass'] = input('Password: ')
        self._login()


login = Login('login', 'password', headers, headers2, payload, payload2)