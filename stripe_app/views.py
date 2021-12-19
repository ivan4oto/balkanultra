from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from app.models import UltraAthlete, SkyAthlete
from .models import Payment
import stripe
import json


@csrf_exempt
def create_checkout_session_view(request, race):
    request_body = json.loads(request.body.decode("utf-8"))
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
            metadata = {
                "race_type": race,
                "form_mail": request_body.get('email')
            },
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
        session = event['data']['object']
        metadata = session.get('metadata')
        customer_details = session.get('customer_details')
        # Saving the payment to db
        payment = Payment(
            payment_mail = session.get('customer_details', None).get('email'),
            amount_total = session.get('amount_total'),
            payment_status = session.get('payment_status'),
            payment_intent = session.get('payment_intent')
        )
        payment.save()

        model = UltraAthlete if metadata.get('race_type') == 'ultra' else SkyAthlete
        athlete = model.objects.filter(email=metadata.get('form_mail')).first()
        # Adding payment info to athlete if emails match
        if athlete:
            athlete.payment_mail = customer_details.get('email')
            athlete.paid = True
            athlete.save()
        
        return HttpResponse(status=200)

    return HttpResponse(status=200)