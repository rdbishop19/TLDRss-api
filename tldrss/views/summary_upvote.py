from rest_framework.viewsets import ViewSet
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

# from django.contrib.auth.models import User
# from django.http import HttpResponseServerError
# from django.db.models import Count
from django.db import IntegrityError

from ..models import SummaryUpvote


class SummaryUpvoteSerializer(serializers.HyperlinkedModelSerializer):
    '''JSON serializer for upvotes

    Arguments:
        serializers.HyperLinkedModelSerializer
    '''

    class Meta:
        model = SummaryUpvote
        url = serializers.HyperlinkedIdentityField(
            view_name='article_upvote',
            lookup_field='id',
        )

        fields = '__all__'


class SummaryUpvoteViewSet(viewsets.ModelViewSet):
    '''Article upvotes basic view'''

    queryset = SummaryUpvote.objects.all()
    serializer_class = SummaryUpvoteSerializer

    def create(self, request, *args, **kwargs):
        '''Handle POST

        Returns:
            Response == JSON serialized instance
        '''

        try:
            new_upvote = SummaryUpvote()
            new_upvote.summary_id = request.data['summary_id']
            new_upvote.user_id = request.auth.user.id
            new_upvote.save()

            serializer = SummaryUpvoteSerializer(
                new_upvote, context={'request': request}
            )
            return Response(serializer.data)
        except IntegrityError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)      

