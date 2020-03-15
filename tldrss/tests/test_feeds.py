import json
from unittest.mock import patch
from django.test import TestCase
from tldrss.models import Article, Feed
from rest_framework.reverse import reverse
from datetime import datetime

TEST_CONTENT = [
    {
        'url': 'http://testserver' + reverse('feed-detail', kwargs={'pk': 1}),
        'name': 'World Health Organization (WHO)',
        'feed_url': 'https://www.who.int/feeds/entity/csr/don/en/rss.xml'
    }
]

class FeedEndpointTestCase(TestCase):
    '''RSS Feed sources'''
    maxDiff = None

    def setUp(self):
        Feed.objects.create(
            name='World Health Organization (WHO)',
            feed_url='https://www.who.int/feeds/entity/csr/don/en/rss.xml'
        )

        # article = Article.objects.create(
        #     title='COVID-19', 
        #     description='Up-to-date news on coronavirus',
        #     link='https://www.who.int/',
        #     feed_id=feed.id,
        #     # created_at='2020-03-06T05:34:55.663133Z',  # don't need this with @patch
        #     pub_date='2020-03-13T05:34:55.663133Z'
        # )

    def test_get(self):
        '''test we can get a feed source and its attributes'''

        response = self.client.get(
            reverse('feed-detail', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(json.loads(response.content), TEST_CONTENT[0])

    def test_post(self):
        '''test we can create a new feed source'''

        # appended `TEST_NEW` so feed_url is different from setUp
        new_rss_source = {
            'name': 'World Health Organization (WHO)',
            'feed_url': 'https://www.who.int/feeds/entity/csr/don/en/rss.xml/TEST_NEW'
        }

        response = self.client.post(
            reverse('feed-list'), new_rss_source, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

    def test_cant_post_duplicate_feed_source(self):
        '''test we cant create a feed source with the same url as a previous one'''

        new_rss_source = {
            'name': 'World Health Organization (WHO)',
            'feed_url': 'https://www.who.int/feeds/entity/csr/don/en/rss.xml'
        }

        # first make sure the previous entry has the same url as the new entry
        response = self.client.get(
            reverse('feed-detail', kwargs={'pk': 1})
        )
        self.assertEqual(json.loads(response.content)['feed_url'], TEST_CONTENT[0]['feed_url'])

        # now do a POST with the matching URL and make sure it returns http 400
        response = self.client.post(
            reverse('feed-list'), new_rss_source, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
