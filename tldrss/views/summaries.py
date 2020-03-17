import datetime

from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from tldrss.models import Summary

class SummarySerializer(serializers.HyperlinkedModelSerializer):
    '''Serializer for user-submitted summaries (tl;dr)'''
    # user = serializers.ModelSerializer()
    class Meta:
        model = Summary
        exclude = ['user']
        # fields = '__all__'
class SummaryViewSet(viewsets.ModelViewSet):
    '''Viewset for article summaries 'tl;dr's'''
    queryset = Summary.objects.all()
    serializer_class = SummarySerializer

    # def create(self, request, *args, **kwargs):
    #     '''Handle POST'''

    #     new_summary = Summary()
    #     new_summary.article_id = request.data['article_id']
    #     new_summary.user_id = request.data['user_id']
    #     new_summary.summary_text = request.data['summary_text']

    #     new_summary.save()

    #     serializer = SummarySerializer(new_summary, context={'request': request})

    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

# def partial_update(self, request, pk=None):
#         """Handle PUT requests for an individual payment type item
#         Returns:
#             Response -- Empty body with 204 status code
#         """
#         customer = Customer.objects.get(pk=pk)
#         customer.address = request.data["address"]
#         customer.city = request.data["city"]
#         customer.phone = request.data["phone"]
#         customer.save()

#         user = User.objects.get(pk=pk)
#         user.first_name = request.data["first_name"]
#         user.last_name = request.data["last_name"]
#         user.email = request.data["email"]

#         user.save()

#         return Response({}, status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk=None):
        '''Handle PATCH'''
        
        summary = Summary.objects.get(pk=pk)
        summary.summary_text = request.data['summary_text']
        # summary.edited_on = request.data['edited_on']

        summary.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


