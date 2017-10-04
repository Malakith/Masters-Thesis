"""This is for scraping the output of each url"""

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from multiprocessing import Pool
from cache.cache import NoneCache


class AbstractWebScraper(object):
    """This is an abstract web scraper, that can output the html of a page
    in a certain way.
    """
    def get_soup(self, address):
        """This method is just supposed to return the souped version of
         the page that the addresss points to.
         """
        raise NotImplementedError("Should be implemented by concrete")

    def get_soups(self, addresses):
        """This method does the same as get soup, but takes a list of
        addresses and returns a list of soups.
        """
        raise NotImplementedError("Should be implemented by concrete")


class PureBSScraper(AbstractWebScraper):
    """This is a concrete implementation which only uses beautiful soup."""
    VALID_TAGS = ['div', 'p']

    def __init__(self):
        self.cache = NoneCache()

    def get_soup(self, address):
        """ Just gets the souped version of the html for the page the
        address refers to.
        :param address: A single address
        :return: the soup.
        """
        if not address.startswith("http"):
            address = "https://"+address
        cval = self.cache.lookup(address)
        if cval is not None:
            return cval
        r = requests.get(address)
        soup = BeautifulSoup(r.text, "lxml")
        self.cache.save(address, soup)
        return soup

    def get_soups(self, addresses):
        """
        This method is an expansion of the one above, handling a list of
        addresses and making the requests asyncronously.

        :param addresses: a list of addresses.
        :return: a list of soups.
        """
        with Pool(5) as p:
            result = p.map_async(self.get_soup, addresses)
            result.wait()
            return result.get()


class SeleniumScraper(AbstractWebScraper):
    """This is a concrete implementation which uses Selenium"""
    def __init__(self):
        """Since we are using selenium, we need to instantiate a driver."""
        self.driver = webdriver.Firefox()
        self.cache = NoneCache()

    def get_soup(self, address):
        """
        This method just gets the soup matching a single address.
        :param address: A string address, which doesnt have to start with http://
        :return: A soup - a representation of the html on the page.
        """
        if not address.startswith("http"):
            address = "http://"+address
        cval = self.cache.lookup(address)
        if cval is not None:
            return cval
        self.driver.get(address)
        soup = BeautifulSoup(self.driver.page_source)
        self.cache.save(address, soup)
        return soup

    def get_soups(self, addresses):
        """
        This method takes a list of addresses and returns the soups belonging to those addresses.
        :param addresses: A list of addresses. They need not start with http://
        :return: A list of soups, in the same order as the input addresses.
        """
        soups = []
        for addr in addresses:
            soups.append(self.get_soup(addr))
        return soups
