"""This is for getting google search results.
The same can be achieved with the google custom search api but it costs money.
Might be changed to use the api, when project has gotten further.
"""

from selenium import webdriver
from ..cache.cache import NoneCache


class GoogleSearch:
    """It creates the webdriver when initialized. Should be closed when done.

    An example of use:
    s = GoogleSearch()
    urls = s.get_urls_for_query("potato chips", 200)
    s.close()
    """
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.cache = NoneCache()

    def close(self):
        self.driver.close()

    """Queries google for search results until it has gathered n urls."""
    def get_urls_for_query(self, query, n):
        query = query.replace(" ", "+")
        cVal = self.cache.lookup(query + "+" + str(n))
        if cVal is not None:
            return cVal
        result = []
        while len(result) < n:
            self.driver.get("https://www.google.dk/search?q="+query+"&num=100&start="+str(len(result)))
            results = self.driver.find_elements_by_class_name("r")
            for r in results:
                try:
                    result.append(r.find_element_by_css_selector("a").get_attribute("href"))
                except:
                    pass
        self.cache.save(query + "+" + str(n), result[:n])
        return result[:n]


# An example of use:

