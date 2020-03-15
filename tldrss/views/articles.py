# from rest_framework.viesets import Viewset
# from django.http import HttpResponseServerError
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from django.db import IntegrityError

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
        ### defining the `url` field is not actually needed like we did in class. 
        ### Inherited serializer base class knows to look for `id` field
        fields = ('url', 'title', 'link', 'description', 'pub_date', 'created_at', 'feed')

class ArticleViewSet(viewsets.ModelViewSet):
    '''ViewSet for RSS articles'''
    
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def create(self, request, *args, **kwargs):
        '''Handle POST

        Returns:
            Response == JSON serialized Article instance
        '''

        # obj, created = Article.objects.get_or_create(**request.data)
        try:
            article = Article.objects.create(**request.data)
            serializer = ArticleSerializer(article, context={'request': request})
            return Response(serializer.data)
        except IntegrityError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)