#!/usr/bin/env python

"""This module is for interacting with google's trends api."""

from pytrends.request import TrendReq

from ..cache.cache import NoneCache

from multiprocessing import Pool

pytrend = TrendReq(hl='en-US', tz=360)


class KeyList:
    def __init__(self, limit):
        self.limit = limit
        self.keys = []
        self.addedKeys = set()
        self.cache = NoneCache()

    def add_prime_key(self, key):
        if not isinstance(key, list):
            key = [key]
        self.addedKeys.add(key[0])
        self.__add_key(key, True)

    def add_key(self, key):
        if not isinstance(key, list):
            key = [key]
        if key[0] not in self.addedKeys:
            self.addedKeys.add(key[0])
            self.__add_key(key, False)

    def __add_key(self, key, prime):
        newKeys = []
        for k in self.keys:
            if len(k) < self.limit:
                newKeys.append(k+key)
        if prime:
            newKeys.append(key)
        self.keys = self.keys+newKeys

    def get_queries(self):
        queries = []
        with Pool(processes=20) as p:
            res = p.map_async(self.get_queries_from_keywords, self.keys)
            res.wait()
            [queries.extend(r) for r in res.get() if r is not None]
        return queries

    def get_queries_from_keywords(self, keys):
        cVal = self.cache.lookup(keys)
        if cVal is not None:
            return cVal
        pytrend.build_payload([" ".join(keys)], geo="US")
        result = pytrend.related_queries()
        n = len(keys)
        for r in result:
            top = result[r]["top"]
            if top is not None:
                res = []
                for i in range(len(top['query'])):
                    res.append([n, top['query'][i], top['value'][i]])
                self.cache.save(keys, res)
                return res



