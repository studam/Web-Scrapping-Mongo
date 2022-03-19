### Import Dependencies
# Setup 
#-----------------------------
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager



def scrape():

    # Set up Splinter 
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    # When you’ve finished testing, close your browser using browser.quit:

    # Create a empty dictionary to store the data
    #----------------------------------------------
    scraped_data = {}

    # Visit the Mars News Site
    #---------------------------------------------
    Mars_News_Site = ('https://redplanetscience.com/')
    browser.visit(Mars_News_Site)


    # Create HTML object 
    #---------------------
    html = browser.html

    # Parse HTML with BeautifulSoup 
    #---------------------------------------------
    bsoup = BeautifulSoup(html, 'html.parser')

    # Get the first list of headlines containing the latest news title and paragraph text 
    #------------------------------------------------------------------------------------------
    first_div = bsoup.select_one('div.list_text')

    # Save the news title under the <div> tag with a class of 'content_title' 
    #--------------------------------------------------------------------------
    news_title = first_div.find('div', class_='content_title').get_text()

    # Save the paragraph text under the <div> tag with a class of 'article_teaser_body' 
    #-----------------------------------------------------------------------------------
    news_p = first_div.find('div', class_='article_teaser_body').get_text()

    # Create a dictionary with the scraped data
    #---------------------------------------------------------
    Nasa_News = {"Title":news_title, "Paragraph": news_p}

    # Save the scraped data to an entry of the dictionary
    #----------------------------------------------------
    scraped_data["Title"] = news_title
    scraped_data["Paragraph"] = news_p

    # Visit the JPL Featured Space Image website 
    #-----------------------------------------------
    JPL_image = 'https://spaceimages-mars.com'
    browser.visit(JPL_image)

    # Featured image is in the div class="carousel_container"
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    html = browser.html

    # Parse HTML with BeautifulSoup 
    #-------------------------------------------
    soup = BeautifulSoup(html, 'html.parser')

    # find the relative image url
    img_url_rel = soup.find('img', class_='fancybox-image').get('src')

    full_address = "https://spaceimages-mars.com/"+ img_url_rel

    # URL
    #--------------------------------------------------------
    url_mars_facts = "https://galaxyfacts-mars.com/"

    # Pandas to scrape any table data from a page
    #-----------------------------------------------
    tables = pd.read_html(url_mars_facts)

    # Select the intended table
    #-------------------------------
    table_facts = tables[0]

    # Convert the data to a HTML table string
    #---------------------------------------------------
    scraped_data["TableHTML"] = table_facts.to_html()

    # URL
    #--------------------------------------------------------------------------------------------------------------
    url_mars_hemispheres = "https://marshemispheres.com/"

    # Use the browser to visit the url
    #--------------------------------------
    browser.visit(url_mars_hemispheres)

    # Splinter capture a page's underlying html and use pass it to BeautifulSoup to scrape the content
    #-------------------------------------------------------------------------------------------------------------------
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # By analyzing the page we can find that the images are in a div class='description'
    #--------------------------------------------------------------------------------------
    results= soup.find_all('div',class_='description')

    # list with the name of the hemispheres
    #------------------------------------------------
    list_hemispheres = []
    for i in range(len(results)):
        list_hemispheres.append(results[i].a.h3.text)

    list_hemispheres

    hemisphere_image_urls = []

    # Create a list of dictionaries for each hemisphere
    for i in range(len(list_hemispheres)):

        # Use the browser to visit the url
        browser.click_link_by_partial_text(list_hemispheres[i])
        
        # Splinter can capture a page's underlying html and use pass it to BeautifulSoup to allow us to scrape the content
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        # By analyzing the page we can find that the images link are in a li
        results_new = soup.find_all('li')

        # Append the dictionary with the image url string and the hemisphere title to a list.
        for n in range(len(results_new)):
            if results_new[n].a.text == 'Sample':
                hemisphere_image_urls.append({"title": list_hemispheres[i].replace("Hemisphere Enhanced", 'Hemisphere'), "img_url": url_mars_hemispheres+results_new[0].a['href']})
                
        # Use the browser to visit the url
        browser.visit(url_mars_hemispheres)

    # Create a dictionary with the scraped data
    DSD = {"ListImages": hemisphere_image_urls}  

    # Save the scraped data to an entry of the dictionary
    scraped_data["ListImages"] = hemisphere_image_urls

    # When you’ve finished testing, close your browser using browser.quit:
    browser.quit()

    # The scraped data is available on the dictionary form
    return scraped_data