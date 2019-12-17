def scrape():

    #import dependencies
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from splinter import Browser
    import pandas as pd
    import requests
    import time
    import re


    # # 1. NASA MARS NEWS
    #target news url
    news_url = 'https://mars.nasa.gov/news'

    #open browser & scrape HTML
    driver = webdriver.Chrome()
    driver.get(news_url)
    time.sleep(1)
    news_soup = BeautifulSoup(driver.page_source, features='lxml')

    #find & save tag
    news_headline = news_soup.find('div', class_='content_title').text
    news_teaser = news_soup.find('div', class_='article_teaser_body').text


    # # 2. JPL MARS IMAGE
    #target image URL
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    #open browser
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(jpl_url)
    jpl_button = browser.find_by_id('full_image')
    jpl_button.click()

    #scrape HTML and close browser
    jpl_soup = BeautifulSoup(browser.html, 'html.parser')
    browser.quit()

    #find tag
    jpl_image = jpl_soup.find('article', class_='carousel_item')
    jpl_fullimage = jpl_image['style']
    jpl_regex = re.search( 'spaceimages/images/wallpaper/\w+-\d+\w\d+.jpg', jpl_fullimage)

    #save tag
    featured_image_url = f'http://jpl.nasa.gov/{jpl_regex.group()}'


    # # 3. MARS WEATHER
    #target weather URL
    weather_url = 'https://twitter.com/marswxreport'

    #open browser and scrape HTML
    weather_request = requests.get(weather_url)
    weather_soup = BeautifulSoup(weather_request.text, 'html.parser')

    #find tag
    mars_weather = weather_soup.find('p', class_='TweetTextSize').text
    tweet_tail = re.search('pic.twitter.com/\w+', mars_weather)

    #format & save tag
    mars_tweet = mars_weather.replace(tweet_tail.group(), "")


    # # 4. MARS FACTS
    #target table URL
    facts_url = 'https://space-facts.com/mars/'

    #scrape, format, and save table
    facts_read = pd.read_html(facts_url)
    facts_table = facts_read[0].to_html()


    # # 5. MARS HEMISPHERES
    #target images URL
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    #open broswer & scrape root html
    driver.get(hemi_url)
    hemi_soup = BeautifulSoup(driver.page_source, features='lxml')

    #find and store individual anchors
    hemi_links = hemi_soup.find_all('a', class_='product-item')

    #loop through anchors for text
    hemi_names = []
    for x in range(len(hemi_links)):
        #every other link is the target text
        if x%2 == 1:
            
            #split the hemisphere name
            hemi_split = hemi_links[x].text.split()        
            hemi_holder = []
            
            #removes "enhanced"
            for y in hemi_split:
                if y != "Enhanced":
                    hemi_holder.append(y)
            
            hemi_names.append(" ".join(hemi_holder))

    #loop through individual pages and save url names
    hemi_images = []
    for j in range(4):
        d_url = "https://astrogeology.usgs.gov" + hemi_links[j]['href']
        d_request = driver.get(d_url)
        d_soup = BeautifulSoup(driver.page_source, features='lxml')
        d_link = d_soup.find('a', text="Sample")
        hemi_images.append(d_link['href'])

    #close browser
    driver.quit()

    #assemble title & url dictionary
    hemi_dict = []
    for z in range(4):
        hemi_dict.append({'title': hemi_names[z], 'img_url': hemi_images[z]})



    # 6. FINAL CONTENT OUTPUT
    content = {
        "news_headline": news_headline,
        "news_summary": news_teaser,
        "featured_image": featured_image_url,
        "weather": mars_tweet,
        "facts": facts_table,
        "hemi_n": hemi_dict,
        "hemi_i": hemi_images
    }

    # 7. RETURN
    return content