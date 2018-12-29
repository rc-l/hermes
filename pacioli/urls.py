from django.urls import path
from pacioli.views import NewTransactionsView

urlpatterns = [
    path('transactions/new/', NewTransactionsView.as_view(), name='new-transaction'),
]