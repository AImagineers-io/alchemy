from django.urls import path
from . import views

app_name = 'document'

urlpatterns = [
    path('', views.main, name='main-document'),
]
