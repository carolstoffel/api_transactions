from rest_framework.response import Response
from rest_framework import viewsets
from api.serializers import EventSerializer
from api.models import Event
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
        """
        print('CAROL', request._full_data)  # _full_data
        if request.data['descricao'] == str(1):
            print('entrou')
            request._full_data['descricao'] == str(2)
        print('NOVO VALOR DE DESCRICAO=', request.data['descricao'])
        """
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
