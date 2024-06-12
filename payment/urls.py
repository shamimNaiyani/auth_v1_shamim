from django.urls import path
from .views import ProductPreview, CreateCheckOutSession, home, StripeWebhookView, success, cancel
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('webhook/', csrf_exempt(StripeWebhookView.as_view()), name='stripe-webhook'),
    path("checkout/home/", home, name="home"),
    path('checkout/create-checkout-session/<pk>/', csrf_exempt(CreateCheckOutSession.as_view()), name='checkout_session'),
    path('product/<int:pk>/', ProductPreview.as_view(), name="product"),
    path("success/", success, name="success"),
    path("cancel/", cancel, name="cancel"),
]
