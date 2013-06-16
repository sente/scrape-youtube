import lxml
import lxml.html
from pattern.web import Link, URL


urls = ['http://www.youtube.com/user/GoogleDevelopers/about',
        'http://www.youtube.com/user/ajannasmom/about']


classnames = ['branded-page-related-channels-content',
              'channel-summary-list-item']


def get_links(html, url):

    print url
    classnames = ['branded-page-related-channels-content',
                  'channel-summary-list-item']
    res = []
    for c in classnames:
        res.extend(get_side_bar_urls(html=html, url=url, classname=c))

    return res

def get_side_bar_urls(html, url, classname):
    print 'calling get_side_bar_urls'
    if html:
        root = lxml.html.fromstring(html)
    elif url.startswith('http'):
        root = lxml.html.parse(url).getroot()
        root.make_links_absolute()
    #elif len(url) > 100:
    #    root = lxml.html.fromstring(url)
    #else:
    #    root = None

    res = []
    for foo in  root.xpath("//*[contains(@class, '{0}')]".format(classname)):
        for a in foo.xpath(".//a/@href"):
            new_url = a + '/about'
            res.append(Link(new_url, referrer=url))
    return res



def get_side_bar_urls2(url):
    root = lxml.html.parse(url).getroot()
    root.make_links_absolute()

    for foo in  root.xpath("//*[contains(@class, 'channel-summary-list-item')]"):
        for a in foo.xpath(".//a/@href"):
            print a



if __name__ == '__main__':
    for u in urls:
        print '\n\n'
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





