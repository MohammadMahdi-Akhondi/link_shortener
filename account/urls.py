from django.urls import path

from .api import views

app_name = 'account'


urlpatterns = [
    path('registration/', views.UserRegistrationView.as_view(), name='user_registration'),
    path('activate/<str:token>/', views.UserActivateView.as_view(), name='user_activate'),
    path('phone/activate/', views.UserPhoneActivateView.as_view(), name='phone_activate'),
    path('phone/verify/', views.UserPhoneVerifyView.as_view(), name='phone_verify'),
    path('upgrade/', views.UserUpgradeView.as_view(), name='user_upgrade'),
]
