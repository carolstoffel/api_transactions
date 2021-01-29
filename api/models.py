from django.db import models


class Event(models.Model):
    type = models.CharField(max_length=50)
    destination = models.CharField(max_length=50, null=True)
    origin = models.CharField(max_length=50, null=True)
    amount = models.FloatField(null=True)

    def __str__(self):
        return self.type, self.destination


class Balance(models.Model):
    account_id = models.CharField(max_length=50, primary_key=True)
    balance = models.FloatField(null=True)
