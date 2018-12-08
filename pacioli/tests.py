from django.test import TestCase
from django.core.exceptions import ValidationError
from pacioli import models
from datetime import date


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
