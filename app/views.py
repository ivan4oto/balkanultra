from django.shortcuts import render, HttpResponseRedirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import UltraAthleteForm, SkyAthleteForm
import stripe

# stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_key = "sk_test_51K4TloIv6n82Hb4KrY6OcDmmxyxDe500U6nTHkz8pn5QAoa9Y4gqwy8Npki0741ec2eGImVJDV9TTnp66xhwI16K00HO2dAkuZ"

# Create your views here.
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

def home_view(request, *args, **kwargs):
    context = {}
    return render(request, "home.html", context)

def about_view(request, *args, **kwargs):
    context = {}
    return render(request, "about.html", context)

def results_view(request, year):
    context = {'year': year}
    return render(request, "results.html", context)

def register_view(request, race):
    print('hi bro')
    context = {'race': race}
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UltraAthleteForm(request.POST) if race == 'Ultra' else SkyAthleteForm()
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UltraAthleteForm() if race == 'Ultra' else SkyAthleteForm()


    return render(request, "register.html", {'form': form})

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


def checkout_view(request):
    return render(request, "checkout.html")

def success_view(request):
    return render(request, "success.html")

def cancel_view(request):
    return render(request, "cancel.html")