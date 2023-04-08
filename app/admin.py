import csv
from django.contrib import admin
from django.http import HttpResponse
from app.models import UltraAthlete, SkyAthlete
from stripe_app.models import Payment

# Register your models here.

@admin.action(description='export as csv')
def export_as_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])

    return response

@admin.register(SkyAthlete)
class AuthorAdmin(admin.ModelAdmin):
    actions = [export_as_csv]

@admin.register(UltraAthlete)
class AuthorAdmin(admin.ModelAdmin):
    actions = [export_as_csv]

@admin.register(Payment)
class AuthorAdmin(admin.ModelAdmin):
    pass