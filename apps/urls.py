from django.urls import path

from apps.views import RegisterCreateAPIView, user_profile_api_view, PostsListAPIView, PostDetailRetrieveAPIView, \
    SellerCommentAPIView, PostCreateAPIView, CommentCreateAPIView, PostUpdateAPIView, PostDeleteAPIView, \
    CommentDeleteAPIView, AllPostsForSellerAPIView, AdminLoginApiView, CategoryCreateAPIView, GetCategoriesListAPIView, \
    CreateProductAPIView, GetProductListAPIView, EditCommentUpdateAPIView, CategoryUpdateAPIView, \
    DeleteCategoryDestroyAPIView, ProductUpdateAPIView, ProductDestroyAPIView, AllProductsListAPIView, \
    AllCategoryProductListAPIView

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
    path('edit-comment/<int:pk>/',EditCommentUpdateAPIView.as_view(),name='edit-comment'),

#      admin
    path('admin/login/',AdminLoginApiView.as_view(),name='admin-login'),
    path('create-category/',CategoryCreateAPIView.as_view(),name='create-category'),
    path('edit-category/<int:pk>/',CategoryUpdateAPIView.as_view(),name='edit-category'),
    path('delete-category/<int:pk>/',DeleteCategoryDestroyAPIView.as_view(),name='delete-category'),
    path('all-categories/',GetCategoriesListAPIView.as_view(),name='all-categories'),
    path('create-product/<int:pk>/',CreateProductAPIView.as_view(),name='create-product'),
    path('edit-product/<int:pk>/',ProductUpdateAPIView.as_view(),name='edit-product'),
    path('delete-product/<int:pk>/',ProductDestroyAPIView.as_view(),name='delete-product'),
    path('admin-product/<int:pk>/',GetProductListAPIView.as_view(),name='products'),
    path('all-products/',AllProductsListAPIView.as_view(),name='all-products'),

    path('all-products-categories/',AllCategoryProductListAPIView.as_view(),name='all-products-categories'),
]