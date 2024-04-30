import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import tldextract
from textProcessor import *

stopwordSet = {"a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
               "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
               "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
               "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
               "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have",
               "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers",
               "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've",
               "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more",
               "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only",
               "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't",
               "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than",
               "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's",
               "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to",
               "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've",
               "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who",
               "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll",
               "you're", "you've", "your", "yours", "yourself", "yourselves"}

valid_domains = {".ics.uci.edu", ".cs.uci.edu", ".informatics.uci.edu", ".stat.uci.edu"}

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
