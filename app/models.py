from django.db import models
from django.core.mail import send_mail
from .mail_letters import Letter

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
            Letter.ULTRA_LETTER.format(
                f=self.first_name,
                l=self.last_name,
                m=self.email,
                fl=self.first_link,
                sl=self.second_link
            ),
            'balkanultra.noreply@gmail.com',
            [self.email, 'balkanultra@abv.bg'],
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
            Letter.SKY_LETTER.format(
                f=self.first_name,
                l=self.last_name,
                m=self.email
                ),
            'balkanultra.noreply@gmail.com',
            [self.email, 'balkanultra@abv.bg'],
            fail_silently=False,
        )

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)