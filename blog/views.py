from django.http import Http404
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView


from .serializer import PostsSerializer, CommentSerializer, UserSerializer, FollowingSerializer
from .models import Posts, Comment, UserFollowing, User
from .service import PostFilter, CommentFilter, PaginationPosts


class PostsCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = PostsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PostsListView(ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostFilter
    pagination_class = PaginationPosts
    permission_classes = [AllowAny]


class PostDetailView(APIView):
    def get_object(self, pk):
        try:
            return Posts.objects.get(pk=pk)
        except Posts.DoesNotExist:
            raise Http404


    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostsSerializer(post)
        return Response(serializer.data)


    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostsSerializer(post, data=request.data)
        if serializer.is_valid():
            if self.request.user == post.user:
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({"Permission Denied"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        post = self.get_object(pk)
        if self.request.user == post.user:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Permission Denied"}, status=status.HTTP_400_BAD_REQUEST)


class CommentsCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class CommentsListView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CommentFilter
    pagination_class = PaginationPosts
    permission_classes = [AllowAny]



class CommentDetailView(APIView):
    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404


    def get(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)


    def put(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            if self.request.user == comment.user:
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({"Permission Denied"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Permission Denied"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = self.get_object(pk)
        if self.request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"Permission Denied"}, status=status.HTTP_400_BAD_REQUEST)


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
