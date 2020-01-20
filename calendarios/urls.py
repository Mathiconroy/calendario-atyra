from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_client_form', views.add_client_form, name='add_client_form'),
    path('view_client_form/<int:id>', views.view_client_form, name='view_client_form'),
    path('edit_client_form/<int:id>', views.edit_client_form, name='edit_client_form'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='calendarios/login.html')),
    path('test', views.test_mail, name='test'),
]

urlpatterns += staticfiles_urlpatterns()