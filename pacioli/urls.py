from django.urls import path
from pacioli.views import TransactionsView, TransactionView, CreateTransactionView, UpdateTransactionEntriesView

urlpatterns = [
    path('transactions/new/', CreateTransactionView.as_view(), name='new-transaction'),
    path('transactions/<int:transaction_id>/entries', UpdateTransactionEntriesView.as_view(), name='transaction-entries'),
    path('transactions/<int:pk>/', TransactionsView.as_view(), name='transaction'),
]
