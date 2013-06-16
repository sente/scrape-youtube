from pattern.web import Spider


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
            print 'WILL CRAWL %s' % link.url
            return True
        else:
            print 'IGNORING  %s' % link.url
            return False

#    def parse(self, html):
#       return get_links(html)

s = Spiderling(links=['http://www.youtube.com/user/ajannasmom/about'], domains=['www.youtube.com'], delay=0, parser=get_links)

for i in range(20):
    print i
    print s.crawl()
    print s.GRAPH
    print '\n\n\n'

#print s.crawl()
#print s.crawl()
#print s.crawl()


#while not s.done:
#    print s.crawl
#    s.crawl(cached=False, throttle=5)
