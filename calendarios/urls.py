from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_client_form', views.add_client_form, name='add_client_form'),
    path('test', views.test_mail, name='test'),
]