from django.urls import path
from . import views

app_name = 'document'

urlpatterns = [
    path('', views.main, name='main-document'),
    path('generate-q-and-a/<int:document_id>/', views.generate_q_and_a_view, name="generate-q-and-a"),
    path('edit-q-and-a/<int:document_id>/',views.edit_q_and_a_view, name="edit-q-and-a"),
]


