import logging
import time
# from rssfeed.rss_aggregator import RssAggregator
from tldrss.helpers import RssAggregator
from tldrss.models import Feed, Article

LOGGER = logging.getLogger(__name__)

def get_updated_articles() -> None:
    '''
    Method to fetch all feed sources and then check for updated articles
    
    Arguments:
        None
    Returns:
        None
    '''

    LOGGER.info('FETCHING NEW RSS ARTICLES')

    db_feeds = Feed.objects.all()
    entries = []

    for feed in db_feeds:

        rss_object = RssAggregator(feed.feed_url)
        newfeed = rss_object.parse()

        prev_entries = 0
        new_entries = 0

        for feedentry in newfeed.entries:
            try:
                link = feedentry.get('link', '')
                new_entry = Article.objects.get(link=link)
                prev_entries += 1
            except Article.DoesNotExist:
                new_entry = Article()
                date = feedentry.get('published_parsed', '')
                if date:
                    iso_date = time.strftime('%Y-%m-%dT%H:%M:%SZ', date)
                    new_entry.pub_date = iso_date
                else:
                    new_entry.pub_date = None

                new_entry.title = feedentry.get('title', '')
                remove_quotes = new_entry.title.replace('&quot;', '"')
                new_entry.title = remove_quotes
                remove_apostrophe = new_entry.title.replace("&#39;", "\'")
                new_entry.title = remove_apostrophe
                remove_ampersand = new_entry.title.replace('&amp;', "&")
                new_entry.title = remove_ampersand
                new_entry.link = feedentry.get('link', '')
                new_entry.description = feedentry.get('description', '')
                new_entry.feed_id = feed.id
                new_entry.save()

                entries.append(new_entry)

                LOGGER.info('NEW TITLE: %s', new_entry.link)
                new_entries += 1

        LOGGER.info(
            'SUMMARY: %(feed)s PREVIOUS: %(prev)s NEW: %(new)s', \
            {"feed": feed.name, "prev": prev_entries, "new": new_entries}
        )