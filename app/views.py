from django.shortcuts import render
from django.http import JsonResponse
from .forms import UltraAthleteForm, SkyAthleteForm
from .models import UltraAthlete, SkyAthlete
from django.conf import settings
from .services import join_results


def home_view(request, *args, **kwargs):
    context = {}
    return render(request, "home.html", context)

def about_view(request, *args, **kwargs):
    context = {}
    return render(request, "about.html", context)

def results_view(request, type):
    if type == 'all':
        return render(request, "results.html")
    elif type == 'json':
            results = join_results({
                '2020': ['ultra'],
                '2021': ['ultra', 'sky']
            })
            return JsonResponse(results, safe=False)
    return JsonResponse({
        'ala': 'bala'
    })


def register_view(request, race):
    stripe_config = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        model = UltraAthlete if race == 'ultra' else SkyAthlete
        athlete = model.objects.filter(email=request.POST['email']).first()
        if athlete:
            return JsonResponse({
                "status": "already exists",
                "email": athlete.email
            })

        form = UltraAthleteForm(request.POST) if race == 'Ultra' else SkyAthleteForm(request.POST)
        if form.is_valid():
            athlete = form.save()
            athlete.send_mail()
            return JsonResponse({
                "status": "success",
                "email": athlete.email
            })

    else:
        form = UltraAthleteForm() if race == 'Ultra' else SkyAthleteForm()

    return render(request, "register.html", {'form': form, 'race': race, 'public_key': stripe_config})



def checkout_view(request, race):
    return render(request, "checkout.html", {"race": race})

def success_view(request):
    return render(request, "success.html")

def cancel_view(request):
    return render(request, "cancel.html")