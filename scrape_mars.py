from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
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

#scrape mars table 
    df = pd.read_html("https://space-facts.com/mars/")
    html_table = df[0].to_html()

#scrape another url
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    links=browser.links.find_by_partial_text("Hemisphere Enhanced")
    hemisphere_image_urls= []

#create  loop to repeat scrape
    for l in range(len(links)):
        browser.links.find_by_partial_text("Hemisphere Enhanced")[l].click()
        time.sleep(2)
        html = browser.html
        soup = bs(html, 'html.parser')
        downloads = soup.find_all("div", class_= "downloads")
        figure= downloads[0]
        pic_soup = figure.find_all("a", href = True)
        #print(pic_soup[0]["href"])
        hemisphere={}
        hemisphere["img_url"]= pic_soup[0]["href"]
        titles = soup.find_all("h2", class_= "title")
        title= titles[0]
        hemisphere["title"]= title.get_text()
        hemisphere_image_urls.append(hemisphere)
        browser.back()
#close browser
        browser.quit()




