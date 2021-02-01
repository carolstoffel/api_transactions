from rest_framework import serializers
from rest_framework.response import Response
from api.models import Event, Balance
from django.db.models.query import EmptyQuerySet
from api.actions import new_representation


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('account_id', 'balance')
        model = Balance

    def to_representation(self, data):
        data = super(BalanceSerializer, self).to_representation(data)
        return data['balance']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('type', 'destination', 'origin', 'amount')
        model = Event

    def to_representation(self, data):
        data = super(EventSerializer, self).to_representation(data)
        new_data = {}
        new_data = data.copy()
        if data['type'] == 'deposit':
            type_account = 'destination'
            new_representation(
                'deposit', data['destination'], new_data, type_account)
        elif data['type'] == 'withdraw':
            type_account = 'origin'
            new_representation(
                'withdraw', data['origin'], new_data, type_account)
        elif data['type'] == 'transfer':
            type_account = 'origin'
            new_representation(
                'transfer', data['origin'], new_data, type_account, data['destination'])
        return new_data


class ResetSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('')
        model = Event

    def to_representation(self, data):
        data = super(ResetSerializer, self).to_representation(data)
        return data
