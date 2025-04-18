from django.db import models
from app.mail_service import SendinBlue_Mail_Service


# Create your models here.
mail_service = SendinBlue_Mail_Service()

class UltraAthlete(models.Model):
    distance_str = "Ultra"
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
            {"email": "balkanultra.noreply@gmail.com", "name": "Balkan Ultra"},
            [{"email": self.email, "name": self.first_name}],
            [{"email": "balkanultra@abv.bg", "name": "Rosen Rusev"}],
            athlete=self
        )
        return result

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)


class SkyAthlete(models.Model):
    distance_str = "Sky"
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    gender = models.CharField(max_length=25)
    paid = models.BooleanField(default=False)
    payment_mail = models.EmailField(blank=True, null=True)

    def send_mail(self):
        result = mail_service.send_email(
            {"email": "balkanultra.noreply@gmail.com", "name": "Balkan Ultra"},
            [{"email": self.email, "name": self.first_name}],
            [{"email": "balkanultra@abv.bg", "name": "Rosen Rusev"}],
            athlete=self
        )
        return result


    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)


class Athlete(models.Model):
    first_name = models.CharField(max_length=25, default="")
    last_name = models.CharField(max_length=25, default="")
    gender = models.CharField(max_length=25, default="M")
    year_of_birth = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=20, default="")
    nationality = models.CharField(max_length=20, default="BG")

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)

class Result(models.Model):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name='results')
    year = models.PositiveIntegerField()
    distance = models.FloatField(help_text="Distance in kilometers")
    result_time = models.DurationField(null=True, help_text="Time taken for the result (e.g., hours, minutes, seconds)")
    position = models.PositiveIntegerField(null=True, default=0)

    def __str__(self):
        return f"{self.year} - {self.distance}km: {self.result_time}"
    
    class Meta:
        ordering = ['-year']
