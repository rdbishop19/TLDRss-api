import feedparser

class RssAggregator():
    feedurl = ''

    def __init__(self, rss_url):
        self.feedurl = rss_url

    def parse(self):
        print('SOURCE: ', self.feedurl)
        newfeed = feedparser.parse(self.feedurl)
        return newfeed