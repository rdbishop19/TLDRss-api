from rest_framework import viewsets
from rest_framework import serializers
from tldrss.models import Summary

class SummarySerializer(serializers.HyperlinkedModelSerializer):
    '''Serializer for user-submitted summaries (tl;dr)'''

class SummaryViewSet(viewsets.ModelViewSet):
    '''Viewset for article summaries 'tl;dr's'''
    queryset = Summary.objects.all()
    serializer_class = SummarySerializer