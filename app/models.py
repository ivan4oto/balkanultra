from django.db import models

# Create your models here.

class UltraAthlete(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    gender = models.CharField(max_length=25)
    paid = models.BooleanField(default=False)
    payment_mail = models.EmailField()
    first_link = models.URLField(blank=True, null=True)
    second_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)

class SkyAthlete(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    gender = models.CharField(max_length=25)
    paid = models.BooleanField(default=False)
    payment_mail = models.EmailField()

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)