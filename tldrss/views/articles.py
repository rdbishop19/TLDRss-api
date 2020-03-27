# from rest_framework.viesets import Viewset
# from django.http import HttpResponseServerError
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response

from django.db import IntegrityError

from django.db.models import Count, F, ExpressionWrapper, Func, IntegerField,  FloatField
from django.db.models.functions import Now

from tldrss.models import Article
from tldrss.views.feeds import FeedSerializer
from tldrss.views.custom_pagination import CustomPagination

class JulianDay(Func):
    function = ''
    output_field = IntegerField()

    def as_postgresql(self, compiler, connection):
        self.template = "CAST (to_char(%(expressions)s, 'J') AS INTEGER)"
        return self.as_sql(compiler, connection)

    def as_sqlite(self, compiler, connection):
        self.template = 'julianday(%(expressions)s)'
        return self.as_sql(compiler, connection)

class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    '''
        JSON serializer for RSS article

        Arguments:
            serializers.HyperLinkedModelSerializer
    '''
    feed = FeedSerializer()
    upvote_count = serializers.SerializerMethodField()
    # upvotes = serializers.HyperlinkedModelSerializer(many=True)
    class Meta:
        model = Article
        # defining the `url` field is not actually needed like we did in class.
        # Inherited serializer base class knows to look for `id` field
        url = serializers.HyperlinkedIdentityField(
            view_name='article',
            lookup_field='id'
        )
        fields = ('id', 'url', 'title', 'link', 'description',
                  'pub_date', 'created_at', 'feed', 'upvote_count')

    def get_upvote_count(self, obj):
        return obj.upvotes.count()

class ArticleViewSet(viewsets.ModelViewSet):
    '''ViewSet for RSS articles'''
    queryset = Article.objects.all()
    # queryset = Article.objects.annotate(relevant=Count('upvotes')).order_by('relevant')
    serializer_class = ArticleSerializer
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        '''Handle POST

        Returns:
            Response == JSON serialized Article instance
        '''

        # obj, created = Article.objects.get_or_create(**request.data)
        try:
            article = Article.objects.create(**request.data)
            serializer = ArticleSerializer(
                article, context={'request': request})
            return Response(serializer.data)
        except IntegrityError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        ''' Handle GET for all article elements

        Returns:
            Response == JSON serialized Article list
        '''

        articles = Article.objects.all()

        sort = request.query_params.get('sort', None)
        relevant = request.query_params.get('relevant', None)
        if sort == 'true':
            articles = articles.annotate(Count('upvotes', distinct=True)).order_by('-upvotes')
            if relevant == 'true':
                #### https://stackoverflow.com/questions/38707848/query-annotation-with-date-difference
                articles = Article.objects.annotate(relevant=Count('upvotes')) \
                    .annotate(diff=(JulianDay(Now())-JulianDay(F('pub_date')))) \
                    .annotate(relevance=ExpressionWrapper(((Count('upvotes'))/((F('diff')+2)**1.8)), output_field=FloatField())).order_by(F('relevance').desc(nulls_last=True))

        coronavirus = request.query_params.get('coronavirus', None)
        if coronavirus == 'true':
            articles = articles.filter(title__icontains='corona') | Article.objects.filter(description__icontains='corona') | \
                Article.objects.filter(title__icontains='covid') | Article.objects.filter(description__icontains='covid')

        search = request.query_params.get('search', None)
        if search:
            articles = articles.filter(title__icontains=search) | articles.filter(description__icontains=search) | \
                articles.filter(title__icontains=search) | articles.filter(description__icontains=search)

        feed = request.query_params.get('feed', None)
        if feed:
            articles = articles.filter(feed_id=feed)

        custom = request.query_params.get('custom', None)
        if custom:
            articles = articles.filter(feed_id__subscriptions__user=request.auth.user)

        saved = request.query_params.get('saved', None)
        if saved:
            articles = articles.filter(user_saves__user=request.auth.user)

        favorites = request.query_params.get('favorites', None)
        if favorites:
            articles = articles.filter(upvotes__user=request.auth.user)

        usersummaries = request.query_params.get('usersummaries', None)
        if usersummaries:
            articles = articles.filter(summary__user=request.auth.user)

        page = self.paginate_queryset(articles)
        serializer = ArticleSerializer(
            page,
            many=True,
            context={'request': request}
        )

        # https://stackoverflow.com/questions/31785966/django-rest-framework-turn-on-pagination-on-a-viewset-like-modelviewset-pagina
        return self.get_paginated_response(serializer.data)
