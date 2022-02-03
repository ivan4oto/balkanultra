from django.db import models
from django.core.mail import send_mail

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

    def send_mail(self):
        send_mail(
            'Балкан Ултра - успешна регистрация',
            'Благодарим Ви, че се регистрирахте за Балкан Ултра. Очакваме ви на 06.08 2022',
            'balkanultra.noreply@gmail.com',
            [self.email],
            fail_silently=False,
        )

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

    def send_mail(self):
        send_mail(
            'Балкан Ултра - успешна регистрация',
            'Благодарим Ви, че се регистрирахте за Балкан Ултра. Очакваме ви на 06.08 2022',
            'balkanultra.noreply@gmail.com',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)