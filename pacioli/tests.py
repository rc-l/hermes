from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from pacioli import models
from datetime import date
from bs4 import BeautifulSoup
import re

class TestsModels(TestCase):
    def test_accounts_valid(self):
        account = models.Accounts(name="bank", credit=False, type="AS")
        self.assertEqual(account.open, date.today())
        self.assertEqual(account.close, None)
        try:
            account.full_clean()
            clean_success = True
        except:
            clean_success = False
        self.assertTrue(clean_success)

    def test_accounts_invalid_type(self):
        account = models.Accounts(name="bank", credit=False, type="BS")
        with self.assertRaisesRegex(
            ValidationError, "\{'type'\: \[\"Value 'BS' is not a valid choice.\"\]\}"
        ):
            account.full_clean()

    def test_accounts_no_type(self):
        account = models.Accounts(name="bank", credit=False)
        with self.assertRaisesRegex(
            ValidationError, "\{'type'\: \['This field cannot be blank\.'\]\}"
        ):
            account.full_clean()

    def test_accounts_double_name(self):
        account = models.Accounts(name="bank", credit=False, type="AS")
        account.save()
        account2 = models.Accounts(name="bank", credit=True, type="IN")
        with self.assertRaisesRegex(
            ValidationError,
            "\{'name'\: \['Accounts with this Name already exists.'\]\}",
        ):
            account2.full_clean()

class DataPersistence():
    '''
    Object for storing variables over tests, something that the TestCase does not seem to like.
    '''
    pass

class TestsSystem(TestCase):
    """
    All tests in this test case are assumed to be run in the order they are listed below
    """
    data = DataPersistence()

    def test_create_accounts(self):
        """
        Create accounts both as a test and to supply them to the following tests
        """
        accounts = {}
        accounts['bank'] = models.Accounts(name="bank", credit=False, type="AS")
        self.assertEqual(accounts['bank'].open, date.today())
        self.assertEqual(accounts['bank'].close, None)

        accounts['income'] = models.Accounts(name="income", credit=True, type="AS")
        self.assertTrue(accounts)
        self.data.accounts = accounts
        self.assertTrue(self.data.accounts)

    def test_create_new_transaction(self):
        """
        Create a new transaction
        """
        # Check present data
        self.assertTrue(self.data.accounts, "not all the required data is present")
        # GET page
        url = reverse_lazy('new-transaction')
        self.assertTrue(url)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertTrue(soup.body.find('form', id="transaction_form"))
        self.assertTrue(soup.body.find('button', id="submit-button"))
        # POST data
        postdata = {'date':date(2018, 12, 31), 'description':'some text'}
        response = self.client.post(url, postdata)
        re_test = re.compile("/transactions/[0-9]+/entries")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(re_test.match(response.get('Location')))
        transaction_id = [int(s) for s in response.get('Location').split('/') if s.isdigit()][0]
        try:
            transaction = models.Transactions.objects.get(id=transaction_id)
        except models.Transactions.DoesNotExist:
            self.fail("Transaction is not created")
        self.assertEquals(transaction.date, postdata.get('date'))
        self.assertEquals(transaction.description, postdata.get('description'))