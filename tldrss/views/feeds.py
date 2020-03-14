from rest_framework import viewsets
from rest_framework import serializers

from tldrss.models import Feed

class FeedSerializer(serializers.HyperlinkedModelSerializer):
    '''
        JSON serializer for RSS Feed sources

        Arguments:
            serializers.HyperlinkedModelSerializer
    '''

    class Meta:
        model = Feed
        url = serializers.HyperlinkedIdentityField(
            view_name='feed',
            lookup_field='id'
        )
        fields = '__all__'

class FeedViewSet(viewsets.ModelViewSet):
    '''Feed viewset'''

    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
