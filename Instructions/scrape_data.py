from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
import pandas as pd
information = {}


def Scrape():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")

    chrome_driver = os.getcwd() +"\\chromedriver.exe"
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)

    driver.get('https://mars.nasa.gov/news/')
    time.sleep(2)
    base_class = driver.find_element_by_class_name('slide')
    time.sleep(2)
    information['news_title'] = base_class.find_element_by_class_name("content_title").text
    information['news_p'] = base_class.find_element_by_class_name("list_text").find_element_by_class_name("article_teaser_body").text

    driver.get('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

    Full_Url = driver.find_element_by_class_name("carousel_item").get_attribute('style')
    information['featured_image_url'] = 'https://www.jpl.nasa.gov' + ((Full_Url.split('"'))[1].split('"')[0])

    driver.get('https://twitter.com/marswxreport?lang=en')

    time.sleep(2)
    Unfinished_Information = driver.find_element_by_css_selector("div[data-testid='tweet']").text
    information['mars_weather'] = 'InSight' + ((Unfinished_Information.split('InSight'))[1].split('hPa')[0]).replace("\n","") + 'hPa'

    url_facts = "https://space-facts.com/mars/"
    time.sleep(2)
    table = pd.read_html(url_facts)
    table[0]

    marsFacts = table[0]
    marsFacts.columns = ["Parameter", "Values"]
    finishedFacts = marsFacts.set_index(["Parameter"])
    html = finishedFacts.to_html()
    html = html.replace("\n", "")
    information["Mars_Facts"] = html

    # VHM = {"title": "Valles Marineris Hemisphere", "img_url": Hemisphere('Valles Marineris Hemisphere',driver)}
    # time.sleep(2)
    # CH  = {"title": "Cerberus Hemisphere", "img_url": Hemisphere('Cerberus Hemisphere',driver)}
    # time.sleep(2)
    # SH  = {"title": "Schiaparelli Hemisphere", "img_url": Hemisphere('Schiaparelli Hemisphere',driver)}
    # time.sleep(2)
    # SMH = {"title": "Syrtis Major Hemisphere", "img_url": Hemisphere('Syrtis Major Hemisphere',driver)}
    # information["hemisphere_image_urls"] = [VHM, CH, SH, SMH]

    driver.quit()

    return information

def Hemisphere(surface,driver):
    driver.get('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    time.sleep(2)
    driver.find_element_by_css_selector("img[alt*='" + surface + "']").click()
    hem_link = driver.find_element_by_tag_name("li").find_element_by_css_selector("a[target*='_blank']").get_attribute('href')
    return hem_link
