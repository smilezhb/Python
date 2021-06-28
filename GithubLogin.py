# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
# 配置代理
proxies = {
    "https": "http://127.0.0.1:4780",
}
# UA伪装
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
# 获取会话对象，自动携带cookie
session = requests.session()
def get_preset_field():
    url = "https://github.com/login"
    response = session.get(url=url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(response.text, 'lxml')
    # 获取登录需要的预设值
    authenticity_token = soup.find('input', attrs={'name': 'authenticity_token'}).get("value")
    timestamp = soup.find('input', attrs={'name': 'timestamp'}).get("value")
    timestamp_secret = soup.find('input', attrs={'name': 'timestamp_secret'}).get("value")
    return authenticity_token,timestamp,timestamp_secret
def login(authenticity_token,timestamp,timestamp_secret):
    account = input('please enter your account: ')
    password = input('please enter your password: ')
    login_url = 'https://github.com/session'
    # POST传递参数数据
    data = {
        'commit': 'Sign in',
        'login': account,
        'password': password,
        'webauthn-support': 'supported',
        'webauthn-iuvpaa-support': 'supported',
        'authenticity_token': authenticity_token,
        'timestamp': timestamp,
        'timestamp_secret': timestamp_secret
    }
    # 请求登录
    response = session.post(url=login_url, headers=headers, proxies=proxies, data=data)
    print(response.status_code)
    with open('github_login.html', 'w', encoding='utf-8') as f:
        f.write(response.text)

if __name__ == '__main__':
    fields = get_preset_field()
    login(fields[0],fields[1],fields[2])
    # 请求个人主页
    profile_url = 'https://github.com/smilezhb'
    page_text = session.get(url=profile_url, headers=headers, proxies=proxies).text
    with open('github_profile.html', 'w', encoding='utf-8') as f:
        f.write(page_text)

