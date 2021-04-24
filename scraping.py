# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Article scraping

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# With the above line, browser.is_element_present_by_css('div.list_text', wait_time=1), we are accomplishing two things.

# One is that we're searching for elements with a specific combination of tag (div) and attribute (list_text). 
# As an example, ul.item_list would be found in HTML as <ul class="item_list">.

# Secondly, we're also telling our browser to wait one second before searching for components. The optional delay is useful 
# because sometimes dynamic pages take a little while to load, especially if they are image-heavy.

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

# find the title of the most recent article in slide_elem
news_title = slide_elem.find('div', class_='content_title').get_text()
# ^ calling get_text() without an argument is the same as .text
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Image scraping

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Fact table scraping

# use pandas to read HTML
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# make the dataFrame back into HTML
df.to_html()

# quit the browser
browser.quit()

