from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from api.serializers import EventSerializer, BalanceSerializer
from api.models import Event, Balance
from django.http import HttpResponse


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.all()
        return queryset

    def list(self, request, *args, **kwargs):
        # atrelado ao GET
        return super(EventViewSet, self).list(request, *args, **kwargs)
        # return Response({'teste': 123})

    def create(self, request, *args, **kwargs):
        # atrelado ao POST
        if request.data['type'] == 'deposit':
            try:
                account_exist = Balance.objects.get(
                    account_id=request.data['destination'])
                print('existe', account_exist)
                new_balance = float(account_exist.balance) + \
                    float(request.data['amount'])
                Balance.objects.filter(pk=account_exist.account_id).update(
                    balance=new_balance)
            except:
                print('nao existe, cadastrando')
                print(request.data['destination'])
                create_account = Balance(
                    account_id=request.data['destination'], balance=request.data['amount'])
                create_account.save()
        elif request.data['type'] == 'withdraw':
            try:
                account_exist = Balance.objects.get(
                    account_id=request.data['origin'])
                new_balance = float(account_exist.balance) - \
                    float(request.data['amount'])
                Balance.objects.filter(pk=account_exist.account_id).update(
                    balance=new_balance)
            except:
                return Response(0, status=status.HTTP_404_NOT_FOUND)
        elif request.data['type'] == 'transfer':
            try:
                account_origin_exist = Balance.objects.get(
                    account_id=request.data['origin'])
            except:
                return Response(0, status=status.HTTP_404_NOT_FOUND)
            new_balance_origin = float(
                account_origin_exist.balance) - float(request.data['amount'])
            Balance.objects.filter(pk=account_origin_exist.account_id).update(
                balance=new_balance_origin)
            try:
                account_destination_exist = Balance.objects.get(
                    account_id=request.data['destination'])
                new_balance_destination = float(
                    account_destination_exist.balance) + float(request.data['amount'])
                Balance.objects.filter(pk=account_destination_exist.account_id).update(
                    balance=new_destination_origin)
            except:
                create_account = Balance(
                    account_id=request.data['destination'], balance=request.data['amount'])
                create_account.save()
        return super(EventViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # atrelado ao GET, porém ex: pontosturisticos/1/
        return super(EventViewSet, self).destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # atrelado ao PUT
        return super(EventViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        # atrelado ao PATCH
        return super(EventViewSet, self).partial_update(request, *args, **kwargs)


class BalanceViewSet(viewsets.ModelViewSet):
    serializer_class = BalanceSerializer

    def get_queryset(self):
        queryset = Balance.objects.all()
        return queryset

    def list(self, request, *args, **kwargs):
        # atrelado ao GET
        return super(BalanceViewSet, self).list(request, *args, **kwargs)
        # return Response({'teste': 123})
