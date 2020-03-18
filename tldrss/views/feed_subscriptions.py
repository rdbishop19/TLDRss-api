# imports
from rest_framework import serializers
from rest_framework import viewsets

from ..models import FeedSubscription
from ..views.feeds import FeedSerializer
from ..views.users import UserSerializer
# serializer
class FeedSubscriptionSerializer(serializers.HyperlinkedModelSerializer):
    '''Feed subscription serializer'''
    user = UserSerializer()
    feed = FeedSerializer()

    class Meta:
        model = FeedSubscription
        fields = '__all__'
# viewset
class FeedSubscriptionViewSet(viewsets.ModelViewSet):
    '''Feed subscription viewset'''

    queryset = FeedSubscription.objects.all()
    serializer_class = FeedSubscriptionSerializer