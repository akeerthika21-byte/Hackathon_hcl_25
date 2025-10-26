from django.urls import path

from bank_app.views import BankAccountView

urlpatterns = [
    path('accounts/create/', BankAccountView.as_view()),
]