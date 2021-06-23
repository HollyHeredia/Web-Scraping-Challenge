# Defining function from work previously done in Jupyter notebook

 # Dependencies
import requests
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
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

    hemi_names = []
    results = soup.find_all('div', class_="collapsible results")
    hemispheres = results[0].find_all('h3')
    for name in hemispheres:
        hemi_names.append(name.text)
    
    thumbnail_results = results[0].find_all('a', href=True)
    thumbnail_links = []
    for thumbnail in thumbnail_results:
        if (thumbnail.img):
            thumbnail_url = 'https://marshemispheres.com/' + thumbnail['href']
            thumbnail_links.append(thumbnail_url)
    
    full_imgs = []
    for url in thumbnail_links:
        browser.visit(url)
        html = browser.html
        soup = bs(html, 'html.parser')
        results = soup.find_all('div', class_='description')
        relative_img_path = results[0].find('a', href=True)
        img_link = 'https://marshemispheres.com/' + relative_img_path['href']
        full_imgs.append(img_link)

    browser.quit()
    
    # Add all to collection
    mars_info = {}
    
    mars_info['news_header'] = header
    mars_info['news_article'] = subheader
    mars_info['featured_image_url'] = featured_image_url
    mars_info['mars_facts'] = mars_facts_table
    mars_info['hemispheres_names'] = hemi_names
    mars_info['full_imgs'] =full_imgs

    return mars_info
print("Scrape complete!")