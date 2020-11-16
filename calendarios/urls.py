from django.urls import path
from . import views
from .forms import LoginForm
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_client_form', views.add_client_form, name='add_client_form'),
    path('view_client_form/<int:id>', views.view_client_form, name='view_client_form'),
    path('edit_client_form/<int:id>', views.edit_client_form, name='edit_client_form'),
    path('view_reservation_requests', views.view_reservation_requests, name='view_reservation_requests'),
    path('login/', auth_views.LoginView.as_view(template_name='calendarios/login.html', authentication_form=LoginForm), name='login'),
    path('logout', views.logout, name='logout'),
    path('test', views.test_mail, name='test'),
    path('search_reservation', views.search_reservation, name='search_reservation'),
    path('confirm_reservation/<int:id>', views.confirm_reservation, name='confirm_reservation'),
    path('delete_reservation/<int:id>', views.delete_reservation, name='delete_reservation'),
    path('change_payment/<int:id>', views.change_payment, name='change_payment'),
]

urlpatterns += staticfiles_urlpatterns()