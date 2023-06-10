import requests
import streamlit as st
from bs4 import BeautifulSoup

# we can only support certain filetypes rn
crawlable_exts = ['pdf','download']
# save $$$
limit = 2

def crawl_page(url,file_exts=None,keywords=None):
    """
    given a web page url -
    and optional list of file exts and keywords -
    crawl page for matching files
    and return download urls
    """
    # keep track of files to download
    get_list = []
    # return name, content, ext payload list
    payload = []
    # no url will be given on page load
    if url:
        if 'http' not in url and 'https' not in url:
            url = 'http://' + url
        # get page
        page = requests.get(url).content
        # parse with beautiful soup
        soup = BeautifulSoup(page,'html.parser')
        # get links on page
        links = soup.find_all('a')
        # get pdf links
        for link in links:
            # check if ext is in accept list
            for href_ext in crawlable_exts:
                # check if this link contains href to acceptable ext
                if 'href' in link.attrs and href_ext in link.attrs['href']:
                    # if so get it
                    get_list.append(link.attrs['href'])
       
        # keep track of how many files you've scraped
        counter = 0
        # get the acceptable links we've collected
        for link in get_list:
            # file name
            name = link.split('/')[-1]
            # file ext
            ext = name.split('.')[-1]
            # hack TODO use .html or .txt if it's not a supported ext
            if 'download' in link:
                ext = 'pdf'
                link = url + link
                link = link.replace('capitol-breach-cases/usao-dc/','')
                print('zyx',link)
            # binary content
            content = requests.get(link).content
            # return as dict
            payload.append({'name':name,'content':content,'ext':ext})
            # increment
            counter += 1
            if counter == limit:
                break
        # zero, one or more file name, content exts
        return payload[0:limit] # save $$$
            
