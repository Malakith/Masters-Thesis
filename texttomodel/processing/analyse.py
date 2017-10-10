from multiprocessing import Queue
from collections import defaultdict


def get_sentence_stats(span):
    result = defaultdict(lambda: 0)
    for t in span:
        i = t.vocab.strings[t.text]
        result[i] = result[i]+1
    return result
