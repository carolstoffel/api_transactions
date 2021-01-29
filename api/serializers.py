from rest_framework import serializers
from api.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('type', 'destination', 'origin', 'amount')
        model = Event

    def to_representation(self, data):
        data = super(EventSerializer, self).to_representation(data)
        new_data = data.copy()
        d = "destination"
        del new_data['type']
        del new_data['destination']
        del new_data['origin']
        del new_data['amount']
        new_data[d] = {"id": data["destination"], "balance": data["amount"]}
        return new_data
