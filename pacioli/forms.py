from django.forms import ModelForm, formset_factory, DateInput
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

EntriesFormSet = formset_factory(EntriesForm, min_num=5)