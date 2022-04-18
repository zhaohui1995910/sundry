# -*- coding: utf-8 -*-
# @Time    : 2021\\3\\22 17:27
# @Author  : zhaohui
# @FileName: selenium_proxy.py
# @Software: PyCharm
import json
import time

from selenium import webdriver
from browsermobproxy import Server

# 创建browsermobproxy
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType

caps = DesiredCapabilities.CHROME
caps['loggingPrefs'] = {
    'browser'    : 'ALL',
    'performance': 'ALL'
}
caps['perfLoggingPrefs'] = {
    'enableNetwork' : True,
    'enablePage'    : False,
    'enableTimeline': False
}

option = webdriver.ChromeOptions()
option.add_argument('--no-sandbox')
option.add_argument('--headless')
option.add_argument('--disable-extensions')
option.add_argument('--allow-running-insecure-content')
option.add_argument('--ignore-certificate-errors')
option.add_argument('--disable-single-click-autofill')
option.add_argument('--disable-autofill-keyboard-accessory-view[8]')
option.add_argument('--disable-full-form-autofill-ios')
option.add_experimental_option('w3c', False)
option.add_experimental_option('perfLoggingPrefs', {
    'enableNetwork': True,
    'enablePage'   : False
})

driver = webdriver.Chrome(executable_path='./drivers/chromedriver.exe', options=option, desired_capabilities=caps)

browsermod_path = "C:\\Users\\admin\\Desktop\\工作\\代码\\spider-toolframe\\drivers\\browsermob-proxy-2.0-beta-6\\bin\\browsermob-proxy.bat"
server = Server(browsermod_path)
server.start()

print(server.host)
print(server.port)

# 创建 proxy
# proxy = server.create_proxy(params={'trustAllServers': 'true'})
proxy = server.create_proxy(params={'trustAllServers': True})
proxy.new_har('baidu', options={'captureHeaders': True, 'captureContent': True})
# capabilities = DesiredCapabilities.CHROME
# proxy.add_to_capabilities(capabilities)

# 创建浏览器
# chrome_options = webdriver.ChromeOptions()

print(proxy.proxy)


def chrome_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    chrome_options.add_argument("--ssl-version-max")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--proxy-server=%s" % proxy.proxy)
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-insecure-localhost')
    chrome_options.add_argument('--ignore-urlfetcher-cert-requests')

    chrome = webdriver.Chrome('./drivers/chromedriver.exe',
                              chrome_options=chrome_options)

    # chrome.get('http://www.baotaigroup.com.cn')
    chrome.get('https://www.baidu.com')

    return chrome


def firefox_driver():
    profile = webdriver.FirefoxProfile()
    profile.set_proxy(proxy.selenium_proxy())
    firefox = webdriver.Firefox(executable_path='.\\drivers\\geckodriver.exe', firefox_profile=profile)

    # firefox.get('http:\\\\www.baotaigroup.com.cn')
    firefox.get('https:\\\\www.baidu.com')

    return firefox


driver = chrome_driver()

result = proxy.har
print('1', id(result['log']['entries']))
for entry in result['log']['entries']:
    print(entry)

# print('第二次请求')

# driver.get('http:\\\\www.baotaigroup.com.cn')
# result = proxy.har
# print('2', id(result['log']['entries']))
#
# for entry in result['log']['entries']:
#     print(entry)

input()


def driver_response():
    for typelog in driver.log_types:
        perfs = driver.get_log(typelog)
        for row in perfs:
            log_data = row
            log_json = json.loads(log_data['message'])
            log = log_json['message']

            if log['method'] == 'Network.responseReceived':
                request_id = log['params']['requestId']
                try:
                    response_body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
                    print(response_body['body'])
                except Exception:
                    print('response.body is null')


driver.quit()
proxy.close()
server.stop()
