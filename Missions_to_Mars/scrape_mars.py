# Defining function from work previously done in Jupyter notebook

 # Dependencies
import requests
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager

Def scrape:
    # Initialize PyMongo to work with MongoDBs
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    # Define database and collection
    db = client.mars
    collection = db.articles

    # Setup splinter
    executable_path = {'executable_path': r'\Users\holly\.wdm\drivers\chromedriver\win32\91.0.4472.101\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Mars News
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    header = soup.find('div', class_='content_title').text
    subheader = soup.find('div', class_='article_teaser_body').text

    # Mars Image
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    html = browser.html
    soup = bs(html, 'html.parser')

    img_url = soup.find('img',class_="fancybox-image").get("src")
    featured_image_url = url + img_url  
    featured_image_url

    # Mars Facts
    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)
    df = tables[1]
    df.columns=['Description', 'Values']
    mars_facts_table = df.to_html()

    # Mars Hemispheres
    url = 'https://marshemispheres.com/index.html'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')