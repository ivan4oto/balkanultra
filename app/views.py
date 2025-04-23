from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, JsonResponse
from .forms import UltraAthleteForm, SkyAthleteForm
from .models import UltraAthlete, SkyAthlete, Result, Athlete
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
        return render(request, "results.html", {
            'scheme': request.scheme,
            'host': request.get_host()
        })

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
        # form invalid
        else:
            return JsonResponse({
                "status": "error",
                "error_msg": "Form validation error!"
            })
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

def athletes_by_year_distance(request, year, distance):
    """
    View to get all athletes who have results for a specific year and distance.
    URL: /athletes/year/<int:year>/distance/<float:distance>/
    Returns JSON data.
    """
    # Query results matching the year and distance
    distance = float(distance)
    results = Result.objects.filter(year=year, distance=distance)

    if not results.exists():
        return JsonResponse({'message': 'No results found for the given year and distance'}, status=404)

    # Get unique athletes from these results
    athletes = Athlete.objects.filter(results__in=results).distinct()

    # Prepare the data for JSON response
    athletes_data = []
    for athlete in athletes:
        athlete_result = athlete.results.get(year=year, distance=distance)
        athletes_data.append({
            'position': athlete_result.position if athlete_result.position > 0 else "DNF",
            'time': str(athlete_result.result_time) if athlete_result.position > 0 else "DNF",
            'athlete_second_name': athlete.last_name,
            'athlete_first_name': athlete.first_name,
            'gender': athlete.gender,
        })
    athletes_data.sort(key=lambda record: (not isinstance(record['position'], (int, float)), record['position']))
    response_data = {
        'year': year,
        'distance': distance,
        'athletes': athletes_data
    }

    return JsonResponse(response_data, safe=False)  # safe=False allows non-dict objects

def athlete_results(request, first_name, last_name):
    athlete = get_object_or_404(Athlete, first_name=first_name, last_name=last_name)
    results = athlete.results.all().values(
        'year', 'distance', 'result_time', 'position'
    )
    return JsonResponse({
        'athlete': f"{athlete.first_name} {athlete.last_name}",
        'results': list(results)
    })

def hall_of_fame_view(request):
    return render(request, "hall_of_fame.html", {
            'scheme': request.scheme,
            'host': request.get_host()
        })


def top_athletes_by_participations(request):
    distance = request.GET.get('distance')

    if not distance:
        return JsonResponse({'error': 'Distance parameter is required'}, status=400)

    try:
        distance = float(distance)
    except ValueError:
        return JsonResponse({'error': 'Distance must be a valid number'}, status=400)

    # Query to find athletes with most participations for the given distance
    top_athletes = Athlete.objects.filter(
        results__distance=distance
    ).annotate(
        participations=Count('results')
    ).order_by(
        '-participations'
    )[:10]

    # Format the results
    result_data = [
        {
            'first_name': athlete.first_name,
            'last_name': athlete.last_name,
            'participations': athlete.participations
        }
        for athlete in top_athletes
    ]

    return JsonResponse(result_data, safe=False)