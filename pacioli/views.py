from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView
from django.core.exceptions import ValidationError
from pacioli.forms import TransactionsForm, EntriesFormSet, EntriesForm
from pacioli.models import Transactions, Entries
import logging

logger = logging.getLogger('django.request')

class NewTransactionsView(View):
    context = {}
    template = "pacioli/transaction.html"

    def get(self, request):
        self.context['transactions_form'] = TransactionsForm()
        self.context['entries_formset'] = EntriesFormSet()
        
        return render(request, self.template, self.context)

    def post(self, request):
        transactionform = TransactionsForm(request.POST)
        if transactionform.is_valid():
            transaction = transactionform.save()
            entriesformset= EntriesFormSet(request.POST)
            errors = self._process_entries(entriesformset, transaction)
            if errors:
                logging.error(errors)
                self.context['message'] = errors
                self.context['message_type'] = 'error'

        if "message" in self.context.keys():
            self.context['message_type'] = "error"
            self.context['transactions_form'] = transactionform
            self.context['entries_formset'] = entriesformset
            return render(request, self.template, self.context)
        else:
            self.context['message'] = "Transaction saved sucessfully"
            self.context['message_type'] = "success"
            return redirect(reverse("new-transaction"))

    def _process_entries(self, efs, transaction):
        """
        process the entries in the entries formset.
        Combine the entries with the transaction and validity of each entry.

        TODO: check validity of entire set of entries for transaction.
        """

        # Validate input
        assert type(efs) == EntriesFormSet
        assert type(transaction) == Transactions

        # Templates
        efs_account = 'form-{}-account'
        efs_credit = 'form-{}-credit'
        efs_amount = 'form-{}-amount'

        errors = []
        for i in range(len(efs)):
            if efs.data[efs_account.format(i)] != '':  # Only process the entry if it contains any data
                if efs_credit.format(i) in efs.data.keys() and efs.data[efs_credit.format(i)] == 'on':  # Convert the checkbox to a boolean
                    credit = True
                else:
                    credit = False
                # Create the entry
                data = {'account':efs.data[efs_account.format(i)],
                        'transaction':transaction.id,
                        'credit':credit,
                        'amount':efs.data[efs_amount.format(i)]}
                e = EntriesForm(data)
                if e.is_valid():
                    e.save()
                else:
                    errors.append(e.errors)

        return errors  # Return errors to calling function to handle



class TransactionsView(View):
    context = {}
    template = "pacioli/transaction.html"

    def get(self, request, transaction_id=None):
        if transaction_id:
            transaction = get_object_or_404(Transactions, pk=transaction_id)
            self.context['transactions_form'] = TransactionsForm(instance=transaction)
            queryset = Entries.objects.filter(transaction_id=transaction.id)
            self.context['entries_formset'] = EntriesFormSet(queryset=queryset)
        else:
            self.context['transactions_form'] = TransactionsForm()
            self.context['entries_formset'] = EntriesFormSet()
        
        return render(request, self.template, self.context)

    def post(self, request, transaction_id=None):
        transactionform = TransactionsForm(request.POST)
        if transactionform.is_valid():
            transaction = transactionform.save()
            entriesformset= EntriesFormSet(request.POST)
            errors = self._process_entries(entriesformset, transaction)
            if errors:
                logging.error(errors)
                self.context['message'] = errors
                self.context['message_type'] = 'error'

        if "message" in self.context.keys():
            self.context['message_type'] = "error"
            self.context['transactions_form'] = transactionform
            self.context['entries_formset'] = entriesformset
            return render(request, self.template, self.context)
        else:
            self.context['message'] = "Transaction saved sucessfully"
            self.context['message_type'] = "success"
            return redirect(reverse("new-transaction"))

    def _process_entries(self, efs, transaction):
        """
        process the entries in the entries formset.
        Combine the entries with the transaction and validity of each entry.

        TODO: check validity of entire set of entries for transaction.
        """

        # Validate input
        assert type(efs) == EntriesFormSet
        assert type(transaction) == Transactions

        # Templates
        efs_account = 'form-{}-account'
        efs_credit = 'form-{}-credit'
        efs_amount = 'form-{}-amount'

        errors = []
        for i in range(len(efs)):
            if efs.data[efs_account.format(i)] != '':  # Only process the entry if it contains any data
                if efs_credit.format(i) in efs.data.keys() and efs.data[efs_credit.format(i)] == 'on':  # Convert the checkbox to a boolean
                    credit = True
                else:
                    credit = False
                # Create the entry
                data = {'account':efs.data[efs_account.format(i)],
                        'transaction':transaction.id,
                        'credit':credit,
                        'amount':efs.data[efs_amount.format(i)]}
                e = EntriesForm(data)
                if e.is_valid():
                    e.save()
                else:
                    errors.append(e.errors)

        return errors  # Return errors to calling function to handle

class TransactionView(DetailView):
    model = Transactions
    template_name = "pacioli/transactiondetail.html"

class TransactionView(FormView):
    form_class = TransactionsForm
    template_name = "pacioli/transactions.html"

class CreateTransactionView(CreateView):
    form_class = TransactionsForm
    template_name = "pacioli/transactions.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add title
        context['form_title'] = "Transaction"
        return context

    def get_success_url(self):
        """Override succes url function to dynamically build it based on the successfull object"""
        if not self.object:
            raise ReferenceError("The object is not created")
        url = reverse('transaction-entries', kwargs={'pk':self.object.id})
        return url

# TODO: make a generic view for adding/updating entries for a transaction. Probably use an inline form to do this 