from django.contrib import admin
from app.models import UltraAthlete, SkyAthlete
from stripe_app.models import Payment

admin.site.register(UltraAthlete)
admin.site.register(SkyAthlete)
admin.site.register(Payment)
# Register your models here.
