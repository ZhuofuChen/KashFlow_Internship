from flask import Blueprint
from flask_restplus import Api
from apis.users import api as users
from apis.creditcards import api as creditcards
from apis.accounts import api as accounts
from apis.plaid import api as plaid
from apis.sms import api as sms

"""
Flask-RESTPlus implementation layout in the format described in documentation
Ref: http://flask-restplus.readthedocs.io/en/stable/scaling.html
"""

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(
    blueprint,
    title='Kashflow API',
    version='1.0',
    description='Kashflow API',
    # All API metadatas
)

api.add_namespace(users, path='/users')
api.add_namespace(creditcards, path='/creditcards')
api.add_namespace(accounts, path='/accounts')
api.add_namespace(plaid, path='/plaid')
api.add_namespace(sms, path='/sms')
