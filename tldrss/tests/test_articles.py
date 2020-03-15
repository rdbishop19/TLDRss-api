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

    @patch('django.utils.timezone.now', lambda: '2020-03-06T05:34:55.663133Z')
    def setUp(self):
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

    # https://docs.python.org/3/library/unittest.mock.html
    @patch('django.utils.timezone.now', lambda: '2020-03-06T05:34:55.663133Z')
    def test_get(self):
        '''Test we can get a list of articles'''

        # list view - part 1
        response = self.client.get('/article')
        # make sure the list view returns a 1-length array
        self.assertEqual(len(response.data['results']), 1)

        # detail view
        response = self.client.get('/article/1')

        # valid endpoint response
        self.assertEqual(response.status_code, 200)
        # make sure the content matching how we need it to look above
        self.assertEqual(json.loads(response.content), TEST_CONTENT[0])

        # invalid entry
        bad_response = self.client.get(
            reverse('article-detail', kwargs={"pk": 2})
        )
        self.assertEqual(bad_response.status_code, 404)
    
    @patch('django.utils.timezone.now', lambda: '2020-03-06T05:34:55.663133Z')
    def test_cant_post_duplicate_article(self):
        '''Test duplicate articles aren't allowed in db'''

        duplicate_article = {
            "title": 'COVID-19', 
            "description": 'Up-to-date news on coronavirus',
            "link": 'https://www.who.int/',
            "feed_id": 1,
            "pub_date": '2020-03-13T05:34:55.663133Z'
        }

        # make sure the prev article is found
        response = self.client.get(
            reverse('article-detail', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 200)

        # make sure prev article matches duplicate_article
        prev_article = Article.objects.filter(link=duplicate_article['link']).values()[0]
        self.assertEqual(duplicate_article['title'], prev_article['title'])
        self.assertEqual(duplicate_article['link'], prev_article['link'])
        # self.assertEqual(duplicate_article['pub_date'], prev_article['pub_date'])

        # make sure a post returns 500 using the duplicate article
        response = self.client.post(
            reverse('article-list'), duplicate_article, content_type="application/json"
        )
        self.assertEqual(response.status_code, 500)

    def test_pagination_length(self):
        '''Test the pagination limit is working'''

        # list view - part 2
        new_articles = 25
        pagination_length = 25
        for i in range(new_articles):
            Article.objects.create(
            title='COVID-19', 
            description=f'Up-to-date news on coronavirus-{1}',
            link=f'https://www.who.int/{i}',
            feed_id=1,
            pub_date='2020-03-13T05:34:55.663133Z'
        )

        response = self.client.get(reverse('article-list'))
        self.assertEqual(len(response.data['results']), pagination_length)