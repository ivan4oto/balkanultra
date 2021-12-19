from django.urls import path
from .views import create_checkout_session_view, stripe_webhook
    
urlpatterns = [
    path('create_checkout_session/<str:race>', create_checkout_session_view, name='create_checkout_session'),
    path('webhooks/stripe/', stripe_webhook, name='stripe_webhook')
]