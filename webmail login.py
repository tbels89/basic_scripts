#pip install selenium, chromedriver 

# automatically login to webmail using chrome and selenium 

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

username1 = 'your email address'
password1 = 'your email password' 

class Browser:
    browser, service = None, None

    def __init__(self, driver: str):
        self.service = Service(driver)
        self.browser = webdriver.Chrome(service=self.service)

    def open_page(self, url: str):
        self.browser.get(url)

    """def close_browser(self):
        self.browser.close()"""

    def add_input(self, by: By, value: str, text: str):
        field = self.browser.find_element(by=by, value=value)
        field.send_keys(text)
        time.sleep(2)

    def click_button(self, by: By, value: str):
        button = self.browser.find_element(by=by, value=value)
        button.click()
        time.sleep(2)

    def login_email(self, username: str, password: str):
        self.add_input(by=By.ID, value='rcmloginuser', text=username)
        self.add_input(by=By.ID, value='rcmloginpwd', text=password)
        self.click_button(by=By.ID, value='rcmloginsubmit')

if __name__ == '__main__':
    browser = Browser('chromedriver_linux64/chromedriver') #where chromedriver is located 

    browser.open_page('https://website.com/login') # login page to open
    time.sleep(3)

    browser.login_email(username=username1, password=password1)
    time.sleep(10)