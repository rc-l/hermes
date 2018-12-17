from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views import View
from pacioli.forms import TransactionsForm, EntriesFormSet

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
            for form in entriesformset:
                if not form.data['account'] is None:
                    form.data['transaction'] = transaction
            if entriesformset.is_valid():
                entriesformset.save()
            else:
                self.context['message'] = entriesformset.errors
        else:
            self.context['message'] = transaction.errors

        if "message" in self.context.keys():
            self.context['message_type'] = "error"
            return render(request, self.template, self.context)
        else:
            self.context['message'] = "Transaction saved sucessfully"
            self.context['message_type'] = "success"
            return redirect(reverse("new-transaction"))