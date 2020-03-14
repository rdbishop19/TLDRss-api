import json
from django.test import TestCase, Client
from tldrss.models import Article, Feed
from rest_framework.reverse import reverse

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
            created_at='2020-03-06T05:34:55.663133Z',
            pub_date='2020-03-13T05:34:55.663133Z'
        )

        response = client.get('/article/1')
        response.data.pop('created_at', None)
        # print(response)
        # print(response.content, TEST_CONTENT[0])
        self.assertEqual(response.status_code, 200)
        print(response.content, TEST_CONTENT[0])
        self.assertEqual(json.loads(response.content), TEST_CONTENT[0])