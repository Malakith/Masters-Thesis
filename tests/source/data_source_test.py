import unittest
from texttomodel.source.parser import SimpleHTMLParser
from texttomodel.source.scrape import PureBSScraper
from texttomodel.source.trends import KeyList
from bs4 import BeautifulSoup

import spacy

class KeyListUnitTest(unittest.TestCase):
    def test_adding_level1(self):
        keys = KeyList(1)
        self.assertEqual(len(keys.keys), 0, "Should have no keys.")
        keys.add_prime_key("test")
        self.assertListEqual([["test"]], keys.keys, "Should contain the test string on level 1.")

        keys.add_prime_key("test2")
        self.assertListEqual([["test"], ["test2"]], keys.keys, "Should contain both test strings on level 1.")

    def test_adding_level2(self):
        keys = KeyList(2)
        keys.add_prime_key("test1")
        keys.add_prime_key("test2")
        keys.add_prime_key("test3")
        self.assertEqual(len(keys.keys), 6)
        self.assertEqual(keys.keys, [["test1"],  ["test1", "test2"], ["test2"], ["test1", "test3"],  ["test2", "test3"], ["test3"]])

    def test_adding_level3(self):
        keys = KeyList(3)
        keys.add_prime_key("test1")
        keys.add_prime_key("test2")
        keys.add_prime_key("test3")
        self.assertEqual(len(keys.keys), 7)
        self.assertEqual(keys.keys, [["test1"], ["test1", "test2"], ["test2"], ["test1", "test3"], ["test1", "test2", "test3"], ["test2", "test3"], ["test3"]])

    def test_adding_level3_non_prime(self):
        keys = KeyList(3)
        keys.add_prime_key("prime1")
        keys.add_prime_key("prime2")
        keys.add_key("nonPrime1")
        keys.add_key("nonPrime2")
        print(keys.keys)
        self.assertEqual(len(keys.keys), 11)

    def test_google_trends_lookup(self):
        keys=KeyList(3)
        keys.add_prime_key("calendar event")
        keys.add_prime_key("date")
        keys.add_prime_key("duration")
        keys.add_prime_key("participant")
        keys.add_prime_key("location")
        keys.get_queries()
        for q in keys.keys.queries:
            print(q)
        print(len(keys.keys.queries))
        self.assertTrue(True)


class SimpleHTMLParserTest(unittest.TestCase):
    def test_parse1(self):
        scr = PureBSScraper()
        soup = scr.get_soup("https://en.wikipedia.org/wiki/Algebra")
        parser = SimpleHTMLParser()
        title, texts = parser.parse_html(soup)
        print(title, texts)
        self.assertTrue(True)




