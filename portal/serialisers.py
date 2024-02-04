from rest_framework import serializers
from portal.models import Location,Remote,Incident,Subscription
from django.contrib.auth.models import User

class LocationSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Location
        fields = '__all__'

class RemoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remote
        fields = '__all__'

class IncidentSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Incident
        fields = '__all__'

class LimitedLocationSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Location
        fields = ('id', 'name', 'address','serial_number')

class LimitedRemoteSerializer(serializers.ModelSerializer):
    location = LimitedLocationSerializer()
    class Meta:
        model = Remote
        fields = ('id', 'name', 'location',)

class IncidentDetailedSerializer(serializers.ModelSerializer): 
    remote = LimitedRemoteSerializer()
    class Meta:
        model = Incident
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer): 
    #Location = LocationSerializer()
    class Meta:
        model = Subscription
        fields = '__all__'
        #read_only_fields = ['Location']


class SubscriptionDetailedSerializer(serializers.ModelSerializer): 
    location = LocationSerializer()
    class Meta:
        model = Subscription
        fields = '__all__'
        #read_only_fields = ['Location']