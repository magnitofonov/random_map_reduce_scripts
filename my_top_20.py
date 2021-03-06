#!/usr/bin/env python
import sys

class Mapper:

    def __init__(self, count_threshold):
        self.count_threshold = count_threshold

    def run(self):
        data = self.readInput()
        for word, count in data:
            if int(count) > self.count_threshold:
                print ('%s+%s\t' % (word, count)).encode('utf-8')

    def readInput(self):
        for line in sys.stdin:
            yield unicode(line, 'utf8').strip().split('\t', 1)

class Reducer:

    def __init__(self, top_size):
        self.top_size = top_size

    def run(self):
        data = self.readInput()
        cur_word = '1'
        emit_count = 0
        for w1, count in data:
            if cur_word != w1:
                cur_word = w1
                emit_count = 0
            if emit_count < self.top_size:
                print ('%s+%s' % (w1, count)).encode('utf-8')
                emit_count += 1

    def readInput(self):
        for line in sys.stdin:
            yield unicode(line, 'utf8').strip().split('\t')[0].split('+')


if __name__ == "__main__":
    mr_func = sys.argv[1]
    if mr_func == "map":
        count_threshold = int(sys.argv[2])
        mapper = Mapper(count_threshold)
        mapper.run()
    elif mr_func == "reduce":
        top_size = int(sys.argv[2])
        reducer = Reducer(top_size)
        reducer.run()