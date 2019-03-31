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
        self.charges = transaction[2]
        self.balance = transaction[6]


class CheckingTransaction:
    def __init__(self, transaction):
        self.date = transaction[0]
        self.description = transaction[1]
        self.charges = transaction[2]
        self.balance = transaction[3]


TRANSACTION_TYPES = {'VISA': VISATransaction, 'Checking': CheckingTransaction}


def parse():
    transaction_log = sys.argv[1]
    transaction_type = TRANSACTION_TYPES[sys.argv[2]]

    summary = {}

    with open('categories.json') as categories_file:
        categories = json.load(categories_file)

    with open(transaction_log) as transactions:
        csv_reader = csv.reader(transactions, delimiter=',')
        for line in csv_reader:
            transaction = transaction_type(line)

            category = categorize(transaction.description, categories)
            amount = Decimal(transaction.charges.strip('-$'))

            try:
                summary[category] += amount
            except KeyError:
                summary[category] = amount

    # Remember any changes to the categories and keywords
    with open('categories.json', 'w') as categories_file:
        json.dump(categories, categories_file, indent=4)

    for category in summary:
        print('{:>30}: {:>10}'.format(category, summary[category]))


parse()
