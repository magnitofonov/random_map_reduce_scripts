#!/usr/bin/env python
import sys

class Mapper:
    def run(self):
    	for line in sys.stdin:
	    lower = unicode(line, "utf-8").lower()
	    cleaned = ''.join(c for c in lower if (c.isalnum() or c==' ') and not c.isnumeric())
	    words = cleaned.split()
	    for word in words:
        	print ('%s\t%d' % (word, 1)).encode("utf-8")

class Reducer:
	def run(self):
		cur_word = None
		cur_count = 0

		for line in sys.stdin:
		    data = unicode(line, "utf-8").split('\t')
		    word = data[0]
		    count = int(data[1])

		    if cur_word == word:
		        cur_count += count
		    else:
		        if cur_word:
		            print ('%s\t%d' % (cur_word, cur_count)).encode("utf-8")
		        cur_count = count
		        cur_word = word

		print ('%s\t%d' % (cur_word, cur_count)).encode("utf-8")


if __name__ == "__main__":
    mr_func = sys.argv[1]
    if mr_func == "map":
        mapper = Mapper()
        mapper.run()
    elif mr_func == "reduce":
        reducer = Reducer()
        reducer.run()