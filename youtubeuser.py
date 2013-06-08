# -*- coding: utf-8 -*-

import lxml
import lxml.html
import requests
import base64
import sys
import os
import gzip
from collections import deque



class YouTubeUser(object):

    content = None
    page = None

    def __init__(self, *args, **kwargs):

        assert(len(args) == 1)
        parm = args[0]
        self.page = parm
        if os.path.isfile(parm):
            content = self._from_file(parm)
        elif parm.startswith('http://') or parm.startswith('https://'): 
            content = self._from_web(parm)
        else:
            parm = "http://www.youtube.com/user/%s/about" % parm
            content = self._from_web(parm)
        self.content = content

        self._process_user()

    def _process_user(self):
        self.get_featured_channels()
        open('data/%s.txt' % self.page, 'w').write('\n'.join(self.featured_channels) + '\n')
        with open('data/%s.dat' % self.page.lower(), 'w') as ofile:
            for fc in self.featured_channels:
                ofile.write("%s\t%s\n" % (self.page.lower(), fc.lower()))

    def get_featured_channels(self):

        root = lxml.html.fromstring(self.content)

        div = None
        for h2 in root.xpath('//h2'):
            if h2.text_content().strip() == "Featured Channels":
                div = h2.getparent()
                break

        if div is None:
            self.featured_channels = []
            return []

        featured_channels = []
        for a in div.xpath('.//ul/li/a'):
            featured_channels.append(a.get('href'))

        #for img in div.xpath('.//img[@class="yt-uix-button-icon yt-uix-button-icon-subscribe"]'):
        #    print img.get('alt')

        featured_channels = [f.split('/')[-1] for f in featured_channels]
        self.featured_channels = featured_channels
        return featured_channels



    def get_featured_channels2(self):

        root = lxml.html.fromstring(self.content)

        div = None
        for h2 in root.xpath('//h2'):
            if h2.text_content().strip() == "Featured Channels":
                div = h2.getparent()
                break

        if div is None:
            self.featured_channels = []
            return []

        featured_channels = []

        features = []
        for li in div.xpath('.//ul/li'):
            feature = {}
            for a in li.xpath('.//a'):
                print a.get('href')
                feature['href'] = a.get('href')
                break
            for img in li.xpath('.//img'):
                alt = img.get('alt')
                if alt.endswith('subscribers'):
                    print alt
                    feature['subscribers'] = alt

            features.append(feature)

        self.featured_channels2 = features
        return features



    def _from_file(self, arg):

        sys.stderr.write("_from_file(\"%s\")\n" % arg)
        content = open(arg,'r').read()
        return content

    def _from_web(self, arg):

        sys.stderr.write("_from_web(\"%s\")\n" % arg)

        # check if we've already cached this page...
        # if so, return the cached page
        cachestr = base64.encodestring(arg).strip() + '.html.gz'
        if os.path.isfile("cache/%s" % cachestr):
            sys.stderr.write("from_cache: %s\n" % cachestr)
            content = gzip.open("cache/%s" % cachestr, "rb").read()
            return content

        # fetch, cache & return the page...
        content = requests.get(arg).content

        sys.stderr.write("%s cached: %s\n" % (arg, cachestr))
        gzip.open("cache/%s" % cachestr, "wb").write(content)
        return content





if __name__ == '__main__':

    #a = YouTubeUser("http://www.youtube.com/user/ajannasmom/about")
    users = open('vloggers.txt').read().strip().split('\n')

    q = deque(users)
    seen = set()

    yts = {}
    while q:
        sys.stderr.write("\n%d items in queue\t%d items in yts\n" % (len(q),len(yts)))
        name = q.popleft()
        if name in seen:
            sys.stderr.write("already seen %s\n" % name)
            continue
        y = YouTubeUser(name)
        yts[name] = y
        seen.add(name)
        q.extend(y.featured_channels)

