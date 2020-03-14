# from rest_framework.viesets import Viewset
# from django.http import HttpResponseServerError
from rest_framework import viewsets
from rest_framework import serializers

from tldrss.models import Article
from tldrss.views.feeds import FeedSerializer

class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    '''
        JSON serializer for RSS article

        Arguments:
            serializers.HyperLinkedModelSerializer
    '''
    feed = FeedSerializer()
    class Meta:
        model = Article
        
        fields = '__all__'
        # exclude = ['feed']

class ArticleViewSet(viewsets.ModelViewSet):
    '''ViewSet for RSS articles'''
    
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer