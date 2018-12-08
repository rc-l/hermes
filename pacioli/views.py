from django.shortcuts import render
from django.views import View
from pacioli.forms import TransactionsForm

class NewTransactionsView(View):
    context = {}
    template = "pacioli/transaction.html"

    def get(self, request):
        self.context['form'] = TransactionsForm()
        return render(request, self.template, self.context)