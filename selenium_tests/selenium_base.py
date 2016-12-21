from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest
import os
from sys import platform
import time
import requests

driver_dir = os.path.join(os.getcwd(), 'drivers/')

class BaseTest(unittest.TestCase):
    # grab url from main
    base_url = 'https://www.digitaldemocracy.org/'

    # get os type from platform
    os_name = platform
    #print os_name

    # path to chromedriver
    chrome_options = None

    if 'linux2' == os_name:
        chrome_path = driver_dir + 'linux_chromedriver'
    elif 'win32' == os_name:
        chrome_path = driver_dir + 'win_chromedriver'
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
    elif 'darwin' == os_name:
        chrome_path = driver_dir +  'mac_chromedriver'

    def set_up_browser(self):
        '''This function will be called before each individual test is run.'''

        chromedriver = self.chrome_path
        #print chromedriver
        os.environ['webdriver.chrome.driver'] = chromedriver
        self.driver = webdriver.Chrome(chromedriver, chrome_options=self.chrome_options)

    def set_up_headless(self):
        self.driver = webdriver.PhantomJS()

    def navigate_to_page(self):
        driver = self.driver

        driver.get(self.base_url)

        #driver.find_element_by_class_name('ui-dialog-titlebar-close').click()

    def tearDown(self):
        self.driver.quit()
        self.driver = None

    def highlight(self, element, timeout=3):
        '''Highlights a Selenium Webdriver element, timeout should be a positive
        integer representing the number of seconds to highlight the
        element on the page'''

        # get the driver
        driver = element._parent

        # scroll to center the element in current view
        driver.execute_script("return arguments[0].scrollIntoView();", element)

        # internal callable to apply new style
        def apply_style(new_style):
            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                   element, new_style)

        # get original style to put it back later
        original_style = element.get_attribute('style')

        # change to new debug style
        apply_style("background: orange; border: 6px solid red;")

        time.sleep(timeout)

        # change back to original style
        apply_style(original_style)

    # grabs the file 'elements.txt'
    # file should have a word/phrase separated by newline
    # start with 'tag=' if tag is specified otherwise will default to text
    def get_text_to_find(self):
        f = open('elements.txt', 'r')
        txt_list = []
        for line in f:
            txt_list.append(line.rstrip())
        return txt_list

    # splits text by comma and returns the second word/phrase
    def split_text(self, line):
        split = line.split(',')
        return split[1].lstrip()
