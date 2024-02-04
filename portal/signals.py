from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

from .serialisers import IncidentDetailedSerializer
from .models import Remote,Incident

from django.conf import settings

firebase_config = settings.FIREBASE_CONFIG
cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred)

def send_fcm_message_to_topic(topic, title, body, data=None):
    # Construct message payload
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        topic=topic,
        data=data
    )

    # Send message
    try:
        response = messaging.send(message)
        print("Message sent successfully:", response)
        return True
    except Exception as e:
        print("Error sending message:", e)
        return False


@receiver(post_save, sender=Remote)
def send_new_Remote(sender, instance, created, **kwargs):
    if created:
        print("Remote Created")#Incident.objects.create(User=instance)
    else:
        print("Remote Updated")


@receiver(post_save, sender=Incident)
def send_new_Incident(sender, instance, created,**kwargs):
    #print(instance,created)
    serializer = IncidentDetailedSerializer(instance)
    serialized_data = serializer.data
    print(serialized_data,created)
    location_serial_number = serialized_data['remote']['location']['serial_number']
    location_address = serialized_data['remote']['location']['address']
    location_name = serialized_data['remote']['location']['name']
    remote_name = serialized_data['remote']['name']
    event_type = serialized_data['event_type']
    call = serialized_data['call']
    acknowledge = serialized_data['acknowledge']
    reset = serialized_data['reset']
    id = serialized_data['id']
    if(created ==True):
        print("Incident Created")
        
    else:
        print("Incident Updated")

    if call != None and acknowledge == None and reset == None:
        step = "Call"
        Title = remote_name + " : " + event_type + " - " + step 
        body = event_type + " " + step + "  from "  + remote_name  + " at " + location_name + ", " + location_address

        send_fcm_message_to_topic(location_serial_number, Title, body, data=None)
        pass
    elif call != None and acknowledge != None and reset == None:
        step = "Acknowledge"
        Title = remote_name + " : " + event_type + " - " + step 
        body = event_type + " " + step + " Recieved from "  + remote_name  + " at " + location_name + ", " + location_address

        send_fcm_message_to_topic(location_serial_number, Title, body, data=None)
        pass
    elif call != None and  reset != None:
        step = "Reset"
        Title = remote_name + " : " + event_type + " - " + step 
        body = event_type + " " + step + " Recieved from "  + remote_name  + " at " + location_name + ", " + location_address

        send_fcm_message_to_topic(location_serial_number, Title, body, data=None)
        pass
# event_type + " " + step + " Recieved from "  + remote_name  + " at " + location_serial_number

'''
{
        "id": 10,
        "remote": {
            "id": 3,
            "name": "Room 1",
            "location": {
                "id": 17,
                "name": "Nursing Station- First Floor",
                "address": "Aditya Birla Hospital, Pune-41"
            }
        },
        "event_type": "House Keeping",
        "call": "2024-02-03T21:21:01.452603+05:30",
        "acknowledge": null,
        "reset": "2024-02-03T21:21:17.126354+05:30",
        "timestamp": "2024-02-03T21:21:01.454106+05:30"
    }
'''