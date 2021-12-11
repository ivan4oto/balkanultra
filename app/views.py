from django.shortcuts import render, HttpResponseRedirect
from .forms import UltraAthleteForm, SkyAthleteForm

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

def checkout_view(request, race):
    return render(request, "checkout.html", {"race": race})

def success_view(request):
    return render(request, "success.html")

def cancel_view(request):
    return render(request, "cancel.html")