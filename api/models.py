from django.db import models


class Event(models.Model):
    type = models.CharField(max_length=50)
    destination = models.CharField(max_length=50, null=True)
    origin = models.CharField(max_length=50, null=True)
    amount = models.FloatField(null=True)
    '''
    def json_object(self):
        return {
            "destination": self.destination,
            "type": self.type,
            "ammount": self.ammount
        }
    '''

    def __str__(self):
        return self.type, self.destination
