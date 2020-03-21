from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

DEFAULT_PAGE = 1

class CustomPagination(PageNumberPagination):
    page = DEFAULT_PAGE
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'page': int(self.request.GET.get('page', DEFAULT_PAGE)),
            # 'links': {
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            # },
            'results': data
        })