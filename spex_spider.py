# -*- coding: utf-8 -*-
#!/usr/bin/python

# needs the Selenium package. Install it with pip by typing: pip install selenium
#install pip by running the script: https://bootstrap.pypa.io/get-pip.py (run by typing: python get-pip.py)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class Spex_spider:
    def login_f_spexet_wiki(self):
        # Solution to log into google form from
        # https://stackoverflow.com/a/45954766
        # adapted from java to python
        #login in, please do not fail
        self.driver.get('https://wiki.f-spexet.se/index.php?title=Special:Inloggning&returnto=Huvudsida')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'identifierId')))
        #emailElem = self.driver.find_element_by_id('Email')
        emailElem = self.driver.find_element_by_id('identifierId')
        emailElem.send_keys(self.username)
        nextButton = self.driver.find_element_by_id('identifierNext')
        nextButton.click()
        time.sleep(1) # for some reason, explicit sleep is needed. Probabbly because password field is always there, just hidden.
        # attempt at solving this below does not work:
        #WebDriverWait(self.driver, 10).until(EC.visibility_of(self.driver.find_element_by_xpath("//input[@type='password']")))
        passwordElem = self.driver.find_element_by_xpath("//input[@type='password']")
        passwordElem.send_keys(self.password)
        signinButton = self.driver.find_element_by_id('passwordNext')
        signinButton.click()
        WebDriverWait(self.driver, 10).until(EC.title_contains('F-spexet'))

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
            #firefox_capabilities = DesiredCapabilities.FIREFOX
            #firefox_capabilities['marionette'] = True
            self.driver = webdriver.Firefox() #capabilities=firefox_capabilities
        else:
            print("Error: implemented drivers are: firefox.")
            print("Need something else? Try to implement a case that does self.driver=webdriver.MyBrowser() in __init__ in spex_spider.py")
        self.login_f_spexet_wiki()
