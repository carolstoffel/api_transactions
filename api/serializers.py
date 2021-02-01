from rest_framework import serializers
from rest_framework.response import Response
from api.models import Event, Balance
from django.db.models.query import EmptyQuerySet


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('account_id', 'balance')
        model = Balance

    def to_representation(self, data):
        data = super(BalanceSerializer, self).to_representation(data)

        # print(data,'data') #OrderedDict([('account_id', '100'), ('balance', 0.0)]) data
        return data['balance']
        # return Response({'teste': 123})


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('type', 'destination', 'origin', 'amount')
        model = Event

    def to_representation(self, data):
        data = super(EventSerializer, self).to_representation(data)

        new_data = {}
        if data['type'] == 'deposit':
            try:
                ob = Balance.objects.get(
                    account_id=data['destination'])
                new_balance = ob.balance
            except:
                print('sem obje')
            new_data = data.copy()
            d = "destination"
            del new_data['type']
            del new_data['destination']
            del new_data['origin']
            del new_data['amount']
            try:
                ob = Balance.objects.get(
                    account_id=data['destination'])
                data['balance'] = ob.balance
                print('BALANCE', data['balance'])
            except:
                pass
            try:
                new_data[d] = {"id": data["destination"],
                               "balance": data["balance"]}
            except:
                pass
        elif data['type'] == 'withdraw':
            try:
                ob = Balance.objects.get(
                    account_id=data['origin'])
                new_balance = ob.balance
                print('NEW_BALANCE', new_balance)
            except:
                print('sem obje')
            new_data = data.copy()
            d = "origin"
            del new_data['type']
            del new_data['destination']
            del new_data['origin']
            del new_data['amount']
            try:
                ob = Balance.objects.get(
                    account_id=data['origin'])
                data['balance'] = ob.balance
                print('BALANCE', data['balance'])
            except:
                pass
            try:
                new_data[d] = {"id": data["origin"],
                               "balance": data["balance"]}
            except:
                pass
        elif data['type'] == 'transfer':
            print(data['origin'], 'origem')
            print(data['destination'], 'destination')
            try:
                ob_origin = Balance.objects.get(
                    account_id=data['origin'])
                ob_destination = Balance.objects.get(
                    account_id=data['destination'])
                new_balance_origin = ob_origin.balance
                new_balance_destination = ob_origin.balance
            except:
                print('sem obje')
            new_data = data.copy()
            d_origin = "origin"
            d_destination = "destination"
            del new_data['type']
            del new_data['destination']
            del new_data['origin']
            del new_data['amount']
            # {"origin": {"id":"100", "balance":0}, "destination": {"id":"300", "balance":15}}

            try:
                data_origin = {}
                data_destination = {}
                print('teste1')
                ob_origin = Balance.objects.get(
                    account_id=data['origin'])
                print(ob_origin, 'ob_origin')
                data_origin['origin'] = ob_origin.account_id
                data_origin['balance'] = ob_origin.balance
                print(ob_origin.balance, 'saldo')
                ob_destination = Balance.objects.get(
                    account_id=data['destination'])
                data_destination['balance'] = ob_destination.balance
                data_destination['destination'] = ob_destination.account_id
                print(data_destination, 'DATA DESTINATION')
            except:
                pass
            try:
                new_data[d_origin] = {"id": data_origin["origin"],
                                      "balance": data_origin["balance"]}
                new_data[d_destination] = {"id": data_destination["destination"],
                                           "balance": data_destination["balance"]}
            except:
                pass
        return new_data


class ResetSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('')
        model = Event

    def to_representation(self, data):
        data = super(ResetSerializer, self).to_representation(data)
        return data
