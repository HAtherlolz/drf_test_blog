from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


from .models import Posts, Comment, User


class PaginationPosts(PageNumberPagination):
    page_size = 3
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'result': data
        })


class PostFilter(filters.FilterSet):
    class Meta:
        model = Posts
        fields = ('id', 'text', 'user')


class CommentFilter(filters.FilterSet):
    class Meta:
        model = Comment
        fields = ('post__id', 'comment_text', 'user__first_name')
