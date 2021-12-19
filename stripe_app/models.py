from django.db import models

# Create your models here.
class Payment(models.Model):
    payment_mail = models.EmailField()
    amount_total = models.IntegerField()
    payment_status = models.CharField(max_length=25)
    payment_intent = models.CharField(max_length=100)


    def __str__(self):
        return str(self.payment_mail)