from django.http import HttpResponseServerError
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for user

    Arguments:
        serializers.HyperlinkedModelSerializer
    """

    class Meta:
        model = User
        # url = serializers.HyperlinkedIdentityField(
        #     view_name='user',
        #     lookup_field='id'
        # )
        
        fields = ('id', 'username', 'url',)
        # fields = ('id', 'username','first_name', 'last_name', 'email', 'url')

class UserViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        '''List User entities'''

        users = User.objects.all()

        user = request.query_params.get("self", None)

        if user:
            users = User.objects.filter(id=request.auth.user.id)
        
        serializer = UserSerializer(users, many=True, context={'request': request})

        return Response(serializer.data)