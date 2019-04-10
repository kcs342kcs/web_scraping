from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import re

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:\\Users\\kcs34\\AppData\\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    output_dict = {}

    # Get top mars news story from nasa
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    # Get the title and teaser from the top mars story

    ln = soup.find('div', class_='content_title')
    lp = soup.find('div', class_='article_teaser_body')
    output_dict['news_title'] = ln.text
    output_dict['news_info'] = lp.text

    # Get the featured mars image

    url1 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    base_url = 'https://www.jpl.nasa.gov'
    browser.visit(url1)
    time.sleep(1)
    html1 = browser.html
    soup1 = bs(html1,'html.parser')
    pic = soup1.find('article', class_='carousel_item')
    first_part = pic['style'].split('\'')
    featured_image = (base_url + first_part[1])
    output_dict['featured_image'] = featured_image

    # Get the latest mars weather

    url2 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url2)
    time.sleep(1)
    html2 = browser.html
    soup2 = bs(html2,'html.parser')
    pic1 = soup2.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    regexPattern = '^InSight sol.*'
    for x in pic1:
        if (re.match(regexPattern,x.text)):
            pic12 = x.text.split('hPapic.twitter.com')
            output_dict['mars_weather'] = pic12[0]
            break
    
    # get some mars trivia

    url3 = "https://space-facts.com/mars/"
    browser.visit(url3)
    time.sleep(1)
    html3 = browser.html
    soup3 = bs(html3,'html.parser')
    facts = soup3.find_all('div', id='facts')
    mars_trivia=[]
    for fact in facts:
        f = fact.find_all('li')
        for i in f:
            try:
                mars_trivia.append(i.text.strip('\\n'))
            except:
                print('bad')
    output_dict['mars_trivia'] = mars_trivia

    # get mars table data
    table = pd.read_html(url3)
    table[0].columns=['Description','Value']
    table[0].set_index('Description',inplace=True)
    mars_table = table[0].to_html()
    output_dict['mars_table'] = mars_table

    #Get hemisphere pics and titles
    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    part_url = 'https://astrogeology.usgs.gov'
    browser.visit(url4)
    time.sleep(1)
    html4 = browser.html
    soup4 = bs(html4,'html.parser')
    hemi = soup4.find_all('div', class_='description')
    h_data = {}
    h_final_data = []

    # find the links to the hemi pics
    for h in hemi:
        hpic = h.find('a')
        pic_title = h.find('h3')
        get_pic = (part_url + hpic['href'])
        h_data[pic_title.text] = get_pic

    # get the url's for the hemi pics
    for v in h_data.keys():
        browser.visit(h_data[v])
        time.sleep(1)
        tmp_html = browser.html
        tmp_soup = bs(tmp_html,'html.parser')
        tmp_dat = tmp_soup.find_all('div', class_='downloads')

        for final in tmp_dat:
            li_f = final.find('li')
            h_final_data.append({'title':v,'link':li_f.a['href']})

    output_dict['hemispheres'] = h_final_data



    # Close the browser after scraping
    browser.quit()

    #Return results
    return output_dict