import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from textProcessor import *
from collections import defaultdict

LARGE_FILE_SIZE = 5 * 1024 * 1024

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

#Global data structure
all_urls = set()
all_tokens = defaultdict(int)
longest_page = ''
longest_length = 0

def scraper(url, resp):
    result = []
    global all_urls
    links = extract_next_links(url, resp)
    for link in links:
        if is_valid(link):
            result.append(link)
            all_urls.add(link)
    return result

def extract_next_links(url, resp):
    global all_tokens, longest_page, longest_length
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content

    result = []
    #Check if the status is 200 (OK)
    if resp.status == 200:
        # Detect and avoid dead URLs that return a 200 status but no data
        if len(resp.raw_response.content) == 0:
            return result
        # Detect and avoid crawling very large files
        fileSize = int(resp.raw_response.headers.get('Content-Length', 0))
        if fileSize > LARGE_FILE_SIZE:
            return result

        # Parse the HTML, create a list of tokens
        parsedHTML = BeautifulSoup(resp.raw_response.content, 'html.parser')
        text_content = parsedHTML.get_text()
        tokenList = tokenize(text_content)

        if len(tokenList) > longest_length:
            longest_length = len(tokenList)
            longest_page = url

        # Check High value information content (Definition: Token > 200)
        if len(tokenList) > 200:
            # Add token that are not stopword into the global token dictionary
            for token in tokenList:
                if token not in stopwordSet:
                    all_tokens[token] += 1
            # Get all URL in this page
            for anchor_tag in parsedHTML.find_all('a', href = True):
                the_link = anchor_tag['href']
                if the_link is not None:
                    u = urlparse(the_link)
                    if not u.scheme:
                        the_link = urljoin(url, the_link)  # Join absolute link
                    #Remove fragment and check if it's in all_urls
                    defragment = urlparse(the_link)._replace(fragment='').geturl()
                    if defragment not in all_urls:
                        result.append(defragment)

    #Check if the status is 302 (redirect)
    if resp.status == 302:
        newUrl = resp.raw_response.headers['Location']
        #Might need to check redirect link is relative
        #Remove the fragment part of the URL
        defragment = urlparse(newUrl)._replace(fragment='').geturl()
        #Check if it's already in all_urls
        if defragment not in all_urls:
            result.append(defragment)
            return result

    #Return empty list if neither
    return result

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        #parsed = urlparse(url)._replace(fragment='') # replace fragment to look for unique hyperlinks
        parsed = urlparse(url)
        # exclude not http/https and check if it's in valid domain
        if parsed.scheme not in set(["http", "https"]) or all((domain not in parsed.netloc) for domain in valid_domains):
            return False
        return not re.match(
             r".*\.(css|js|bmp|gif|jpe?g|ico"
             + r"|png|tiff?|mid|mp2|mp3|mp4"
             + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
             + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
             + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
             + r"|epub|dll|cnf|tgz|sha1"
             + r"|thmx|mso|arff|rtf|jar|csv"
             + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise

def printFinalResult():
    # Question 1
    try:
        with open('q1.txt', 'w') as file:
            for url in all_urls:
                file.write(url + '\n')
    except Exception as e:
        print(f"Error writing to file: {e}")

    # Question 2
    try:
        with open('q2.txt', 'w') as file:
            file.write(f'Longest page: {longest_page}\nLongest number of word: {longest_length}\n')
    except Exception as e:
        print(f"Error writing to file: {e}")

    # Question 3
    try:
        with open('q3.txt', 'w') as file:
            sortedTokens = sorted(all_tokens.items(), key=lambda x: (-x[1], x[0]))[:50]
            for token in sortedTokens:
                file.write(f'{token[0]} - {token[1]}\n')
    except Exception as e:
        print(f"Error writing to file: {e}")

    # Question 4
    try:
        with open('q4.txt', 'w') as file:
            file.write("I'm too lazy.")
    except Exception as e:
        print(f"Error writing to file: {e}")