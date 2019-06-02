import sys
import csv
import json
from decimal import Decimal


def categorize(description, categories):
    for category in categories:
        for keyword in categories[category]["Keywords"]:
            if keyword in description:
                return category
    else:
        add_keyword(description, categories)
        return categorize(description, categories)


def add_keyword(description, categories):
    print("Could not find a category for this transaction: {0}".format(description))
    category = input("Enter a category for this transaction: ")
    keyword = input("Enter a keyword to recognize this transaction in the future: ")

    try:
        categories[category]["Keywords"].append(keyword)
    except KeyError:
        categories[category] = {}
        categories[category]["Keywords"] = [keyword]


class VISATransaction:
    def __init__(self, transaction):
        self.date = transaction[0]
        self.description = transaction[1]
        self.charges = transaction[2].replace("$", "")
        self.balance = transaction[5].replace("$", "")


class CheckingTransaction:
    def __init__(self, transaction):
        self.date = transaction[0]
        self.description = transaction[1]
        self.charges = transaction[2].replace("$", "")
        self.balance = transaction[3].replace("$", "")


TRANSACTION_TYPES = {'VISA': VISATransaction, 'Checking': CheckingTransaction}


def parse():
    transaction_log = sys.argv[1]
    transaction_type = TRANSACTION_TYPES[sys.argv[2]]

    summary = {}

    with open('categories.json') as categories_file:
        categories = json.load(categories_file)

    for category in categories:
        summary[category] = {'total': 0, 'transactions': []}

    with open(transaction_log) as transactions:
        csv_reader = csv.reader(transactions, delimiter=',')
        for line in csv_reader:
            transaction = transaction_type(line)

            category = categorize(transaction.description, categories)
            amount = Decimal(transaction.charges)

            summary[category]['transactions'].append(line)
            summary[category]['total'] += amount

    # Remember any changes to the categories and keywords
    with open('categories.json', 'w') as categories_file:
        json.dump(categories, categories_file, indent=4)

    for category in summary:
        if summary[category]['total'] != 0:
            print("--- {0} ---\n".format(category))
            for transaction in summary[category]['transactions']:
                print(transaction)
            print("\n")

    print("------------------------\n\n")

    for category in summary:
        if summary[category]['total'] != 0:
            print('{:>30}: {:>10}'.format(category, summary[category]['total']))


parse()
