from django.shortcuts import render
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
            # TODO: validate forms
            # TODO: save forms
        # TODO: handle invalid transaction form
        # TODO: handle invalid entries
        # Handle both by loading the page again with the posted data and a message displaying the issues
        self.context['message'] = transaction.data
        return HttpResponse(self.context.keys())