from datetime import datetime

from django.http import HttpResponseServerError
from django.db.models import Count, F, ExpressionWrapper, Func, FloatField, IntegerField

# from rest_framework import viewsets
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from tldrss.models import Summary
from tldrss.views.users import UserSerializer

class Epoch(Func):
    '''Create an SQL 'EXTRACT' fuction template'''
    function = 'EXTRACT'
    template = "%(function)s('epoch' from %(expressions)s)"

class SummarySerializer(serializers.HyperlinkedModelSerializer):
    '''Serializer for user-submitted summaries (tl;dr)'''
    user = UserSerializer()
    upvote_count = serializers.SerializerMethodField()
    class Meta:
        model = Summary
        # exclude = ['user']
        fields = ('id', 'url', 'user', 'upvote_count', 'summary_text', 'created_on', 'updated_on', 'article')

    def get_upvote_count(self, obj):
        return obj.upvotes.count()

class SummaryViewSet(viewsets.ModelViewSet):
    '''Viewset for article summaries 'tl;dr's'''
    queryset = Summary.objects.all()
    serializer_class = SummarySerializer

    # def retrieve(self, request, pk=None):
    #     '''get one item'''

    #     try:
    #         summary = Summary.objects.get(pk=pk)
    #         serializer = SummarySerializer(summary, context={'request': request})
    #         return Response(serializer.data)
    #     except Exception as ex:
    #         return HttpResponseServerError(ex)

    def list(self, request, *args, **kwargs):
        '''custom list method with filters'''

        summaries = Summary.objects.annotate(relevant=Count('upvotes')) \
                    .annotate(diff=(Epoch(datetime.utcnow() - F('created_on'))/3600)) \
                    .annotate(relevance=ExpressionWrapper(((Count('upvotes'))/(((F('diff'))+2)**1.8)), output_field=FloatField())) \
                    .order_by(F('relevance').desc(nulls_last=True))

        user_only = request.query_params.get('user', False)
        article_id = request.query_params.get('article', None)

        if article_id:
            summaries = summaries.filter(article_id=article_id)

        if user_only == "true":
            user = request.auth.user
            summaries = summaries.filter(user_id=user.id)

        page = self.paginate_queryset(summaries)
        serializer = SummarySerializer(
            page,
            many=True,
            context={'request': request}
        )
        # https://stackoverflow.com/questions/31785966/django-rest-framework-turn-on-pagination-on-a-viewset-like-modelviewset-pagina
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        '''Handle POST'''

        new_summary = Summary()
        new_summary.article_id = request.data['article_id']
        new_summary.user_id = request.auth.user.id
        new_summary.summary_text = request.data['summary_text']

        new_summary.save()

        serializer = SummarySerializer(new_summary, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single user-submitted summary
        Returns:
            Response -- 200, 404, or 500 status code
        """

        try:
            summary = Summary.objects.get(pk=pk, user=request.auth.user)
            summary.delete()

            return Response([], status=status.HTTP_204_NO_CONTENT)

        except Summary.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def partial_update(self, request, pk=None):
        '''Handle PATCH'''
        
        summary = Summary.objects.get(pk=pk)
        summary.summary_text = request.data['summary_text']
        # summary.edited_on = request.data['edited_on']

        summary.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


