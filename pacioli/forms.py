from django.forms import ModelForm
from pacioli import models

class AccountsForm(ModelForm):
    class Meta:
        model = models.Accounts
        fields = ['name', 'open', 'close', 'credit', 'type', 'parent']

class TransactionsForm(ModelForm):
    class Meta:
        model = models.Transactions
        fields = ['date', 'description', 'tags', 'comments']

class EntriesForm(ModelForm):
    class Meta:
        model = models.Entries
        fields = ['transaction', 'account', 'credit', 'amount']