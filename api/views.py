from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import filters
import django_filters.rest_framework
from api.serializers import EventSerializer, BalanceSerializer, ResetSerializer
from api.models import Event, Balance
from django.http import HttpResponse
from api.actions import get_account_exist, do_transaction


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        # attached to POST
        if request.data['type'] == 'deposit':
            do_transaction(
                transaction='deposit', account_id1=request.data['destination'], amount=request.data['amount'])
        elif request.data['type'] == 'withdraw':
            validate = do_transaction(
                transaction='withdraw', account_id1=request.data['origin'], amount=request.data['amount'])
            if validate is False:
                # if the function do_transaction returns False, it's because the origin account
                # doesn't exists
                return Response(0, status=status.HTTP_404_NOT_FOUND)
        elif request.data['type'] == 'transfer':
            validate = do_transaction(
                transaction='transfer', account_id1=request.data['origin'], amount=request.data['amount'], account_id2=request.data['destination'])
            if validate is False:
                # if the function do_transaction returns False, it's because the origin account
                # doesn't exists
                return Response(0, status=status.HTTP_404_NOT_FOUND)
        return super(EventViewSet, self).create(request, *args, **kwargs)


class BalanceViewSet(viewsets.ModelViewSet):
    serializer_class = BalanceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['account_id']

    def get_queryset(self):
        queryset = Balance.objects.all()
        print(queryset, 'queryset')
        return queryset

    def list(self, request, *args, **kwargs):
        # attached to  GET
        # if the request method is GET and there is something writting in url
        if request.method == 'GET' and bool(request.query_params):
            info = request.query_params
            try:
                # in case the info written in url is account_id passing a value,
                # is going to catch the balance for the account id and return it
                account_data = Balance.objects.get(
                    account_id=info['account_id'])
                return Response(account_data.balance, status=status.HTTP_200_OK)
            except:
                # if wasn't possible to catch the value due to the info in url isn't
                # "account_id" or the account_id doesn't exist, it will return 404
                return HttpResponse(0, status=404)
        return super(BalanceViewSet, self).list(request, *args, **kwargs)


class ResetViewSet(viewsets.ModelViewSet):
    serializer_class = ResetSerializer

    def get_queryset(self):
        queryset = Balance.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        # attached to POST
        # the variable all_balance will get all the objects that are saved
        # in Balance model and will delete all. The same will happen with
        # Event objects
        all_balance = Balance.objects.all()
        [b.delete() for b in all_balance]

        all_event = Event.objects.all()
        [e.delete() for e in all_event]
        return HttpResponse('OK', status=200)
