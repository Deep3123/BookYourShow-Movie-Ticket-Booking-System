from django.urls import path
from ticketbooker.views import *

urlpatterns = [
    path('theatres/', theatre_list, name='theatre-list'),
    path('showtimings/',show_timings_list, name='showtimings-list'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('password-reset/', CustomPasswordResetAPI.as_view(), name='password_reset_api'),
    path('create-payment-intent/', create_payment_intent, name='create-payment-intent'),
    path('password-reset-confirm/', PasswordResetConfirmAPI.as_view(), name='password_reset_confirm'),
]