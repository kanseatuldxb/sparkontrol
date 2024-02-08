from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.decorators import api_view
from rest_framework.response import Response

import requests

from rest_framework import mixins
from rest_framework import generics
from rest_framework import filters
from rest_framework.parsers import MultiPartParser


from django.contrib.auth.models import User

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


from .serialisers import LocationSerializer,RemoteSerializer,IncidentSerializer,SubscriptionSerializer,SubscriptionDetailedSerializer,IncidentDetailedSerializer
from portal.models import Location,Remote,Incident,Subscription

import django_filters.rest_framework
from rest_framework.authentication import TokenAuthentication

from django.utils import timezone

import json

from django.db.models import Q
# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the portal index.")

class Login(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request, format=None):
        username = self.request.data.get('username')
        password = self.request.data.get("password")
        print(username,password)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"success": 0 ,"detail": "User not found"},status=status.HTTP_401_UNAUTHORIZED)
        
        token, _ = Token.objects.get_or_create(user=user)
        fullname = user.first_name + " " + user.last_name
        return Response({"success": 1,
                         "detail": "",
                         "id":user.id,
                         "token": token.key,
                         "username":user.username,
                         "fullname":fullname,
                         "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email":user.email,
                        "date_joined":user.date_joined,
                        "last_login":user.last_login},status=status.HTTP_200_OK)


class Logout(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    
class LocationList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['serial_number', 'name','address']
    search_fields  = ['serial_number', 'name','address']
    ordering_fields = ['name']
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        user = self.request.user
        return Location.objects.all()
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(request.data["serial_number"])
        x=self.queryset.filter(serial_number=request.data["serial_number"]).first()
        print(x,type(x))
        if x is not None:
            return Response({"id": x.id,"serial_number": x.serial_number, "name": x.name, "address": x.address},status=status.HTTP_200_OK)
        print(request.data)
        return self.create(request, *args, **kwargs)
    
class LocationDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_queryset(self):
        # Only return instances that belong to the current user
        return self.queryset.all()
    authentication_classes = []
    permission_classes = []
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class RemoteList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Remote.objects.all()
    serializer_class = RemoteSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['name', 'location','serial_number','manufacturer']
    search_fields  = ['name', 'location','serial_number','manufacturer']
    ordering_fields = ['name', 'location']
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        user = self.request.user
        return Remote.objects.all()
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class RemoteDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Remote.objects.all()
    serializer_class = RemoteSerializer
    authentication_classes = []
    permission_classes = []
    def get_queryset(self):
        # Only return instances that belong to the current user
        return self.queryset.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

class IncidentList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['remote', 'event_type','call','acknowledge','reset','timestamp']
    search_fields  = ['remote','event_type']
    ordering_fields = ['event_type','call','acknowledge','reset','timestamp']
    authentication_classes = []
    permission_classes = []

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return IncidentSerializer
        return IncidentDetailedSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Incident.objects.all()
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class IncidentDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    authentication_classes = []
    permission_classes = []
    def get_queryset(self):
        # Only return instances that belong to the current user
        return self.queryset.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class CreateIncident(APIView):
    #permission_classes = (IsAuthenticated,)
    
    authentication_classes = []
    permission_classes = []
    def post(self, request, format=None):
        MachineID = self.request.data.get('MachineID')
        RemoteName = self.request.data.get('RemoteName')
        RemoteRequest = self.request.data.get('RemoteRequest')
        RemoteEvent = self.request.data.get('RemoteEvent') # CALL, ACK, RESET
        if MachineID is not None and RemoteName is not None and RemoteRequest is not None and RemoteEvent is not None:
            print(self.request.data)
            if RemoteEvent not in ["CALL","ACK","RST"]:
                return Response({"message": "Remote Event is Invalid"}, status=status.HTTP_200_OK)
            x=Remote.objects.filter(location=MachineID).filter(name=RemoteName).first() #check if remote exists for machine
            if x is not None: #check if remote name exists
                NewRemote = x
                if RemoteEvent == "CALL":
                    NewIncident = Incident()
                    NewIncident.remote = Remote.objects.get(pk=x.id)
                    NewIncident.event_type = RemoteRequest
                    NewIncident.call = timezone.now()
                    NewIncident.save()
                    IncidentPresentForRemote = Incident.objects.filter(remote=x.id).filter(event_type=RemoteRequest).filter(call__isnull=False, reset__isnull=True)
                    return Response({"message": "Remote Present " + str(NewRemote.id) + " With Incidents Called " + str(len(IncidentPresentForRemote))}, status=status.HTTP_200_OK)
                elif  RemoteEvent=="ACK":
                    FilterIncident = Incident.objects.filter(remote=x.id).filter(event_type=RemoteRequest).filter(call__isnull=False, acknowledge__isnull=True, reset__isnull=True)
                    for incident in FilterIncident:
                        incident.acknowledge = timezone.now()
                        incident.save()
                    return Response({"message": "Remote Present " + str(NewRemote.id) + " With Incidents Acknoledged " + str(len(FilterIncident))}, status=status.HTTP_200_OK)
                elif  RemoteEvent=="RST":
                    FilterIncident = Incident.objects.filter(remote=x.id).filter(event_type=RemoteRequest).filter(call__isnull=False, reset__isnull=True)
                    for incident in FilterIncident:
                        incident.reset = timezone.now()
                        incident.save()
                    return Response({"message": "Remote Present " + str(NewRemote.id) + " With Incidents Reseted " + str(len(FilterIncident))}, status=status.HTTP_200_OK)
                
            else:
                NewRemote = Remote()
                NewRemote.name = RemoteName
                NewRemote.location = Location.objects.get(pk=MachineID)  
                NewRemote.save() 
                if RemoteEvent == "CALL":
                    NewIncident = Incident()
                    NewIncident.remote = Remote.objects.get(pk=x.id)
                    NewIncident.event_type = RemoteRequest
                    NewIncident.call = timezone.now()
                    NewIncident.save()
                    IncidentPresentForRemote = Incident.objects.filter(remote=x.id).filter(event_type=RemoteRequest).filter(call__isnull=False, reset__isnull=True)
                    return Response({"message": "Remote Created " + str(NewRemote.id) + " With Incidents Called " + str(len(IncidentPresentForRemote))}, status=status.HTTP_200_OK)
                elif  RemoteEvent=="ACK":
                    FilterIncident = Incident.objects.filter(remote=x.id).filter(event_type=RemoteRequest).filter(call__isnull=False, acknowledge__isnull=True, reset__isnull=True)
                    for incident in FilterIncident:
                        incident.acknowledge = timezone.now()
                        incident.save()
                    return Response({"message": "Remote Created " + str(NewRemote.id) + " With Incidents Acknoledged " + str(len(FilterIncident))}, status=status.HTTP_200_OK)
                elif  RemoteEvent=="RST":
                    FilterIncident = Incident.objects.filter(remote=x.id).filter(event_type=RemoteRequest).filter(call__isnull=False, reset__isnull=True)
                    for incident in FilterIncident:
                        incident.reset = timezone.now()
                        incident.save()
                    return Response({"message": "Remote Created " + str(NewRemote.id) + " With Incidents Reseted " + str(len(FilterIncident))}, status=status.HTTP_200_OK)
                
        else:
            # If any field is missing or None, return an error response
            return Response({"message": "Missing or null fields in request data"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"result" : 1},status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK)

from django.shortcuts import get_object_or_404   
class SubscriptionList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['location','subscriber']
    search_fields  = ['location','subscriber']
    ordering_fields = ['location']
    authentication_classes = []
    permission_classes = []

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubscriptionSerializer
        return SubscriptionDetailedSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Subscription.objects.all()
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(self.request.data)
        print(request, *args, **kwargs)
        location_obj = get_object_or_404(Location, serial_number=self.request.data["location"])
        self.request.data["location"] = location_obj.id
        print(request.data["location"])
        x=self.queryset.filter(location=location_obj.id,subscriber=self.request.data["subscriber"]).first()
        print(x,type(x))
        if x is not None:
            return Response({"id": x.id,"location": x.location.pk, "subscriber": x.subscriber.pk, "timestamp": x.timestamp},status=status.HTTP_200_OK)
        print("sssssssssssssssssssssssssss         ssss ")
        print(request.data)
        return self.create(request, *args, **kwargs)
    
class SubscriptionDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    authentication_classes = []
    permission_classes = []
    def get_queryset(self):
        # Only return instances that belong to the current user
        return self.queryset.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)