from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, CartItemViewSet, AddressViewSet, OrderViewSet, StripeCheckoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'cart', CartItemViewSet, basename='cart')
router.register(r'addresses', AddressViewSet, basename='address')
router.register(r'order', OrderViewSet, basename='order')   

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', TokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('auth/token/Refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
    path('create-checkout-session', StripeCheckoutView.as_view(), name = 'stripe_checkout'),
]
