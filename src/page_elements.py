from src.element_classes import *

class PageElements(object):
    def __init__(self, driver):
        # Driver for testing JavaScript elements (can be Browser or Headless)
        self.driver = driver
        # Button to close the About popup box on every page on first visit
        self.popup_close = ElementByClassName('ui-dialog-titlebar-close',
            self.driver)
