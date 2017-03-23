# -*- coding: utf-8 -*-
#!/usr/bin/python

# needs the Selenium package. Install it with pip by typing: pip install selenium
#install pip by running the script: https://bootstrap.pypa.io/get-pip.py (run by typing: python get-pip.py)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

class Spex_spider:
    def login_f_spexet_wiki(self):
        #login in, please do not fail
        self.driver.get('http://f-spexet.se/wiki/index.php?title=Special:Inloggning')
        #To ensure that we have loaded the page
        assert 'Logga in - F-spexet' in self.driver.title
        elementUser = self.driver.find_element_by_id("wpName1")
        elementPass = self.driver.find_element_by_id("wpPassword1")
        elementUser.send_keys(self.username)
        elementPass.send_keys(self.password,Keys.ENTER)
        #To ensure that we have loaded the page
        assert 'F-spexet' in self.driver.title
        time.sleep(1)

    def get_text_body(self,url):
        # to make it wait for the main page to load
        assert 'F-spexet' in self.driver.title
        self.driver.get(url)
        # to make it wait for the main page to load
        assert 'F-spexet' in self.driver.title
        element_body=self.driver.find_element_by_id("mw-content-text")
        text=element_body.text
        return text

    def __init__(self,username,password,browser):
        self.username=username
        self.password=password
        if browser.lower()=="firefox":
            firefox_capabilities = DesiredCapabilities.FIREFOX
            firefox_capabilities['marionette'] = True

            self.driver = webdriver.Firefox(capabilities=firefox_capabilities)
        else:
            print("Error: implemented drivers are: firefox.")
            print("Need something else? Try to implement a case that does self.driver=webdriver.MyBrowser() in __init__ in spex_spider.py")
        self.login_f_spexet_wiki()
