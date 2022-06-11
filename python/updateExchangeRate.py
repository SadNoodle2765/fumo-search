from pymongo import MongoClient
from os import environ
import requests

MONGODB_URL = environ.get('MONGODB_URL')
EXCHANGE_RATE_URL = environ.get('EXCHANGE_RATE_URL')

client = MongoClient(MONGODB_URL)
db = client.fumoApp


def updateExchangeRate():
    rateCollection = db.exchangerates
    rateCollection.drop()

    rate = requests.get(EXCHANGE_RATE_URL).json()

    for currency, value in rate['conversion_rates'].items():
        item = {
            'currency'  : currency,
            'value'     : value
        }

        result = rateCollection.insert_one(item)
        print(f'Added {currency} with value {value}')

    print('Finished adding exchange rates')

if __name__ == '__main__':
    updateExchangeRate()