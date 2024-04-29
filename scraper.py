import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def scraper(url, resp):
    links, word_count = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)], word_count

def extract_next_links(url, resp):
    global last_accessed
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    all_links = []

    if resp.status == 200 and resp.raw_response and resp.raw_response.content: #check if the status is 200 and whether there're contents inside raw_response

        parsedHTML = BeautifulSoup(resp.raw_response.content, 'html.parser') #parse the HTML
        text_content = parsedHTML.get_text() #Get the text
        word_count = len(text_content.split()) # See if we need to crawl the website


        if word_count > 100: # Avoid useless pages

            for anchor_tag in parsedHTML.find_all('a', href = True):

                the_link = anchor_tag['href'] #grab relative link

                joined_link = urljoin(url, the_link) #Join absolute link

                if 'ics.uci.edu' not in joined_link: #filter out links that are not in ics.uci.edu domain
                    continue

                all_links.append(joined_link)
        

    return all_links, word_count

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    excluded_formats = [
    '.css', '.js', '.bmp', '.gif', '.jpg', '.jpeg', '.ico', '.png', '.tiff', '.mid', '.mp2',
    '.mp3', '.mp4', '.wav', '.avi', '.mov', '.mpeg', '.ram', '.m4v', '.mkv', '.ogg', '.ogv', '.pdf',
    '.ps', '.eps', '.tex', '.ppt', '.pptx', '.doc', '.docx', '.xls', '.xlsx', '.names', '.data',
    '.dat', '.exe', '.bz2', '.tar', '.msi', '.bin', '.7z', '.psd', '.dmg', '.iso', '.epub', '.dll',
    '.cnf', '.tgz', '.sha1', '.thmx', '.mso', '.arff', '.rtf', '.jar', '.csv', '.rm', '.smil', '.wmv',
    '.swf', '.wma', '.zip', '.rar', '.gz', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
                               '.zip', '.rar', '.mp3', '.mp4', '.avi', '.mov', '.wmv',
                               '.jpg', '.jpeg', '.png', '.gif', '.exe', '.msi', '.iso', '.bin', '.php'
] #every file formats that should be excluded

    try:
        parsed = urlparse(url)._replace(fragment='') # replace fragment to look for unique hyperlinks
        if parsed.scheme not in set(["http", "https"]): #exclude not https
            return False
        if any(parsed.path.lower().endswith(ext) for ext in excluded_formats): #see whether the url ends with excluded format
            return False
        
        if parsed.netloc in [
            "www.ics.uci.edu",
            "www.cs.uci.edu",
            "www.informatics.uci.edu",
            "www.stat.uci.edu"
        ]: #
            return True
        
        return False


        # return not re.match(
        #     r".*\.(css|js|bmp|gif|jpe?g|ico"
        #     + r"|png|tiff?|mid|mp2|mp3|mp4"
        #     + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
        #     + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
        #     + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
        #     + r"|epub|dll|cnf|tgz|sha1"
        #     + r"|thmx|mso|arff|rtf|jar|csv"
        #     + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
