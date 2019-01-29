from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
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
from pacioli.mixins import PagePinningMixin
from pacioli import tools
import logging

logger = logging.getLogger("django.request")

# TODO: Create view for importing csv data


class HomePageView(PagePinningMixin, TemplateView):
    template_name = "pacioli/home.html"


class TransactionListView(PagePinningMixin, ListView):
    """View multiple transactions in a list"""

    # TODO: implement sorting and filtering of transactions
    # TODO: a view of that shows transaction and entries data
    # TODO: a delete button for transactions

    model = Transactions


class TransactionView(UpdateView):
    """View and edit details of a single transaction"""

    model = Transactions
    fields = ["date", "description", "tags", "comments"]
    template_name_suffix = "_update_form"

    def post(self, request, *args, **kwargs):
        """Override post to have the success url to the current page. Since current page can be obtained through the request object it had to be done in a function that has access to this object."""
        self.success_url = request.path
        return super().post(self, request, *args, **kwargs)


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
        url = reverse("transaction-entries", kwargs={"transaction_id": self.object.id})
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
            # Check the validity of the transaction and write that to the database
            # An invalid transaction will not block the creation of the transaction it will just be marked as invalid.
            tools.transaction.batch_validate(context["parent"])
            return redirect(url)
        else:
            context["errors"] = str(formset.errors)
            context["formset"] = formset
        return render(request, self.template_name, context)

class DeleteTransactionView(DeleteView):
    model = Transactions
    success_url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['cancel_url'] = request.session.get("pinned_page") or self.success_url
        return self.render_to_response(context)


    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        success_url = request.session.get("pinned_page") or self.success_url
        return redirect(success_url)