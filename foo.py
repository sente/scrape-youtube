# -*- coding: utf-8 -*-
import sys
import lxml
import lxml.html
from pattern.web import Link, URL

#def link__repr__(self):
#    return "Link(text=%s)" % repr(self.text)
#Link.__repr__ = link__repr__


def get_links(html, url):

    print url
    classnames = ['branded-page-related-channels-content',
                  'channel-summary-list-item']
    res = []
    for c in classnames:
        for link in get_side_bar_urls(html=html, url=url, classname=c):
            if link not in res:
                res.append(link)
        print '+++++++++++++++++'
        print '\n'.join(map(str,res))
        print  '~~~~~~~~~~~~~~~~~'
    res.append(Link('http://www.youtube.com/user/sentesays/about',referrer=url,text='SENTE'))
    return res

def get_side_bar_urls(html, url, classname):

    print 'getting side by side...'
    def keep(a):
        """ 
        because we want to discard the users which are mentioned within the
        "Subscriptions" grouping...
        """
        print 'tesitng...'

        for parent in list(a.iterancestors()):
            if parent.tag == 'div' and 'about-subscriptions' in parent.get('class',''):
                sys.stderr.write('discarded %s - %s\n' % (a.text_content, a.get('href')))
                return False
        return True

    print 'calling get_side_bar_urls'
    if html:
        root = lxml.html.fromstring(html)
    elif url.startswith('http'):
        root = lxml.html.parse(url).getroot()
        root.make_links_absolute()

    res = []
    for foo in  root.xpath("//*[contains(@class, '{0}')]".format(classname)):
        for a in foo.xpath(".//a"):
            if keep(a):

                text = a.get('href', '').split('/')[-1]
                new_url = a.get('href', '') + '/about'
                link = Link(new_url, referrer=url, text=text)
                res.append(link)

    return res



def get_side_bar_urls2(url):
    root = lxml.html.parse(url).getroot()
    root.make_links_absolute()

    for foo in  root.xpath("//*[contains(@class, 'channel-summary-list-item')]"):
        for a in foo.xpath(".//a/@href"):
            print a



if __name__ == '__main__':

    urls = ['http://www.youtube.com/user/GoogleDevelopers/about',
            'http://www.youtube.com/user/ajannasmom/about']

    classnames = ['branded-page-related-channels-content',
                  'channel-summary-list-item']

    for u in urls:
        print u
        print '\n'.join(map(str,(get_side_bar_urls(u, classnames[0]))))
#        print get_side_bar_urls2(u)
#        for clsname  in classnames:
#            print u
#            print clsname
#            #print get_side_bar_urls(u, clsname)
#            print get_side_bar_urls2(u)
##        print '~~~~~~~~~~~~~~'
#        get_side_bar_urls2(u)





