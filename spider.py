# -*- coding: utf-8 -*-
from pattern.web import Spider
import sys


from foo import *

class Spiderling(Spider):
    considered = {}
    GRAPH = {}
    GRAPH2 = {}

    def visit(self, link, source=None):
        print 'visited:', repr(link.url), 'from:', link.referrer

        try:
            self.GRAPH[link.referrer].append(link.url)
        except:
            self.GRAPH[link.referrer] = [link.url]

    def fail(self, link):
        print 'failed:', repr(link.url)

    def priority(self, url, method):
        """
        this should really be implemented in Spider's __init__()...
        """

        return 0.0

    def follow(self, link):

        try:
            self.GRAPH2[link.referrer].append(link.url)
        except:
            self.GRAPH2[link.referrer] = [link.url]


        if link.url in self.considered:
            self.considered[link.url] += 1
        else:
            self.considered[link.url] = 1

        if 'user' in link.url:
            return True
        else:
            return False


s = Spiderling(links=['http://www.youtube.com/user/ajannasmom/about'],
               domains=['www.youtube.com'],
               parser=get_links,
               sort="filo",
               delay=-1)

#for i in range(20):
#    print i
#    s.crawl(cache=True, throttle=2)
#    print s.visited
#    print s._queue

#print s.crawl()
#print s.crawl()
#print s.crawl()


#while not s.done:
#    print s.crawl
#    s.crawl(cached=False, throttle=5)
