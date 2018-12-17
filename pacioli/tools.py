from pacioli.models import Accounts
from django.core.exceptions import ValidationError
import logging

def bulk_accounts(data):
    assert type(data) is list

    for record in data:
        acc = Accounts(record)
        try:
            acc.full_clean()
        except ValidationError as err:
            logging.error("{}, based on data {}".format(err, record))
        acc.save()
        logging.info("{:<15} Done".format(record['name']))

