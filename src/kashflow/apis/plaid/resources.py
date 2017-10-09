import plaid
import datetime
from flask import request
from flask_restplus import Resource, Namespace
# from api import api
from .test_transactions import data
from database.db import transactionCollection
import json
import os

api = Namespace('plaid', description='Plaid related operations')

# EXPORT PLAID_CLIENT_ID=Yourplaidclient in your Operating System
PLAID_CLIENT_ID = os.environ.get('PLAID_CLIENT_ID')
# EXPORT PLAID_SECRET=Yourplaidsecret in your Operating System
PLAID_SECRET = os.environ.get('PLAID_SECRET')
# EXPORT PLAID_PUBLIC_KEY=Yourplaidpublickey in your Operating System
PLAID_PUBLIC_KEY = os.environ.get('PLAID_PUBLIC_KEY')

# Use 'sandbox' to test with Plaid's Sandbox environment (username: user_good,
# password: pass_good)
# Use `development` to test with live users and credentials and `production`
# to go live
# plaid_ns = api.namespace('plaid', description='Operations related to plaid')
PLAID_ENV = 'development'
client = plaid.Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET,
                      public_key=PLAID_PUBLIC_KEY, environment=PLAID_ENV)
access_token = None


@api.route('/credential')
class GetPlaidAccessToken(Resource):
    def post(self):
        print("Getting access token ")
        global access_token

        public_token = request.form['public_token']
        print("with public token:" + public_token)

        exchange_response = client.Item.public_token.exchange(public_token)
        print('access token: ' + exchange_response['access_token'])

        access_token = exchange_response['access_token']

        return exchange_response, 200


@api.route('/access_token')
class set_access_token(Resource):
    def get(self):
        return {'access_token': access_token}, 200

    def post(self):
        global access_token
        access_token = request.form['access_token']
        print('access token: ' + access_token)
        return {}, 200


@api.route('/accounts')
class accounts(Resource):
    def get(self):
        global access_token
        accounts = client.Auth.get(access_token)
        return accounts, 200


@api.route('/item')
class item(Resource):
    def get(self):
        global access_token
        item_response = client.Item.get(access_token)
        institution_response = client.Institutions.get_by_id(item_response['item']['institution_id'])
        return {'item': item_response['item'], 'institution': institution_response['institution']}, 200


@api.route('/transactions')
class transactions(Resource):
    def get(self):
        global access_token
        # Pull transactions for the last 30 days
        start_date = "{:%Y-%m-%d}".format(datetime.datetime.now() + datetime.timedelta(-30))
        end_date = "{:%Y-%m-%d}".format(datetime.datetime.now())

        # response = client.Transactions.get(access_token, start_date, end_date)
        transactions = data["transactions"]
        print(transactions)

        transactionCollection.insert_many(transactions)

        return "", 200


@api.route('/create_public_token')
class create_public_token(Resource):
    def get(self):
        global access_token
        # Create a one-time use public_token for the Item. This public_token can be used to
        # initialize Link in update mode for the user.
        response = client.Item.public_token.create(access_token)
        return response, 200
