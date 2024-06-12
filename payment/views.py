from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import stripe 
from helper.utils import commonApiResponse
from django.shortcuts import redirect 
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import permissions, status
from django.conf import settings
from .serializers import (
    ProductPreviewSerializer
)
from .models import Product 
from .utils import successful_payment_email


stripe.api_key = settings.STRIPE_SECRET_KEY 
API_URL = 'http://localhost:8000'


def home(request):
    return render(request, "home.html")

def success(request):
    return render(request, "success.html")

def cancel(request):
    return render(request, "cancel.html")


class ProductPreview(RetrieveAPIView):
    serializer_class = ProductPreviewSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.all() 


class CreateCheckOutSession(APIView):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs['pk']
        try:
            product = Product.objects.get(id=product_id) 
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': int(product.price) * 100,
                            'product_data': {
                                'name': product.name,
                                'images': ["https://i.imgur.com/EHyR2nP.png"]
                            }
                        },
                        'quantity': 1,
                    }
                ],
                metadata={
                    'product_id':product.id,
                },
                mode="payment",
                # success_url=settings.SITE_URL + '?success=true',
                # cancel_url=settings.SITE_URL + '?canceled=true'
                success_url=request.build_absolute_uri(reverse("success")),
                cancel_url=request.build_absolute_uri(reverse("cancel")),
            ) 
            return redirect(checkout_session.url, status=status.HTTP_303_SEE_OTHER) 
        except:
            return commonApiResponse(
                message="something went wrong while creating stripe session",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# Stripe Event Handeler 
# Receive an event notification when a customer pays you.
# Optionally, handle additional payment methods.
# @csrf_exempt
# def stripe_webhook_view(request):
#     print("Payment completed")
#     payload = request.body  
#     # For now, you only need to print out the webhook payload so you can see
#     # the structure.
#     print(payload)

#     # Send an email to the user that their payment is successful
#     # successful_payment_email()  
#     return commonApiResponse(status=200)

class StripeWebhookView(APIView):
    def post(self, request, *args, **kwargs):
        print("Payment completed")
        payload = request.body  
        # For now, you only need to print out the webhook payload so you can see
        # the structure.
        print(payload)

        # Send an email to the user that their payment is successful
        successful_payment_email()  
        return commonApiResponse(status=status.HTTP_200_OK)