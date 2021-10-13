from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView


from .serializer import PostsSerializer, CommentSerializer, UserSerializer, FollowingSerializer
from .models import Posts, Comment, UserFollowing, User
from .service import PostFilter, CommentFilter, PaginationPosts
from .business_services import get_object_detail, update_object, delete_object, create_object

import datetime
class PostsCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        return create_object(request, PostsSerializer)


class PostsListView(ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostFilter
    pagination_class = PaginationPosts
    permission_classes = [AllowAny]


class PostDetailView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, pk):
        return get_object_detail(request, pk, Posts, PostsSerializer)


    def put(self, request, pk):
        return update_object(pk, request, Posts, PostsSerializer)


    def delete(self, request, pk):
        return delete_object(request, pk, Posts)

class CommentsCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        return create_object(request, CommentSerializer)


class CommentsListView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CommentFilter
    pagination_class = PaginationPosts
    permission_classes = [AllowAny]



class CommentDetailView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, pk):
        return get_object_detail(request, pk, Comment, CommentSerializer)


    def put(self, request, pk):
        return update_object(pk, request, Comment, CommentSerializer)


    def delete(self, request, pk):
        return delete_object(request, pk, Comment)

class UserFollowingView(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_current_user(self, request):
        try:
            return User.objects.get(user__id=self.request.user)
        except User.DoesNotExist:
            raise Http404

    def get_other_profile(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        post = self.get_other_profile(pk)
        serializer = UserSerializer(post)
        return Response(serializer.data)

    def post(self, request, pk, format=None):

        current_profile = self.get_current_user(request)
        other_profile = self.get_other_profile(pk)

        serializer = FollowingSerializer(user_id=current_profile, following_user_id=other_profile)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        follow = self.get_other_profile(pk)
        if self.request.user == follow.user:
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"Permission Denied"}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PaginationPosts
    permission_classes = [AllowAny]
