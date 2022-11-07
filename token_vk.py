import requests
from bs4 import BeautifulSoup as Bs

url = 'https://oauth.vk.com/authorize?client_id=6121396&scope=274677727&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1'
url2 = 'https://login.vk.com/?act=login&soft=1'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'sec-ch-ua-platform': 'Windows',
    'content-type': 'application/x-www-form-urlencoded',
    'upgrade-insecure-requests': '1',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
}
headers2 = {
    'authority': 'login.vk.com',
    'method': 'POST',
    'path': '/?act=login&soft=1',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'content-length': '369',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': '',
    'origin': 'https://oauth.vk.com',
    'referer': 'https://oauth.vk.com/',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "Windows",
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

payload = {
    'ip_h': '',
    'lg_domain_h': '',
    '_origin': '',
    'to': '',
    'expire': '',
    'email': input('login: '),
    'pass': input('password: ')
}

session = requests.Session()
response = session.get(url, headers=headers)
string = str(response.headers.get("set-cookie"))
soap = Bs(response.text, 'lxml')
cookie = f'{string[string.index("remixstlid="):].split(";")[0]}; {string[string.index("remixlgck="):].split(";")[0]}'
headers2['cookie'] = cookie
for i in soap.find('div', class_='oauth_form_login').find_all('input')[:5]: payload[i.get('name')] = i.get('value')
response = session.post(url2, data=payload, headers=headers2)
soap = Bs(response.text, 'lxml')
href_str = str(soap.find('script', type='text/javascript').findNext())
href = href_str[href_str.index('location.href = "') + len('location.href = "'):href_str.index('"+addr;')]
response = session.get(href)
print(response.url)


"""To pass captcha insert code below"""

# sid=soap.find_all('input')[-3].get('value')
# link=soap.find('img', class_='oauth_captcha').get('src')
# print(link)
# key=input()
# payload['captcha_sid']=sid
# payload['captcha_key']=key
# session.post(url2, data=payload, headers=headers2)
