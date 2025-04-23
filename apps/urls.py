from django.urls import path

from apps.views import RegisterCreateAPIView, user_profile_api_view, PostsListAPIView, PostDetailRetrieveAPIView, \
    SellerCommentAPIView, PostCreateAPIView, CommentCreateAPIView, PostUpdateAPIView, PostDeleteAPIView, \
    CommentDeleteAPIView, AllPostsForSellerAPIView

urlpatterns=[
    path('register/',RegisterCreateAPIView.as_view(),name='register'),
    path('profile/',user_profile_api_view,name='profile'),
    path('post-list/',PostsListAPIView.as_view(),name='posts'),
    path('post-detail/<int:pk>/',PostDetailRetrieveAPIView.as_view(),name='post-detail'),
    path('comments/',SellerCommentAPIView.as_view(),name='comments'),
    path('create-post/',PostCreateAPIView.as_view(),name='create-post'),
    path('create-comment/<int:post_id>/',CommentCreateAPIView.as_view(),name='create-comment'),
    path('edit-post/<int:pk>/',PostUpdateAPIView.as_view(),name='edit-post'),
    path('delete-post/<int:pk>/',PostDeleteAPIView.as_view(),name='delete-post'),
    path('delete-comment/<int:pk>/',CommentDeleteAPIView.as_view(),name='delete-comment'),
    path('all-posts/',AllPostsForSellerAPIView.as_view(),name='all-posts'),
]