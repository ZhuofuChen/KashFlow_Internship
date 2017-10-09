from pymongo import MongoClient, errors
from flask import g
from flask import Flask
from flask import current_app


def connect(uri='localhost:27017'):
    """Creates a configurable connections to MongoDb"""
    try:
        client = MongoClient(uri)
        db = client[current_app.config['DATABASE']]
    except errors.ConnectionFailure:
        raise

    print('Connected to database: {}'.format(current_app.config['DATABASE']))

    return db


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'db'):
        try:
            g.db = connect()
        except errors.ConnectionFailure:
            raise
    return g.db


def close_db_factory(app):
    @app.teardown_appcontext
    def close_db(error):
        """Closes the database again at the end of the request."""
        if hasattr(g, 'db'):
            g.db.client.close()

    return close_db

# Statements remain to support endpoints until full refactor is complete
mdb_client = MongoClient()
mdb = mdb_client.kashflow
userCollection = mdb['user']
accountCollection = mdb['account']
creditcardCollection = mdb['creditcard']
transactionCollection = mdb['transaction']
userCollection.create_index('u_id', unique=True)
accountCollection.create_index('acc_id', unique=True)

