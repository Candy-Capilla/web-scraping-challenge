from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

#url to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(2)

#scrape page into soup
    html = browser.html
    soup = bs(html, 'html.parser')



