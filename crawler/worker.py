from threading import Thread

from collections import defaultdict
from urllib.parse import urlparse
from inspect import getsource
from utils.download import download
from utils import get_logger
import scraper
import time


def update_new_unique_url(new_url, visited_urls):
    new_base_url = urlparse(new_url)._replace(fragment='').geturl()
    # print(new_base_url)
    if not new_base_url in visited_urls:
        visited_urls.append(new_base_url)
    return visited_urls

def count_subdomains(urls):
    subdomain_counts = defaultdict(int)
    subdomain_pages = defaultdict(set)

    for url in urls:
        parsed_url = urlparse(url)
        if parsed_url.netloc.endswith('.ics.uci.edu'):
            subdomain = parsed_url.netloc.split('.')[0]
            subdomain_counts[subdomain] += 1
            subdomain_pages[subdomain].add(parsed_url.geturl())

    subdomain_info = []
    for subdomain, count in sorted(subdomain_counts.items()):
        subdomain_info.append(f"http://{subdomain}.ics.uci.edu, {count}")

    return subdomain_info

class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        self.longest_word_count = None #Longest URL word count
        self.longest_url = None # The actual URL
        self.every_visited_urls = [] # This stores every visited Urls
        self.unique_visited_urls = []
        self.subdomain_info = []
        # basic check for requests in scraper
        assert {getsource(scraper).find(req) for req in {"from requests import", "import requests"}} == {-1}, "Do not use requests in scraper.py"
        assert {getsource(scraper).find(req) for req in {"from urllib.request import", "import urllib.request"}} == {-1}, "Do not use urllib.request in scraper.py"
        super().__init__(daemon=True)
        
    def run(self):
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                the_string = f"Longest_word_count: {self.longest_word_count}\nLongest_url: {self.longest_url}"
                self.logger.info(the_string)

                self.subdomain_info = count_subdomains(every_visited_urls)
                for info in self.subdomain_info:
                    self.logger.info(info)
                break
            if tbd_url in self.every_visited_urls:
                continue
            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
            scraped_urls, word_count = scraper.scraper(tbd_url, resp)

            self.every_visited_urls.append(tbd_url)
            self.unique_visited_urls = update_new_unique_url(tbd_url, self.unique_visited_urls)

            if self.longest_word_count == None or word_count >= self.longest_word_count:
                self.longest_url = tbd_url
            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)
            self.frontier.mark_url_complete(tbd_url)
            time.sleep(self.config.time_delay)
