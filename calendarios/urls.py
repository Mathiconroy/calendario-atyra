from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index, name='index'),
    path('add_client_form', views.add_client_form, name='add_client_form'),
    path('view_client_form/<int:id>', views.view_client_form, name='view_client_form'),
    path('edit_client_form/<int:id>', views.edit_client_form, name='edit_client_form'),
    path('test', views.test_mail, name='test'),
]

urlpatterns += staticfiles_urlpatterns()