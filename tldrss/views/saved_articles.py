# imports
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError

from ..models import SavedArticle
from ..views.articles import ArticleSerializer
from ..views.users import UserSerializer
# serializer
class SavedArticleSerializer(serializers.HyperlinkedModelSerializer):
    '''Feed subscription serializer'''
    user = UserSerializer()
    article = ArticleSerializer()

    class Meta:
        model = SavedArticle
        fields = '__all__'
# viewset
class SavedArticleViewSet(viewsets.ModelViewSet):
    '''Feed subscription viewset'''

    queryset = SavedArticle.objects.all()
    serializer_class = SavedArticleSerializer

    def create(self, request, *args, **kwargs):
        '''Handle POST of new user feed subscription'''

        try:
            new_subscription = SavedArticle()
            new_subscription.article_id = request.data['article_id']
            new_subscription.user_id = request.auth.user.id
            new_subscription.save()
            
            serializer = SavedArticleSerializer(
                new_subscription, context={'request': request})
            return Response(serializer.data)
        except IntegrityError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)