import json
import datetime

from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth.models import User
from tldrss.models import Article, Feed

from rest_framework.reverse import reverse

from tldrss.models import Summary
class SummaryEndpointTestCase(TestCase):
    '''Tests for user-submitted tl;dr summaries'''

    def setUp(self):
        '''Setup for the article summaries'''
        self.user = User.objects.create()

        self.feed = Feed.objects.create(
            name='World Health Organization (WHO)',
            feed_url='https://www.who.int/feeds/entity/csr/don/en/rss.xml'
        )

        self.article = Article.objects.create(
            title='COVID-19', 
            description='Up-to-date news on coronavirus',
            link='https://www.who.int/',
            feed_id=self.feed.id,
            # created_at='2020-03-06T05:34:55.663133Z',  # don't need this with @patch
            pub_date='2020-03-13T05:34:55.663133Z'
        )

        self.summary = Summary.objects.create(
            user=self.user,
            article=self.article,
            summary_text="Test",
        )
    
    def test_get(self):
        '''test we can get a user-submitted summary'''

        response = self.client.get(
            reverse('summary-list')
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)

    def test_post(self):
        '''test we can post a new summary through api'''

        summary_max_length = {
            'user': 1,
            'article': 'http://testserver' + reverse('article-detail', kwargs={'pk': 1}),
            'summary_text': 'test post',
        }

        response = self.client.post(reverse('summary-list'), summary_max_length, content_type="application/json")
        # print(response.data)
        self.assertEqual(response.status_code, 201)

        # make sure both DateTime fields match for initial creation
        self.assertAlmostEqual(response.data['created_on'], response.data['updated_on'])
    
    def test_get_list(self):
        '''test we can get a list of summary items'''

        # create another summary
        Summary.objects.create(
            user_id=1,
            article_id=1,
            summary_text="Test2",
        )
        response = self.client.get(
            reverse('summary-list')
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

    def test_cant_post_summary_longer_than_limit(self):
        '''test user cant go over the length limit of a summary'''

        # create a max_length summary
        lorem_ipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, \
            sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. \
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris \
            nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in \
            reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla \
            pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa \
            qui officia deserunt mollit anim id est laborum."

        summary_max_length = {
            # 'user_id': self.user.id,
            'user': 1,
            # 'user': 'http://testserver' + reverse('user-detail', kwargs={'pk': 1}),
            'article': self.article.id,
            # 'article': 'http://testserver' + reverse('article-detail', kwargs={'pk': 1}),
            'summary_text': lorem_ipsum[:255],
        }

        response = self.client.post(reverse('summary-list'), summary_max_length, content_type="application/json")
        # print(response.data)
        self.assertEqual(response.status_code, 400)

    def test_delete_summmary(self):
        '''test user can delete their summary'''

        summary = Summary.objects.get(pk=1)
        # use the client to send the request and store the response
        response = self.client.delete(
            reverse('summary-detail', kwargs={'pk': summary.id}),
            # reverse('summary-detail', kwargs={'pk': summary.id}), HTTP_AUTHORIZATION='Token ' + str(self.token)
        )
        # response for successful DELETE
        self.assertEqual(response.status_code, 204)

        # product not in db
        response = self.client.get(reverse('summary-list'))
        # response = self.client.get(reverse('summary-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))
        self.assertEqual(len(response.data['results']), 0)

    def test_edit_summary(self):
        '''test user can edit a summary'''

        edited_summary = {
            'summary_text': 'edited summary',
        }

        response = self.client.patch(
            reverse('summary-detail', kwargs={'pk': 1}), edited_summary,
            # reverse('summary-detail', kwargs={'pk': 1}), edited_summary, HTTP_AUTHORIZATION='Token ' + str(self.token),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 204)

        summary = Summary.objects.get()

        # check that the patched data is reflected in the new object
        self.assertEqual(summary.summary_text, "edited summary")
        
        # make sure both DateTime fields no longer match
        self.assertNotEqual(summary.created_on, summary.updated_on)

