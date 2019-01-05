from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from pacioli.forms import (
    TransactionsForm,
    EntriesFormSet,
    EntriesForm,
    TransactionEntriesFormSet,
)
from pacioli.models import Transactions, Entries
import logging

logger = logging.getLogger("django.request")


class HomePageView(TemplateView):
    template_name = "home.html"


class TransactionListView(View):
    """View multiple transactions in a list"""

    pass


class TransactionView(DetailView):
    """View details of a single transaction"""

    model = Transactions
    template_name = "pacioli/transactiondetail.html"


class CreateTransactionView(CreateView):
    """Create a new transaction. This will redirect to the entries for this transaction upon completion"""

    form_class = TransactionsForm
    template_name = "pacioli/transactions.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add title
        context["form_title"] = "Transaction"
        return context

    def get_success_url(self):
        """Override succes url function to dynamically build it based on the successfull object"""
        if not self.object:
            raise ReferenceError("The object is not created")
        url = reverse("transaction-entries", kwargs={"pk": self.object.id})
        return url


class UpdateTransactionEntriesView(View):
    """Create or update the entries to a transaction"""

    template_name = "pacioli/transaction_entries.html"

    def get(self, request, transaction_id):
        context = {}
        context["parent"] = get_object_or_404(Transactions, pk=transaction_id)
        context["formset"] = TransactionEntriesFormSet(instance=context["parent"])
        return render(request, self.template_name, context)

    def post(self, request, transaction_id):
        context = {}
        context["parent"] = get_object_or_404(Transactions, pk=transaction_id)
        formset = TransactionEntriesFormSet(request.POST, instance=context["parent"])
        logger.info(formset.data)
        if formset.is_valid():
            formset.save()
            if "pinned_page" in request.session:
                url = request.session["pinned_page"]
            else:
                url = reverse("home")
            redirect(url)
        else:
            context["errors"] = str(formset.errors)
            context["formset"] = formset
        return render(request, self.template_name, context)
