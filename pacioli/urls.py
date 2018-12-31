from django.urls import path
from pacioli.views import TransactionsView, TransactionView, CreateTransactionView

urlpatterns = [
    path('transactions/new/', CreateTransactionView.as_view(), name='new-transaction'),
    path('transactions/<int:pk>/entries', TransactionsView.as_view(), name='transaction-entries'),
    path('transactions/<int:pk>/', TransactionsView.as_view(), name='transaction'),
]
