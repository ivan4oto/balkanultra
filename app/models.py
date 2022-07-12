from django.db import models
from django.core.mail import send_mail
from .mail_letters import Letter
from .services import Mailjet_Letter_Service

# Create your models here.

class UltraAthlete(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    gender = models.CharField(max_length=25)
    paid = models.BooleanField(default=False)
    payment_mail = models.EmailField(blank=True, null=True)
    first_link = models.URLField(blank=False, null=True)
    second_link = models.URLField(blank=False, null=True)

    def send_mail(self):
        result = Mailjet_Letter_Service().send_letter(
            self.email, self.first_name, self.last_name, self.first_link,
            self.second_link, 'ultra'
        )
        return result

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)


class SkyAthlete(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    gender = models.CharField(max_length=25)
    paid = models.BooleanField(default=False)
    payment_mail = models.EmailField(blank=True, null=True)

    def send_mail(self):
        result = Mailjet_Letter_Service().send_letter(
            self.email, self.first_name, self.last_name, None,
            None, 'ultra'
        )
        return result


    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)