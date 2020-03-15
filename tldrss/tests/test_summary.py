from django.test import TestCase

from rest_framework.reverse import reverse

class SummaryEndpointTestCase(TestCase):
    '''Tests for user-submitted tl;dr summaries'''
    
    def test_get(self):
        '''test we can get a user-submitted summary'''

        response = self.client.get(
            reverse('summary-list')
        )

        self.assertEqual(response.status_code, 200)