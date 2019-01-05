from pacioli.models import Accounts
from django.core.exceptions import ValidationError
from django.db.models import ObjectDoesNotExist
import logging
import os
import csv


class AccountTools:
    def import_csv(self, file):
        assert type(file) is str

        if os.path.isfile(file):
            with open(file, "r") as f:
                inputdata = list(csv.DictReader(f))
        else:
            raise FileNotFoundError("couldn't find {}".format(file))

        # Convert input into a format usable for bulk creation
        outputdata = []
        for record in inputdata:
            for key in [
                "name",
                "credit",
                "type",
            ]:  # Make sure all the required fields are there
                assert key in record.keys()
            clean = {
                "name": record["name"],
                "type": record["type"],
            }  # Create cleaned set and intialise with the strings
            # Convert the credit boolean
            if record["credit"] == "FALSE":
                clean["credit"] = False
            elif record["credit"] == "TRUE":
                clean["credit"] = True
            else:  # Fail if the value is not clear
                raise ValueError(
                    "{} is not a valid value for credit".format(record["credit"])
                )

            # Check for the optional values
            # Handle parent if present
            if "parent" in record.keys():
                if record["parent"] == "":
                    record[
                        "parent"
                    ] = None  # An empty value can't be dealt with, but None works
                clean["parent"] = record["parent"]

            outputdata.append(clean)  # Append cleaned values to outputlist

        self.bulk_accounts(outputdata)  # Create the accounts based on the cleaned data

    @staticmethod
    def bulk_accounts(data):
        assert type(data) is list

        for record in data:
            for key in [
                "name",
                "credit",
                "type",
            ]:  # Make sure all the required fields are there
                assert key in record.keys()
            # Look up the accounts object for the parent
            if "parent" in record.keys() and record["parent"] is not None:
                try:
                    record["parent"] = Accounts.objects.get(name=record["parent"])
                except Accounts.DoesNotExist as err:
                    logging.warning(
                        "Parent {} could not be found for {}".format(
                            record["parent"], record["name"]
                        )
                    )
            acc = Accounts(
                name=record["name"],
                credit=record["credit"],
                type=record["type"],
                parent=record["parent"],
            )
            try:
                acc.full_clean()
            except ValidationError as err:
                logging.error("{}, based on data {}".format(err, record))
            acc.save()
            logging.info("{:<15} Done".format(record["name"]))
