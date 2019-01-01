from django.forms import ModelForm, modelformset_factory, DateInput, inlineformset_factory
from pacioli import models

class AccountsForm(ModelForm):
    class Meta:
        model = models.Accounts
        fields = ['name', 'open', 'close', 'credit', 'type', 'parent']

class TransactionsForm(ModelForm):
    class Meta:
        model = models.Transactions
        fields = ['date', 'description', 'tags', 'comments']
        widgets = {
            'date': DateInput(attrs={'type': 'date'})
        }
class EntriesForm(ModelForm):
    class Meta:
        model = models.Entries
        fields = ['transaction', 'account', 'credit', 'amount']

EntriesFormSet = modelformset_factory(models.Entries, fields=['transaction', 'account', 'credit', 'amount'], min_num=5)
TransactionEntriesFormSet = inlineformset_factory(models.Transactions,  models.Entries, fields=['id', 'transaction', 'account', 'credit', 'amount'])