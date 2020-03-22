# imports
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError

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

    def create(self, request, *args, **kwargs):
        '''Handle POST of new user feed subscription'''

        try:
            new_subscription = FeedSubscription()
            new_subscription.feed_id = request.data['feed_id']
            new_subscription.user_id = request.auth.user.id
            new_subscription.save()
            
            serializer = FeedSubscriptionSerializer(
                new_subscription, context={'request': request})
            return Response(serializer.data)
        except IntegrityError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)