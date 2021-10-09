#!/usr/bin/env python
# coding: utf-8

# In[4]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from IPython import get_ipython


# In[5]:


# Path to chromedriver
get_ipython().system('where chromedriver')


# In[6]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[7]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[8]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[9]:


slide_elem.find('div', class_='content_title')


# In[10]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[11]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[12]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[13]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[14]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[15]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[16]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[17]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[18]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[19]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[20]:



# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[21]:


# Assign the main_url
main_url = 'https://astrogeology.usgs.gov/'

# Parse the HTML with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[22]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

# Results returned as an iterable list
results = img_soup.find_all('div', class_='item')

# Loop through returned results
for result in results:
    
    # Retrieve the titles
    title = result.find('h3').text
    
    # Get the link to go the full image site
    img_url = result.find('a')['href']
    
    # Creating the full_img_url
    full_img_url = main_url + img_url
    
    # Use browser to go to the full image url and set up the HTML parser
    browser.visit(full_img_url)
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    # Retrieve the full image urls
    hemisphere_img = img_soup.find('div',class_='downloads')
    hemisphere_full_img = hemisphere_img.find('a')['href']
    
    # Printing hemisphere_full_img
    print(hemisphere_full_img)
    
    # Creating hemispheres dict
    hemispheres = dict({'img_url':hemisphere_full_img, 'title':title})
  
    #Append the hemisphere_image_urls list
    hemisphere_image_urls.append(hemispheres)


# In[23]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[24]:



# 5. Quit the browser
browser.quit()


# In[ ]:




