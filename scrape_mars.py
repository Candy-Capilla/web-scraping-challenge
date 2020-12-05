#import dependencies

from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

#create function to initalize browser
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
#open browser
    browser = init_browser()

#url to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(2)

# Scrape page into Soup

    html = browser.html
    soup = bs(html, "html.parser")

#find title
    mars_soup_title = soup.find_all("div", class_= "content_title")    
    title = mars_soup_title[1].get_text()

#find paragraph
    mars_soup_paragraph = soup.find_all("div", class_= "article_teaser_body")
    paragraph = mars_soup_paragraph[0].get_text()

#quit browser
    browser.quit()

#open browser
    browser = init_browser()

#next url to be scraped
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(2)

# # Scrape page into Soup
#     html = browser.html
#     soup = bs(html, "html.parser")
    
#find and click links
    browser.links.find_by_partial_text("FULL IMAGE")[0].click()
    time.sleep(5)
    browser.links.find_by_partial_text("more info")[0].click()
    time.sleep(5)

# Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
#use text under figure to find image
    text_soup = soup.find_all("figure", class_= "lede")
    #print(text_soup)
    figure = text_soup[0]
    image_soup = figure.find_all("a", href = True)
    image_soup[0]["href"]

#define feature image url
    featured_image_url = "https://www.jpl.nasa.gov" + image_soup[0]["href"]

#quit browser
    browser.quit()


#open browser
    browser = init_browser()

#read mars table and convert to html
    mars_df = pd.read_html("https://space-facts.com/mars/")
    mars_html_table = mars_df[0].to_html(header=False, index=False)

#quit browser
    browser.quit()

#open browser
    browser = init_browser()

#another url to be scraped    
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    links=browser.links.find_by_partial_text("Hemisphere Enhanced")
    hemisphere_image_urls = []

#create loop to repeat scrape    
    for l in range(len(links)):
        browser.links.find_by_partial_text("Hemisphere Enhanced")[l].click()
        time.sleep(2)
        html = browser.html
        soup = bs(html, 'html.parser')
        downloads = soup.find_all("div", class_= "downloads")
        figure= downloads[0]
        pic_soup = figure.find_all("a", href = True)
        hemisphere={}
        hemisphere["img_url"]= pic_soup[0]["href"]
        titles = soup.find_all("h2", class_= "title")
        title= titles[0]
        hemisphere["title"]= title.get_text()
        hemisphere_image_urls.append(hemisphere)
        browser.back()

#close browser
    browser.quit()

#add everything to dictionary
    mars_data = {
        "Mars_News_Headline": title.get_text(),
        "Mars_News_Article": paragraph,
        "Mars_Featured_Image": featured_image_url,
        "Mars_Facts": mars_html_table,
        "Mars_Hemisphere": hemisphere_image_urls

    }

    return mars_data

#if __name__ == "__main__":
    #data = scrape()
    #print(data)