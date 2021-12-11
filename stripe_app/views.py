from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe

# Create your views here.

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session_view(request, race):
    if race == 'ultra':
        price = settings.PRICE_ULTRA
    elif race == 'sky':
        price = settings.PRICE_SKY
    
    YOUR_DOMAIN = 'http://127.0.0.1:8000'
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price,
                    'quantity': 1
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel',
        )
    except Exception as e:
        return JsonResponse({'error': str(e)})

    return JsonResponse({'sessionId': checkout_session['id']})

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        # TODO: run some custom code here

    return HttpResponse(status=200)