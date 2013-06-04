import lxml
import lxml.html
import sys


def get_featured_channels(filename):
    root = lxml.html.fromstring(open(filename).read())

    div = None
    for h2 in root.xpath('//h2'):
        if h2.text_content().strip() == "Featured Channels":
            div = h2.getparent()
            break

    if div is None:
        return []

    featured_channels = []
    for a in div.xpath('.//ul/li/a'):
        featured_channels.append(a.get('href'))

    return featured_channels

if __name__ == '__main__':
    filename = sys.argv[1]
    featured_channels = get_featured_channels(filename)
    for f in featured_channels:
        print f





