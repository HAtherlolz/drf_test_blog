from django.urls import path
from .views import *


urlpatterns = [
    path('post-create/', PostsCreateView.as_view()),
    path('posts/', PostsListView.as_view()),
    path('post-detail/<int:pk>/', PostDetailView.as_view()),
    path('comment-create/', CommentsCreateView.as_view()),
    path('comments/', CommentsListView.as_view()),
    path('comment-detail/<int:pk>/', CommentDetailView.as_view()),
]