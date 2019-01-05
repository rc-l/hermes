from django.urls import path
from pacioli.views import (
    TransactionView,
    CreateTransactionView,
    UpdateTransactionEntriesView,
    HomePageView,
)

urlpatterns = [
    path("transactions/new/", CreateTransactionView.as_view(), name="new-transaction"),
    path("transactions/<int:transaction_id>/entries", UpdateTransactionEntriesView.as_view(), name="transaction-entries"),
    path("transactions/<int:pk>/", TransactionView.as_view(), name="transaction"),
    path("", HomePageView.as_view(), name="home"),
]
