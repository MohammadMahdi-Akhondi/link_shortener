from django.urls import path

from .api import views

app_name = 'payment'


urlpatterns = [
    path('transaction/callback/', views.CallbackTransactionView.as_view(), name='callback_transaction'),
]
