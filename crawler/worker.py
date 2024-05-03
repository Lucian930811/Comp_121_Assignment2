from threading import Thread

from collections import defaultdict
from urllib.parse import urlparse
from inspect import getsource
from utils.download import download
from utils import get_logger
import scraper
import time

class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        #self.longest_word_count = None #Longest URL word count
        #self.longest_url = None # The actual URL
        #self.every_visited_urls = [] # This stores every visited Urls
        #self.unique_visited_urls = []
        #self.subdomain_info = []
        # basic check for requests in scraper
        assert {getsource(scraper).find(req) for req in {"from requests import", "import requests"}} == {-1}, "Do not use requests in scraper.py"
        assert {getsource(scraper).find(req) for req in {"from urllib.request import", "import urllib.request"}} == {-1}, "Do not use urllib.request in scraper.py"
        super().__init__(daemon=True)
        
    def run(self):
		counter = 0
        while True:
			counter = counter + 1
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                scraper.printFinalResult()
                self.logger.info("Frontier is empty. Stopping Crawler.")
                #the_string = f"Longest_word_count: {self.longest_word_count}\nLongest_url: {self.longest_url}"
                #self.logger.info(the_string)

                #self.subdomain_info = count_subdomains(every_visited_urls)
                #for info in self.subdomain_info:
                #   self.logger.info(info)
                break
            #if tbd_url in self.every_visited_urls:
            #    continue
			if counter > 5000:
				scraper.printFinalResult()
				counter = 0
            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
            scraped_urls = scraper.scraper(tbd_url, resp)

            #self.every_visited_urls.append(tbd_url)
            #self.unique_visited_urls = update_new_unique_url(tbd_url, self.unique_visited_urls)

            #if self.longest_word_count == None or word_count >= self.longest_word_count:
            #    self.longest_url = tbd_url
            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)
            self.frontier.mark_url_complete(tbd_url)
            time.sleep(self.config.time_delay)
