from django.urls import path, include

from apps.models import Wifi
from apps.views import RegisterCreateAPIView, user_profile_api_view, PostsListAPIView, PostDetailRetrieveAPIView, \
    SellerCommentAPIView, PostCreateAPIView, CommentCreateAPIView, PostUpdateAPIView, PostDeleteAPIView, \
    CommentDeleteAPIView, AllPostsForSellerAPIView, AdminLoginApiView, CategoryCreateAPIView, GetCategoriesListAPIView, \
    EditCommentUpdateAPIView, CategoryUpdateAPIView, \
    DeleteCategoryDestroyAPIView, CPUListAPIView, MotherBoardListAPIView, \
    power_unit_api_view, CPUAddCreateAPIView, CPUUpdateAPIView, CPUDestroyAPIView, MotherBoardViewSet, SoketViewSet, \
    PowerUnitViewSet, CPUModelViewSet, AllGPUListAPIView, AllRamsListAPIView, AllMemoryModelSerializer, \
    CollerListAPIView, KeysListAPIView, MonitorListAPIView, WifiListAPIView, AccessorListAPIView, GPUViewSet, \
    RAMViewSet, MemoryViewSet, CollerViewSet, KeysViewSet, MonitorViewSet, WifiViewSet, AccessorViewSet, \
    CategoryPViewSet, ProductViewSet, ProductByCategoryIDListAPIView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'motherboards', MotherBoardViewSet)
router.register(r'sokets', SoketViewSet)
# router.register(r'others', OtherViewSet)
router.register(r'powerunits', PowerUnitViewSet)
router.register(r'cpus', CPUModelViewSet)
router.register(r'gpus', GPUViewSet)
router.register(r'rams', RAMViewSet)
router.register(r'memories', MemoryViewSet)
router.register(r'collers', CollerViewSet)
router.register(r'keys', KeysViewSet)
router.register(r'monitors', MonitorViewSet)
router.register(r'wifi', WifiViewSet)
router.register(r'accessors', AccessorViewSet)

router.register(r'category-product', CategoryPViewSet)
router.register(r'product', ProductViewSet)


urlpatterns = [
    path('register/', RegisterCreateAPIView.as_view(), name='register'),
    path('profile/', user_profile_api_view, name='profile'),
    path('post-list/', PostsListAPIView.as_view(), name='posts'),
    path('post-detail/<int:pk>/', PostDetailRetrieveAPIView.as_view(), name='post-detail'),
    path('comments/', SellerCommentAPIView.as_view(), name='comments'),
    path('create-post/', PostCreateAPIView.as_view(), name='create-post'),
    path('create-comment/<int:post_id>/', CommentCreateAPIView.as_view(), name='create-comment'),
    path('edit-post/<int:pk>/', PostUpdateAPIView.as_view(), name='edit-post'),
    path('delete-post/<int:pk>/', PostDeleteAPIView.as_view(), name='delete-post'),
    path('delete-comment/<int:pk>/', CommentDeleteAPIView.as_view(), name='delete-comment'),
    path('all-posts/', AllPostsForSellerAPIView.as_view(), name='all-posts'),
    path('edit-comment/<int:pk>/', EditCommentUpdateAPIView.as_view(), name='edit-comment'),

    #     Changes

    path('cpu/<int:category_id>/', CPUListAPIView.as_view()),
    path('motherboards-by-cpu/<int:cpu_id>/', MotherBoardListAPIView.as_view()),
    # path('others-by-category/<int:category_id>/', OtherListAPIView.as_view()),
    path('powerunit/', power_unit_api_view),

    # Second Updates For User
    path('gpus-customer/<int:category_id>/',AllGPUListAPIView.as_view()),
    path('rams-customer/<int:category_id>/',AllRamsListAPIView.as_view()),
    path('memories-customer/',AllMemoryModelSerializer.as_view()),
    path('collers-customer/<int:category_id>/',CollerListAPIView.as_view()),
    path('keys-customer/<int:category_id>/',KeysListAPIView.as_view()),
    path('monitors-customer/',MonitorListAPIView.as_view()),
    path('wifi-customer/',WifiListAPIView.as_view()),
    path('accessories-customer/',AccessorListAPIView.as_view()),
    path('categoryp-product/<int:category_id>/',ProductByCategoryIDListAPIView.as_view()),

    # path('add-cpu/', CPUAddCreateAPIView.as_view()),
    # path('update-cpu/<int:pk>/', CPUUpdateAPIView.as_view()),
    # path('delete-cpu/<int:pk>/', CPUDestroyAPIView.as_view()),
    path('', include(router.urls)),

    #      admin
    path('admin/login/', AdminLoginApiView.as_view(), name='admin-login'),
    path('create-category/', CategoryCreateAPIView.as_view(), name='create-category'),
    path('edit-category/<int:pk>/', CategoryUpdateAPIView.as_view(), name='edit-category'),
    path('delete-category/<int:pk>/', DeleteCategoryDestroyAPIView.as_view(), name='delete-category'),
    path('all-categories/', GetCategoriesListAPIView.as_view(), name='all-categories'),
    # path('create-product/<int:pk>/',CreateProductAPIView.as_view(),name='create-product'),
    # path('edit-product/<int:pk>/',ProductUpdateAPIView.as_view(),name='edit-product'),
    # path('delete-product/<int:pk>/',ProductDestroyAPIView.as_view(),name='delete-product'),
    # path('admin-product/<int:pk>/',GetProductListAPIView.as_view(),name='products'),
    # path('all-products/',AllProductsListAPIView.as_view(),name='all-products'),
    #
    # path('all-products-categories/',AllCategoryProductListAPIView.as_view(),name='all-products-categories'),
]
