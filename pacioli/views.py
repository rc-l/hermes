from django.shortcuts import render
from django.views import View
from pacioli.forms import TransactionsForm, EntriesFormSet

class NewTransactionsView(View):
    context = {}
    template = "pacioli/transaction.html"

    def get(self, request):
        self.context['transactions_form'] = TransactionsForm()
        self.context['entries_formset'] = EntriesFormSet()
        return render(request, self.template, self.context)