from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import logout, password_reset, password_reset_done, password_reset_confirm
from django.views.generic import ListView, DetailView
from .forms import CustomAuthForm
from .models import Timecard

app_name = 'accounts'

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='accounts/home.html',authentication_form=CustomAuthForm), name='home'),
    path('registration/', views.UserFormView.as_view(), name='registration'),
    path('profile/', views.profile, name='profile'),
    path('management/', views.management, name='management'),
    path('export/xls/', views.export_users_xls, name='export_users_xls'),
    path('export/xls/all', views.export_all_xls, name='exportall'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('timecards/', views.timecards, name='timecards'),
    path('timecards/add/', views.TimeCardCreate.as_view(), name='timecard_add'),
    path('timecards/<int:pk>/', DetailView.as_view(model=Timecard, template_name='accounts/card.html')),
    path('timecards/delete/<int:pk>/', views.TimeCardDelete.as_view(), name='timecard_delete'),
    path('timecards/update/<int:id>/', views.TimeCardUpdate.as_view(), name='timecard_update'),
]
