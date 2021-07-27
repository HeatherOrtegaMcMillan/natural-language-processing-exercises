# acquire.py for webscraping 
from requests import get
from bs4 import BeautifulSoup
import os
import pandas as pd

############ for getting variables for codeup blog articles
############ run before doing get blog articles, could combine into one function for automation
def get_info_for_codeup_blogs():
    '''
    This function is for storing and returning the website list
    title finder info
    and body finder info
    For scraping data from codeup blog posts
    '''
    
    website_list = ['https://codeup.com/codeups-data-science-career-accelerator-is-here/',
                'https://codeup.com/data-science-myths/',
                'https://codeup.com/data-science-vs-data-analytics-whats-the-difference/',
                'https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/',
                'https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/']

    # all titles are under jupiterx-post-header (header class)

    title_finder = 'jupiterx-post-header'

    # all body text is under jupiterx-post-content (div class)

    body_finder = 'jupiterx-post-content'
    
    return website_list, title_finder, body_finder


############# for acquiring codeup blog articles 
def get_blog_articles():
    '''
    This function takes in a list of website urls, 
    the title finder and body finder (must be the same for each article)
    And returns a list of dictionaries with title text and body text in dictionaries
    Keys in dictionaries are 'title' and 'content'
    '''
    
    websites, title_finder, body_finder = get_info_for_codeup_blogs()
    
    # initalize empty list for the dictionaries
    article_list = []
    
    # set up headers
    headers = {'User-Agent': 'Codeup Data Science'} 
    
    # loop through list of websites
    for website in websites: 
        
        # get response
        response = get(website, headers=headers)
    
        # create soup object
        soup = BeautifulSoup(response.text, features="lxml")
        # find title
        #title = soup.find('header', class_=title_finder).text
        title = soup.title.string
    
        # find body
        body = soup.find('div', class_=body_finder).get_text(strip=True)
        #body = soup.get_text(strip=True)
        
        # create dictionary
        dictionary = {'title': title,
                     'content': body}
        
        # add dictionary to list of dictionaries
        article_list.append(dictionary)
        
    return pd.DataFrame(article_list)

############ creates urls from a baseurl and different endpoints
########### used inside the get_blog_articles2 function

def create_urls(base_url, categories):
    '''
    This function takes in a baseurl and list of categories
    It will create a new list with the base url a / and each category
    
    This is for scraping info from the inshorts website
    
    Returns dataframe of Titles, Articles, and Categories
    '''
    
    website_list = [base_url + '/' + category for category in categories]
    
    return website_list

############## function for getting the title and contents from blog articles

def get_blog_articles2(base_url = 'https://inshorts.com/en/read', categories = ['sports', 'entertainment', 'business', 'technology']): # title_finder, body_finder
    '''
    This function takes in a list of website urls, 
    the title finder and body finder (must be the same for each article)
    And returns a list of dictionaries with title text and body text in dictionaries
    Keys in dictionaries are 'title' and 'content'
    '''

    # initalize empty list for the dictionaries
    article_list = []
    
    # set up headers
    headers = {'User-Agent': 'Codeup Data Science'} 
    
    # create list of websites using the categories
    website_list = create_urls(base_url, categories)
    
    # loop through list of websites and category list
    for website, category in zip(website_list, categories): 
        
        # get response
        response = get(website, headers=headers)
    
        # create soup object
        soup = BeautifulSoup(response.text, features="lxml")
        
        # find titles
        headlines= soup.find_all('span', itemprop = 'headline')
        
        # find bodies 
        bodies = soup.find_all('div', itemprop = 'articleBody')
        
        # loop through length of headlines (could also be bodies) use index to get text and add to dictionary
        for i in range(len(headlines)):
            title = headlines[i].get_text()
            body = bodies[i].get_text()
            
            # create dictionary
            dictionary = {'title': title,
                         'content': body,
                         'category': category}
            
            # add dictionary to list of dictionaries
            article_list.append(dictionary)
        
    return pd.DataFrame(article_list)