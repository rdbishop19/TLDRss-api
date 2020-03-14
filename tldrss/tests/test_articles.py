import json
from unittest.mock import patch
from django.test import TestCase, Client
from tldrss.models import Article, Feed
from rest_framework.reverse import reverse
from datetime import datetime

TEST_CONTENT = [
    {
        # 'id': 1,
        'url': 'http://testserver' + reverse('article-detail', kwargs={'pk': 1}),
        'title': 'COVID-19',
        'description': 'Up-to-date news on coronavirus',
        'link': 'https://www.who.int/',
        'feed': {
            'url': 'http://testserver' + reverse('feed-detail', kwargs={'pk': 1}),
            'name': 'World Health Organization (WHO)',
            'feed_url': 'https://www.who.int/feeds/entity/csr/don/en/rss.xml'
        },
        'created_at': '2020-03-06T05:34:55.663133Z',
        'pub_date': '2020-03-13T05:34:55.663133Z'
    }
]

class ArticleEndpointTestCase(TestCase):
    '''RSS Articles'''
    maxDiff = None

    # https://docs.python.org/3/library/unittest.mock.html
    @patch('django.utils.timezone.now', lambda: '2020-03-06T05:34:55.663133Z')
    def test_get(self):
        '''Test we can get a list of articles'''
        client = Client()

        feed = Feed.objects.create(
            name='World Health Organization (WHO)',
            feed_url='https://www.who.int/feeds/entity/csr/don/en/rss.xml'
        )

        article = Article.objects.create(
            title='COVID-19', 
            description='Up-to-date news on coronavirus',
            link='https://www.who.int/',
            feed_id=feed.id,
            # created_at='2020-03-06T05:34:55.663133Z',  # don't need this with @patch
            pub_date='2020-03-13T05:34:55.663133Z'
        )
        # list view
        response = client.get('/article')
        # make sure the list view returns a 1-length array
        self.assertEqual(len(response.data['results']), 1)

        # detail view
        response = client.get('/article/1')
        
        # valid endpoint response
        self.assertEqual(response.status_code, 200)
        # make sure the content matching how we need it to look above
        self.assertEqual(json.loads(response.content), TEST_CONTENT[0])

        # invalid entry
        bad_response = client.get('article/2')
        self.assertEqual(bad_response.status_code, 404)