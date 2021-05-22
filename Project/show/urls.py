from django.urls import path
from .test import show
urlpatterns=[
    path('',show, name='home')
]