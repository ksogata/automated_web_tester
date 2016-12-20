# Automated Website Tester

This is the repository for my senior project.

## Prerequisites

### Installation
Install the following dependencies. You may need to install with root access.

* Install Selenium:
    ```
    $ pip install selenium
    ```

* Install Linkchecker
    ```
    $ pip install LinkChecker
    ```

## Optional Install

* Install PhantomJS (for headless testing)
    ```
    $ npm install phantomjs-prebuilt
    ```

## LinkChecker
LinkChecker is a tool that checks for broken links in web sites.
The original project's Github can be located at: https://github.com/wummel/linkchecker/.
To run from the command line:
Execute ``linkchecker http://www.example.com``.

## Google PageSpeed Insights
PageSpeed Insights measures the performance of a page for mobile devices and
desktop devices. The PageSpeed score ranges from 0 to 100. A higher score is better
and a score of 85 or above indicates that the page is performing well.

## Selenium
Selenium is a suite of tools that is used to automate web browsers. This installation
is in Python.  

## Folders in the project

### Drivers

* Currently includes three version of the chromedriver (Linux, Mac, and Windows).

### Selenium

* Includes all the selenium tests. Future selenium tests should also be put
into this folder.

## Browser vs Headless testing

Selenium emulates a user test on the browser. Users can automate the actions that a user would do on a webpage using Selenium. Headless testing
uses the PhantomJS webdriver that does not open a browser when it is run. There are some known issues with the PhantomJS webdriver, such as
weird behavior when clicking on a web element. However, PhantomJS can be run in the background.

## Creating tests
It is possible to create custom test suites using the Selenium framework. To do so, I have included
a template file that is used to set up both browser or headless tests. Populate the template file
with the custom test. Then add the test to "main.py" by adding
``suite.addTest(ExampleClassName('test_example'))`` to the selenium_test function.
