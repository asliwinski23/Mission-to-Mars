# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

# Run all scraping functions and store results in dictionary
    news_title, news_paragraph = mars_news(browser)

    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "mars_cerebrus_url": mars_hemi_img(browser)[0]['img_url'],
      "mars_cerebrus_title": mars_hemi_img(browser)[0]['title'],
      "mars_schiaparelli_url": mars_hemi_img(browser)[1]['img_url'],
      "mars_schiaparelli_title": mars_hemi_img(browser)[1]['title'],
      "mars_syrtis_major_url": mars_hemi_img(browser)[2]['img_url'],
      "mars_syrtis_major_title": mars_hemi_img(browser)[2]['title'],
      "mars_valles_marineris_url": mars_hemi_img(browser)[3]['img_url'],
      "mars_valles_marineris_title": mars_hemi_img(browser)[3]['title']
    }

    # quit the browser amd return data
    browser.quit()
    return data


# ### Article scraping
def mars_news(browser):
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

    try: 
        slide_elem = news_soup.select_one('div.list_text')

        # find the title of the most recent article in slide_elem
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # ^ calling get_text() without an argument is the same as .text

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


# ### Image scraping
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


# ### Fact table scraping
def mars_facts():
    try:
        # use pandas to read HTML
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # assign columns and set index of dataframe 
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # make the dataFrame back into HTML
    return df.to_html(classes ="table table-striped")


### Mars hemisphere images scraping
def mars_hemi_img(brow):

    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

     # Use browser to visit the URL 
    url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'
    browser.visit(url)
    
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


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())