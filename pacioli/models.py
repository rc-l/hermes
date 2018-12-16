from django.db import models
from datetime import date

# Create your models here.
class Accounts(models.Model):
    """
    Accounting accounts on which entries can be made.
    """

    TYPES = [
        ("AS", "asset"),  # Eg. Cash in bank
        ("LI", "liability"),  # Eg. Loans, provisions
        ("IN", "income"),  # Eg. Sales, salary
        ("EX", "expense"),  # Eg. Office supplies, paying bills
        ("EQ", "equity"),  # Eg. Initial capital
    ]
    open = models.DateField(default=date.today)
    close = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=30, unique=True)
    credit = models.BooleanField()
    type = models.CharField(choices=TYPES, max_length=2)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Balances(models.Model):
    """
    Once the balance for an account is calculated the value is stored here. This is to prevent recalculation every time the balance is requested.
    """

    account = models.OneToOneField("Accounts", on_delete=models.CASCADE)
    calculation = models.DateTimeField(
        auto_now=True,
        help_text="The time at which the calculation for the balance was done",
    )
    effective_time = models.DateTimeField(
        help_text="Point in time for which the balance is calculated"
    )
    balance = models.IntegerField()


class Entries(models.Model):
    """
    One entry to an account. This is always relate to an transaction which will consist of multiple entries.
    """

    transaction = models.ForeignKey("Transactions", on_delete=models.CASCADE)
    account = models.ForeignKey("Accounts", on_delete=models.PROTECT)
    credit = models.BooleanField()
    amount = models.PositiveIntegerField()


class Transactions(models.Model):
    """
    Transaction is used to register any finanicial transaction or mutation. It always consists of multiple entries.
    """

    created = models.DateField(auto_now_add=True)
    date = models.DateField()
    description = models.CharField(max_length=200)
    tags = models.CharField(max_length=200)  # Should contain a json
    comments = models.CharField(max_length=500)


class Imports(models.Model):
    """
    Store imported records for later auditing purposes and automated processing of imported data through pattern matching.
    """

    created = models.DateField(
        auto_now_add=True, help_text="The date this record was created"
    )
    date = models.DateField(
        help_text="The date of the transaction occurred according to the imported data"
    )
    description = models.CharField(max_length=500)
    concat = models.CharField(
        max_length=200,
        help_text="This field contains several values from the import that can be used for matching on an boolean equals basis",
    )
    comments = models.TextField()
    amount = models.PositiveIntegerField()
    transaction = models.ForeignKey("Transactions", on_delete=models.PROTECT)
    raw = models.TextField(
        help_text="Should contain the raw import value for this record"
    )
    descriptor = models.ForeignKey("ImportDescriptors", on_delete=models.PROTECT)


class ImportDescriptors(models.Model):
    """
    Define how values from import files should be mapped to the fields in Imports.
    """

    name = models.CharField(unique=True, max_length=30)
    mapping = models.TextField(
        help_text="JSON describing which value in the Imports table is which value in the file"
    )
