from django.shortcuts import render

# Create your views here.

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
    context = {'race': race}
    return render(request, "register.html", context)