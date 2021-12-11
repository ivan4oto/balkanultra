from django.urls import path
from .views import stripe_config, create_checkout_session_view, stripe_webhook
    
urlpatterns = [
    path('create_checkout_session/<str:race>', create_checkout_session_view, name='create_checkout_session'),
    path('config/', stripe_config, name='stripe_config'),
    path('webhooks/stripe/', stripe_webhook, name='stripe_webhook')
]