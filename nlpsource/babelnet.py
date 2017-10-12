from pprint import PrettyPrinter
from cachecontrol import CacheControlAdapter
from cachecontrol.caches.file_cache import FileCache
from requests import Session

import config as cfg

printer = PrettyPrinter(indent=4)


class BabelNet(Session):
    def __init__(self, filename=""):
        super(BabelNet, self).__init__()
        if filename == "":
            filename = "babelnet_cache"
        self.mount('https://', CacheControlAdapter(cache=FileCache(filename)))
        self.headers.update({'Accept-Encoding': 'gzip'})
        self.params.update({'key': cfg.babelnet_key})
        self.endpoint = "https://babelnet.io/v4/"

    def get_synset_ids(self, word, pos=None, source=None, normalizer=False):
        params = {'word': word,
                  'langs': 'EN',
                  'pos': pos,
                  'source': source,
                  'normalizer': normalizer,
                  }
        r = self.get(self.endpoint + "getSynsetIds", params=params)
        return [synset['id'] for synset in r.json()]

    def get_synset(self, synset_id):
        params = {
            'id': synset_id,
        }
        r = self.get(self.endpoint + "getSynset", params=params)
        return r.json()

    def get_senses(self, word, pos=None, source=None, normalizer=False):
        params = {
            'word': word,
            'lang': 'EN',
            'pos': pos,
            'source': source,
            'normalizer': normalizer,
        }
        r = self.get(self.endpoint+"getSenses", params=params)
        return r.json()

    def get_edges(self, synset_id):
        params = {
            'id': synset_id,
        }
        r = self.get(self.endpoint+"getEdges", params=params)
        return r.json()

    def get_ym(self, synset_id, ym):
        result = []
        edges = self.get_edges(synset_id)
        for edge in edges:
            group = edge['pointer']['relationGroup']
            if group == ym:
                result.append(edge)
        return result

    def get_hyponyms(self, synset_id):
        return self.get_ym(synset_id, 'HYPONYM')

    def get_hypernyms(self, synset_id):
        return self.get_ym(synset_id, 'HYPERNYM')

    def get_meronym(self, synset_id):
        return self.get_ym(synset_id, 'MERONYM')

    def get_holonym(self, synset_id):
        return self.get_ym(synset_id, 'HOLONYM')

    def get_other(self, synset_id):
        return self.get_ym(synset_id, 'OTHER')