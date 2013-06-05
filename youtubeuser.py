# -*- coding: utf-8 -*-

import lxml
import lxml.html
import requests
import sys
import os




class YouTubeUser(object):

    content = None


    def __init__(self, *args, **kwargs):

        assert(len(args) == 1)
        parm = args[0]
        if os.path.isfile(parm):
            content = self._from_file(parm)
        elif parm.startswith('http://') or parm.startswith('https://'): 
            content = self._from_web(parm)
        else:
            sys.stderr.write("error: invalid call\n")

        self.content = content



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

        self.featured_channels = featured_channels
        return featured_channels



    def _from_file(self, arg):

        sys.stderr.write("_from_file(\"%s\")\n" % arg)
        content = open(arg,'r').read()
        return content

    def _from_web(self, arg):

        sys.stderr.write("_from_web(\"%s\")\n" % arg)
        content = requests.get(arg).content
        return content



if __name__ == '__main__':

    a = YouTubeUser("http://www.youtube.com/user/ajannasmom/about")

