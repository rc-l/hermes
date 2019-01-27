from pacioli.models import Accounts, Transactions, Entries
from django.core.exceptions import ValidationError
from django.db.models import ObjectDoesNotExist
from django.db.models.query import QuerySet
import logging
import os
import csv

# TODO: validate transactions without the user waiting on the validation process


def validate(transaction):
    """Tool to validate a transaction.
    
    The following rules apply:
    - A transaction must have two or more account entries associated with it.
    - The sum of all credit and debit entries must be equal.
    
    parameters:
        transaction: instance of the Transactions model
        
    returns:
        valid (bool): indicates whether the transaction is valid or not
        error (str): the first error encountered with the transaction
    """
    assert type(transaction) == Transactions, "Invalid input type"

    entries = transaction.entries_set.all()
    if not len(entries) >= 2:
        return (
            False,
            "A transaction needs 2 or more entries, this transaction has {}".format(
                len(entries)
            ),
        )

    debit = 0.0
    credit = 0.0
    for e in entries:
        if e.credit:
            credit += float(e.amount)
        else:
            debit += float(e.amount)
    if not debit == credit:
        return (
            False,
            "Sum of the amounts in debit and credit entries are not equal. Debit: {} Credit: {}".format(
                debit, credit
            ),
        )

    return True, ""


def batch_validate(batch=None):
    """
    Validate all the transactions. Returns nothing but sets the valid field in the database.

    params:
        batch: Transaction or queryset of transactions, defaults to None

    returns:
        None
    """
    if batch and type(batch) == Transactions:
        # Turn single transaction into queryset
        transactions = Transactions.objects.filter(id=batch.id)
    elif batch and type(batch) == QuerySet and len(batch) > 0:
        # If the queryset contains any objects, check if the objects are transactions
        assert type(batch[0]) == Transactions
    elif batch:
        raise TypeError("The provided batch needs to be a transaction or a queryset")
    else:
        transactions = Transactions.objects.all()
    errors = {}
    for t in transactions:
        valid, error = validate(t)
        if not valid:
            errors[str(t.id)] = error
        t.valid = valid
        try:
            t.full_clean()
            t.save()
        except ValidationError as err:
            logging.error("Transaction: {} error: {} ".format(t.id, err))
