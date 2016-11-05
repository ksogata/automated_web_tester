from abc import ABCMeta, abstractmethod

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as AC
from selenium.webdriver.chrome.options import Options

def get_element_catch(method):
    '''Decorator for use with get_element() methods. Used because those methods
       all throw an exception if the element could not be found.'''
    def func(*args, **kwargs):
        try:
            # result will be the page page element, if found
            result = method(*args, **kwargs)
        except Exception as e:
            raise AssertionError('get_element() error: could not find '\
                'specified field: \'{}\' \nClass type {}'.format(
                args[0].element_name, type(args[0])))
        else:
            return result
    return func

class AbstractElement(object):
    __metaclass__ = ABCMeta

    def __init__(self, name, driver):
        self.element_name = name
        self.driver = driver

    @abstractmethod
    def get_element(self):
        pass

    def click_near_element(self, x_off, y_off):
        try:
            element = self.get_element()
            action = AC(self.driver)
            action.move_to_element_with_offset(element, x_off, y_off)
            action.click()
            action.perform()
        except Exception as e:
            raise AssertionError('Could not click near ', self.element_name)

    def wait_for_element_open(self, timeout):
        '''Waits for the specified element to appear, and if found returns it'''
        by_type = self._by_type_lookup()
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((
                    by_type, self.element_name)))
        except Exception as e:
            # print 'Could not find element {} with error msg {}'.\
            #     format(element_name, e}
            raise AssertionError('wait_for_element_open() could not find element \
                field by: {}'.format(by_type0))
        else:
            return element

    def wait_for_element_closed(self, timeout):
        '''Waits for the specified element to appear, and if found returns it'''
        by_type = self._by_type_lookup()
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((by_type, self.element_name)))
        except Exception as e:
            raise AssertionError('wait_for_element_closed() could not find element \
                field by: '.format(by_type))
        else:
            return element

    def _by_type_lookup(self):
        '''Get the instance type to determine the By._ variable.'''
        if isinstance(self, ElementById):
            return By.ID
        elif isinstance(self, ElementByClassName):
            return By.CLASS_NAME
        elif isinstance(self, ElementByName):
            return By.NAME

class ElementById(AbstractElement):
    @get_element_catch
    def get_element(self):
        return self.driver.find_element_by_id(self.element_name)

class ElementByClassName(AbstractElement):
    @get_element_catch
    def get_element(self):
        return self.driver.find_element_by_class_name(self.element_name)

class ElementByName(AbstractElement):
    @get_element_catch
    def get_element(self):
        return self.driver.find_element_by_name(self.element_name)

class ElementByXPath(AbstractElement):
    @get_element_catch
    def get_element(self):
        return self.driver.find_element_by_xpath(self.element_name)

class ElementByLinkText(AbstractElement):
    @get_element_catch
    def get_element(self):
        return self.driver.find_element_by_link_text(self.element_name)
