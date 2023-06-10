import requests

def crawl_page(url,file_exts=None,keywords=None):
    """
    given a web page url -
    and optional list of file exts and keywords -
    crawl page for matching files
    and return download urls
    """
    # get page
    page = requests.get(url)

    
