from django.shortcuts import render
from django.http import HttpResponse

import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

from django.conf import settings

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the schedules index.")

# firebase_config = settings.FIREBASE_CONFIG
# cred = credentials.Certificate(firebase_config)
# print(cred)
# firebase_admin.initialize_app(cred)

def send_fcm_message_to_token(fcm_token, title, body, data=None):
    # Construct message payload
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        topic="your_topic_name",
        data=data  # Optional data payload
    )

    # Send message
    try:
        response = messaging.send(message)
        print("Message sent successfully:", response)
        return True
    except Exception as e:
        print("Error sending message:", e)
        return False


# Message content
title = 'Title of Notification'
body = 'Body of Notification -> 123'
data = {
    'key1': 'value1',
    'key2': 'value2'
}

#send_fcm_message_to_token("", title, body, data)