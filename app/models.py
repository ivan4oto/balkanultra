from django.db import models
from app.mail_service import SendinBlue_Mail_Service


# Create your models here.
mail_service = SendinBlue_Mail_Service()

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
        result = mail_service.send_email(
            "balkanultra.noreply@gmail.com",
            [{"email": self.email, "name": self.first_name}],
            "78",
            [{"email": "balkanultra@abv.bg", "name": "Rosen Rusev"}]
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
        result = mail_service.send_email(
            "balkanultra.noreply@gmail.com",
            [{"email": self.email, "name": self.first_name}],
            "14",
            [{"email": "balkanultra@abv.bg", "name": "Rosen Rusev"}]
        )
        return result


    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)