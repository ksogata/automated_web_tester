from __future__ import unicode_literals
from selenium_base import *
import time
import re

class FindElementOnPage(BaseTest):
    def setUp(self):
        super(FindElementOnPage, self).set_up_browser()

    def test_highlight_on_page(self):
        driver = self.driver
        self.navigate_to_page()

        # for case-insensitive search use translate
        upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        lower = 'abcdefghijklmnopqrstuvwxyz'

        # get text to find in webpage
        texts = self.get_text_to_find()

        # loop to find text in 'elements.txt' file
        for text in texts:
            # check if user specified tag
            # find_elements_by_* functions are case-sensitive
            if 'tag=name' in text:
                t = self.split_text(text)
                elements = driver.find_elements_by_name(t)
                self.highlight_elements(elements, text)

            elif 'tag=link' in text:
                t = self.split_text(text)
                elements = driver.find_elements_by_link_text(t)
                self.highlight_elements(elements, text)

            elif 'tag=partial link' in text:
                t = self.split_text(text)
                elements = driver.find_elements_by_partial_link_text(t)
                self.highlight_elements(elements, text)

            elif 'tag=tag name' in text:
                t = self.split_text(text)
                elements = driver.find_elements_by_tag_name(t)
                self.highlight_elements(elements, text)

            elif 'tag=class' in text:
                t = self.split_text(text)
                elements = driver.find_elements_by_class_name(t)
                self.highlight_elements(elements, text)

            elif 'tag=css selector' in text:
                t = self.split_text(text)
                elements = driver.find_elements_by_css_selector(t)
                self.highlight_elements(elements, text)

            # if no tag specified search through all text on page
            else:
                # finds all instances of a word/phrase using xpath
                text = text.lower()
                # we can use xpath translate to perform case insensitive search
                elements = driver.find_elements_by_xpath("//*[contains(translate(text(), \
                    '" + upper + "', \
                    '" + lower + "'), \
                    '" + text + "')]")
                highlight_elements(elements, text)
                    #print 'text {0} is not found.'.format(text)

    # highlights text given the elements to highlight
    def highlight_elements(self, elements, text):
        if (elements):
            for el in elements:
                if (el.is_displayed()):
                    self.highlight(el)
        else:
            print 'The element "{0}" can not be found on the webpage.'.format(text)

class FindElementHeadless(BaseTest):
    def setUp(self):
        super(FindElementHeadless, self).set_up_headless()

    def test_element_on_page(self):
        driver = self.driver
        self.navigate_to_page()

        # for case-insensitive search using translate
        upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        lower = 'abcdefghijklmnopqrstuvwxyz'

        # get text from file to search for on webpage
        texts = self.get_text_to_find()

        for text in texts:
            # check if user specified tag
            # find_elements_by_* functions are case-sensitive
            if 'tag=name' in text:
                t = self.split_text(text)
                elements = driver.find_elements_by_name(t)
                self.check_elements_on_page(elements, text)

            elif 'tag=link' in text:
                t = self.split_text(text)
                elements = driver.find_elements_by_link_text(t)
                self.check_elements_on_page(elements, text)

            elif 'tag=partial link' in text:
                t = self.split_text(text)
                elements = driver.find_elements_by_partial_link_text(t)
                self.check_elements_on_page(elements, text)

            elif 'tag=tag name' in text:
                t = self.split_text(text)
                elements = driver.find_elements_by_tag_name(t)
                self.check_elements_on_page(elements, text)

            elif 'tag=class' in text:
                t = self.split_text(text)
                elements = driver.find_elements_by_class_name(t)
                self.check_elements_on_page(elements, text)

            elif 'tag=css selector' in text:
                t = self.split_text(text)
                elements = driver.find_elements_by_css_selector(t)
                self.check_elements_on_page(elements, text)

            # if no tag specified search through all text on page
            else:
                text = text.lower()
                elements = driver.find_elements_by_xpath("//*[contains(translate(text(), \
                    '" + upper + "', \
                    '" + lower + "'), \
                    '" + text + "')]")
                self.check_elements_on_page(elements)

    def check_elements_on_page(self, elements, text):
        if (elements):
            for el in elements:
                print 'The element "{0}" is on the webpage.'.format(text)
                self.assertTrue(el)
        else:
            print 'The element "{0}" can not be found on the webpage.'.format(text)
#if __name__ == "__main__":
#    unittest.main()
