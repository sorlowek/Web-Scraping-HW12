#import beautiful soup and splinter
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time

def init_browser():
# @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser = init_browser()
# Visit the NASA news URL
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(10)

# Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #get news title
    news_title = soup.find("div",class_="content_title").text

    #get news paragraph
    news_paragraph = soup.find("div", class_="article_teaser_body").text

    #store as dictionary
    mars_news = {
        "news_title": news_title,
        "news_paragraph": news_paragraph
    }
    #Visit image url
    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_image)
    time.sleep(10)

    #scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image = soup.find("img", class_="thumb")["src"]

    #store
    img_url = "https://jpl.nasa.gov"+image


    #Visit mars twitter
    url_mars_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_mars_weather)
    time.sleep(10)

    #scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    #get tweet
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    weather_tweet = {
        "Mars Weather Tweet": mars_weather
    }

    #Visit mars facts page
    url_mars_facts = "https://space-facts.com/mars/"
    browser.visit(url_mars_facts)
    time.sleep(10)

    #store
    facts_table = pd.read_html(url_mars_facts)[0]
    facts_table.columns = ["Description", "Values"]
    facts_table.set_index(["Description"],inplace=True)


    #Visit Mars Hemisphere's page
    url_mars_hems = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_mars_hems)
    time.sleep(10)

    #scrap page into soup
    hem_html = browser.html
    hem_soup = BeautifulSoup(hem_html,'html.parser')

    #get titles/links
    results = hem_soup.find_all('h3')

    #Create a list
    mars_hems_list=[]

    # Loop through returned results
    for result in results:
        
        # image title
        title_text = result.text
        
        #image_link
        browser.click_link_by_partial_text(title_text)
        hem_htmls = browser.html
        hem_soup = BeautifulSoup(hem_htmls, "html.parser")
        url = hem_soup.find('a', target='_blank').get("href")
        mars_hems_list.append({'title': title_text, 'URL': url})
        browser.click_link_by_partial_text('Back')

    final_mars_data ={}
    final_mars_data["Mars_News"] = mars_news
    final_mars_data["Mars_Feat_Image"] = url_image
    final_mars_data["Mars_Weather"] = weather_tweet
    final_mars_data["Mars_Facts"] = facts_table
    final_mars_data["Mars_Hemispheres"] = mars_hems_list


    # Close the browser after scraping
    browser.quit()

    # Return results
    return final_mars_data