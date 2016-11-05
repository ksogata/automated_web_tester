from selenium import webdriver
import unittest
import os
from sys import platform
import time
import requests

from page_elements import *
from custom_assertions import *

driver_dir = os.path.join(os.getcwd(), 'drivers/')

'''
README:
-will need to install PhantomJS()
    -on linux can be installed with npm: npm install -g phantomjs-prebuilt
'''

class BaseTestCase(unittest.TestCase, CustomAssertions):
    base_url = ''
    pages = ['/apache-search', '/hearings', '/bills', '/persons',
             '/organizations', '/commentators', '/about', '/contact/',
             '/node/1', '/user', '/user/register', '/user/password']

    # get os type from platform
    os_name = platform
    # get the 32bit/64bit info from first tuple
    # arch_version = platform.architecture()

    # path to chromedriver
    chrome_options = None
    if 'linux2' in os_name:
        chrome_path = driver_dir + 'linux_chromedriver64'
    elif 'win32' in os_name:
        chrome_path = driver_dir + 'win_chromedriver'
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
    elif 'darwin' in os_name:
        chrome_path = driver_dir + 'mac_chromedriver'

    #setup intial drive and direct to the home page
    def set_up_browser(self):
        '''This function will be called before each individual test is run.'''
        chromedriver = self.chrome_path
        os.environ['webdriver.chrome.driver'] = chromedriver
        # chrome_options.add_argument('')
        self.d = webdriver.Chrome(chromedriver, chrome_options=self.chrome_options)

    def set_up_headless(self):
        '''This function will be called before each individual test is run.'''
        self.d = webdriver.PhantomJS()

    # NOTE: camelCase is needed in this functions name for it to work properly.
    def tearDown(self):
        '''This function will be called after each individual test is run.'''
        self.d.quit()
        self.driver = None

    def navigate_to_page(self, page):
        '''Use this function to start navigation at your desired test page in
           the beginning of every test caes.'''
        # build path for the specified page
        full_path = self.base_url + page

        # navigate to the search page
        self.d.get(full_path)

        # close the 'About Digital Democracy' popup
        self.driver.popup_close.get_element().click()

    def highlight(self, element, timeout=3):
        '''Highlights a Selenium Webdriver element, timeout should be a
           positive integer representing the number of seconds to highlight
           the element on the page.'''
        # get the driver
        driver = element._parent

        # scroll to center the element in current view
        driver.execute_script("return arguments[0].scrollIntoView();", element)

        # internal callable to apply new style
        def apply_style(new_style):
            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, new_style)

        # get original style to put it back later
        original_style = element.get_attribute('style')

        # change to new debug style
        apply_style("background: orange; border: 6px solid red;")

        time.sleep(timeout)

        # change back to original style
        apply_style(original_style)

    def get_page_list(self):
        # return the list of navigation to pages
        return self.pages;

    def test_status_code(self, link_to_check):
        '''Test the status code of a single webpage is 200.'''
        try:
            # try to get the response status code
            response = requests.get(link_to_check)
            resp_code = response.status_code

            # confirm that the code is 200 (request has succeeded)
            self.assertEqual(resp_code, 200, msg='Webpage: {} response code: {}'\
                .format(link_to_check, resp_code))
        except requests.ConnectionError:
            print 'Failed to connect to: ', link_to_check
