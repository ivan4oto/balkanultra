from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, JsonResponse
from .forms import UltraAthleteForm, SkyAthleteForm
from .models import UltraAthlete, SkyAthlete
from django.conf import settings
from .services import join_results, get_gpx_file
from sib_api_v3_sdk.rest import ApiException


def home_view(request, *args, **kwargs):
    context = {}
    return render(request, "home.html", context)

def about_view(request, *args, **kwargs):
    context = {}
    return render(request, "about.html", context)

def results_view(request, type):
    if type == 'all':
        return render(request, "results.html")

def get_results(request):
    results = join_results({
        '2020': ['ultra'],
        '2021': ['ultra', 'sky'],
        '2022': ['ultra', 'sky']
    })
    return JsonResponse(results, safe=False)

@csrf_protect
def register_view(request, race):
    if not settings.REGISTRATION_ENABLED:
        return render(request, "disabled_register.html")

    if request.method == 'POST':
        model = UltraAthlete if race == 'ultra' else SkyAthlete
        athlete = model.objects.filter(email=request.POST['email']).first()
        if athlete:
            return JsonResponse({
                "status": "already exists",
                "email": athlete.email
            })

        form = UltraAthleteForm(request.POST) if race == 'ultra' else SkyAthleteForm(request.POST)
        if form.is_valid():
            athlete = form.save()
            response = {
                "status": "success",
                "email": athlete.email,
                "mail_status": "success",
                "mail_error": None,
                'mail_response': None,
                }
            try:
                mail_result = athlete.send_mail()
                response['mail_response'] = mail_result.to_str()

            except ApiException as e:
                response['mail_status'] = "error"
                response['mail_error'] = str(e)
            return JsonResponse(
                response
            )
    else:
        form = UltraAthleteForm() if race == 'ultra' else SkyAthleteForm()

    return render(request, "register.html", {
        'form': form,
        'race': race,
        'scheme': request.scheme,
        'host': request.get_host()
    })


def athletes_view(request):
    sky_athletes = SkyAthlete.objects.all()
    ultra_athletes = UltraAthlete.objects.all().filter(paid=True)
    return render(request, "athletes.html", {
        'sky_athletes': sky_athletes,
        'ultra_athletes': ultra_athletes
    })


def download_gpx_view(request, race):
    f = get_gpx_file(race)
    response = HttpResponse(f.read(), content_type="application/gpx+xml")
    response['Content-Disposition'] = 'inline; filename=' + 'balkan_' + race + '.gpx'

    return response
