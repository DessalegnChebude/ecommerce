from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import ProductImageViewSet, UserViewSet, ProductViewSet,CategoryViewSet,OrderViewSet, ReviewViewSet

from rest_framework_simplejwt.views import TokenObtainPairView

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('products', ProductViewSet)
router.register('categories', CategoryViewSet)
router.register('orders', OrderViewSet )
router.register('reviews', ReviewViewSet)
router.register('product-images', ProductImageViewSet, basename='product-image')



urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]

urlpatterns += router.urls