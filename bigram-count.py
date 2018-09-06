#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# cat data.txt | python bigram-count.py map ru | sort -k1,1 | python bigram-count.py reduce > output.txt
#
import sys
import re
from itertools import groupby
from operator import itemgetter

class Mapper:

    re_en = re.compile(ur"[a-z]+")
    re_ru = re.compile(ur"[а-яё]+")

    def __init__(self, lang):
        if lang == "en":
            self.re = Mapper.re_en
        else:
            self.re = Mapper.re_ru
        self.results = {}

    def run(self):
        doc_count = 0
        data = self.readInput()
        for docid, contents in data:
            text = contents.lower()
            prev_word = None
            word_count = 0
            for match in self.re.finditer(text):
                word = match.group(0)
                if prev_word is not None:
                    self.addResult(prev_word, word)
                prev_word = word
                word_count += 1
            sys.stderr.write("reporter:counter:MyCounters,InputWords,%d\n" % word_count)
            doc_count += 1
            if doc_count % 1000 == 0:
                self.emitResults()
                sys.stderr.write("reporter:status:Processed %d documents\n" % doc_count)        
        self.emitResults()

    def readInput(self):
        for line in sys.stdin:
            yield unicode(line, 'utf8').strip().split('\t', 1)

    def addResult(self, w1, w2):
        if len(w1) > 2 and len(w2) > 2:
            if w1 not in self.results:
                self.results[w1] = {}
            w1_counts = self.results[w1]
            if w2 not in w1_counts:
                w1_counts[w2] = 1
            else:
                w1_counts[w2] += 1

    def emitResults(self):
        for w1, counts in self.results.iteritems():
            for w2, count in counts.iteritems():
                print ('%s+%s\t%d' % (w1, w2, count)).encode('utf-8')
        self.results = {}


class Reducer:

    def run(self):
        data = self.readInput()
        for bigram, group in groupby(data, itemgetter(0)):
            total_count = sum(int(count) for bigram, count in group)
            print ('%s\t%d' % (bigram, total_count)).encode('utf-8')

    def readInput(self):
        for line in sys.stdin:
            yield unicode(line, 'utf8').strip().split('\t', 1)


if __name__ == "__main__":
    mr_func = sys.argv[1]
    if mr_func == "map":
        lang = sys.argv[2]
        mapper = Mapper(lang)
        mapper.run()
    elif mr_func == "reduce":
        reducer = Reducer()
        reducer.run()

