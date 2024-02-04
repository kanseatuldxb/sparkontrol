from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),

    path('location/', views.LocationList.as_view()),
    path('location/<int:pk>/', views.LocationDetail.as_view()),

    path('remote/', views.RemoteList.as_view()),
    path('remote/<int:pk>/', views.RemoteDetail.as_view()),

    path('incident/', views.IncidentList.as_view()),
    path('incident/<int:pk>/', views.IncidentDetail.as_view()),

    path('subscription/', views.SubscriptionList.as_view()),
    path('subscription/<int:pk>/', views.SubscriptionDetail.as_view()),

    path('create-incident/', views.CreateIncident.as_view(), name='create-incident')
    
]

urlpatterns = format_suffix_patterns(urlpatterns)