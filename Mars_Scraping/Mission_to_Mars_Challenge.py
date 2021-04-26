# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# Visit the mars nasa news site
url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base url to create an absolute url
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# ### Mars Facts

df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
df.head()
df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df
df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres
# 1. Use browser to visit the URL 
url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'

browser.visit(url)

def mars_img():
    
    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Write code to retrieve the image urls and titles for each hemisphere.
    
    # get titles
    html = browser.html
    test_soup = soup(html, 'html.parser')
    # slide_element = test_soup.select_one('img')
    image_title = test_soup.find_all('h3')
    for title in image_title:
        title = title.get_text()
        if title != 'Back':
            hemi_dict = {}
            hemi_dict['title'] = title
            hemisphere_image_urls.append(hemi_dict)
    
    # set counter for image urls loop
    counter = 0
    
    for t in range (0,4):
        
        browser.visit(url)

        hemi_image_elem = browser.find_by_tag('h3')[t]
        hemi_image_elem.click()
        
        html = browser.html
        img_soup = soup(html, 'html.parser')
        a_tags_img_soup = img_soup.find_all('a')
        
        for tag in a_tags_img_soup:
            if tag.get_text() == 'Sample':
                href_img = tag['href']
                img_url = f'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/{href_img}'
                hemisphere_image_urls[counter]['img_url'] = img_url
                counter += 1
                
    return hemisphere_image_urls




# Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# Quit the browser
browser.quit()

