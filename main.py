import os
import sys
import subprocess
import urllib2
import urllib
import json
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup
from selenium import *
import argparse

def main():
    parser = argparse.ArgumentParser(description='Generic Web Tester')
    parser.add_argument('url', type=str)
    parser.add_argument('--linkchecker', '-l', action='store_true',
        help='runs linkchecker. DEFAULT runs all.')
    parser.add_argument('--pagespeed', '-p', action='store_true',
        help='runs Google PageSpeed Insights. DEFAULT runs all.')
    parser.add_argument('--selenium_browser', '-s', action='store_true',
        help='runs Selenium browser and headless tests. DEFAULT runs all.')
    #parser.add_argument('--selenium_headless', '-h' action='store_true',
    #    help='runs Selenium headless tests. DEFAULT runs all.')

    args = parser.parse_args()
    url = args.url

    # put 'https://' in front of url
    if (url.find('https://') == -1):
        url = 'https://' + url

    # if no flags, run all programs
    if (not(args.linkchecker or args.pagespeed
            or args.selenium_browser)):
        linkcheck(url)
        query_psi(url)
        selenium_test(url)
    else:
        if (args.linkchecker):
            linkcheck(url)

        if (args.pagespeed):
            # query pagespeed insight api
            query_psi(url)

        if (args.selenium):
            # do selenium tests
            selenium_test(url)

def linkcheck(url):
    subprocess.call(['linkchecker', '--check-extern', url, '-Ftext', '-r1'])
    # linkchecker outputs to file 'linkchecker-out.txt'
    # print that out to stdout
    with open('linkchecker-out.txt', 'r') as outfile:
        print outfile.read()

def selenium_test(url):
    BaseTest.base_url = url
    #print BaseTest.base_url
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner()

    suite.addTest(FindElementHeadless('test_element_on_page'))
    suite.addTest(FindElementOnPage('test_highlight_on_page'))

    runner.run(suite)

def query_psi(url):
    params = {'url': url,
              'key': 'AIzaSyD3XvANMzJthYzMeK0Wfm4r0NFoQiSM5ts'}
    url = ('https://www.googleapis.com/pagespeedonline/v1/runPagespeed?'
    + urllib.urlencode(params))

    response = urllib.urlopen(url).read()
    result = json.loads(response)
    psi_information(result)

def psi_information(result):
    print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
    print '%% Google PageSpeed Results %%'
    print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n'

    print 'Score: ' + str(result['score']) + '\n'
    ruleResults = result['formattedResults']['ruleResults']
    for rule, results in ruleResults.iteritems():
        impact = results['ruleImpact']
        if (float(impact) > 0):
            print '%%%%% ' + rule + ' %%%%%'
            print results['urlBlocks'][0]['header']['format'] + '\n'


if __name__ == '__main__':
    main()
