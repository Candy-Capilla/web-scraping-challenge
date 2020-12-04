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

#soupify page- find title
    mars_soup = soup.find_all("div", class_= "content_title")
    title= mars_soup[1].get_text()

#soupify page- find paragraph
    mars_soup = soup.find_all("div", class_= "article_teaser_body")
    paragraph= mars_soup[0].get_text()

#second url to scrape
    url1 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(2)

#find click links
    browser.links.find_by_partial_text("FULL IMAGE")[0].click()
    browser.links.find_by_partial_text("more info")[0].click()

#use txt to find image
    text_soup = soup.find_all("figure", class_= "lede")
    figure= text_soup[0]
    image_soup = figure.find_all("a", href = True)
    image_soup[0]["href"]

#define feature 
    featured_image_url = "https://www.jpl.nasa.gov" + image_soup[0]["href"]

#



