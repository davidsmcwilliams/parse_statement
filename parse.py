import sys
import csv
import json


def categorize(description, categories):
    for category in categories:
        print('Category: {0}'.format(category))
        for keyword in categories[category]:
            print('Keyword: {0}'.format(keyword))
            if keyword in description:
                return category
    else:
        add_keyword(description)
        return categorize(description, categories)


def add_keyword(description):
    print("Could not find a category for this transaction: {0}".format(description))
    category = input("Enter a category for this transaction: ")
    keyword = input("Enter a keyword to recognize this transaction in the future: ")

    with open('categories.json') as categories_file:
        categories = json.load(categories_file)
        categories[category].append(keyword)


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

    with open('categories.json') as categories_file:
        categories = json.load(categories_file)

    with open(transaction_log) as transactions:
        csv_reader = csv.reader(transactions, delimiter=',')
        for line in csv_reader:
            transaction = transaction_type(line)
            print(transaction.description)

            category = categorize(transaction.description, categories)
            print(category)


parse()
