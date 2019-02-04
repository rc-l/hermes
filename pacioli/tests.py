import pytest
from pacioli import models
from datetime import date
from django.test import Client
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from bs4 import BeautifulSoup
import re

pytestmark = pytest.mark.django_db

data = dict()
client = Client()

## TESTS ##
def test_create_accounts():
    """
    Create accounts both as a test and to supply them to the following tests
    """
    accounts = {}
    accounts['bank'] = models.Accounts(name="bank", credit=False, type="AS")
    assert accounts['bank'].open == date.today()
    assert accounts['bank'].close == None

    accounts['income'] = models.Accounts(name="income", credit=True, type="AS")
    data['accounts'] = accounts

def test_create_new_transaction():
    """
    Create a new transaction.
    Does both a get and post on a page just like a real user would through the UI
    """
    # GET page
    url = reverse_lazy('new-transaction')
    ## Check if page is in configuration
    assert url
    response = client.get(url)
    ## Check if page exists
    assert response.status_code == 200
    ## Check presence of critical elements on page. Also prevents accidentally confguring for the wrong html template
    soup = parse_html(response)
    assert soup.body.find('form', id="transaction_form")
    assert soup.body.find('button', id="submit-button")
    # POST data
    postdata = {'date':date(2018, 12, 31), 'description':'some text'}
    response = client.post(url, postdata)
    ## Verify redirect happens to entries page
    re_test = re.compile("/transactions/[0-9]+/entries")
    assert response.status_code == 302
    assert re_test.match(response.get('Location'))
    data['redirect'] = response.get('Location')
    ## Verify transaction is created with correct data and that redirect happens to the correct transaction's entries
    transaction_id = [int(s) for s in response.get('Location').split('/') if s.isdigit()][0]
    data['transaction_id'] = transaction_id
    try:
        transaction = models.Transactions.objects.get(id=transaction_id)
    except models.Transactions.DoesNotExist:
        assert False, "Transaction is found not in database"
    assert transaction.date == postdata.get('date')
    assert transaction.description == postdata.get('description')

## HELPER CODE ##
def parse_html(response):
    return BeautifulSoup(response.content, 'html.parser')