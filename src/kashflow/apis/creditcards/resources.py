from pymongo import MongoClient, errors
from flask import Flask, request
from flask_restplus import Resource, Namespace, fields
# from api import api
from database.db import creditcardCollection


api = Namespace('creditcards', description='Credit card related operations')
# creditcard_ns = api.namespace('creditcard', description='Opreations related to credit card')

credit_card_fields = api.model('creditcard', {
    'card_name': fields.String(attribute='c_card_name'),
    'bonus_offer': fields.String(attribute='c_card_bonus_offer'),
    'rewards_rate': fields.String(attribute='c_card_rewards_rate'),
    'annual_fee': fields.String(attribute='c_card_annual_fee'),
    'intro_apr': fields.Integer(attribute='c_card_intro_apr'),
    'ongoing_apr': fields.Integer(attribute='c_card_ongoing_apr')
})


@api.route('/')
class CreditcardApi(Resource):
    @api.marshal_with(credit_card_fields)
    def get(self):
        query = {}
        card_name = request.args.get("card_name", None)
        if card_name != None:
            query["c_card_name"] = id
        cursor = creditcardCollection.find(query)
        result = []
        for document in cursor:
            print(document)
            document.pop('_id', None)
            result.append(document)
        return result

    def post(self):
        print(request.json)
        data = request.json
        card = {
            "c_card_name": data.get("card_name", ""),
            "c_card_bonus_offer": data.get("bonus_offer", ""),
            "c_card_rewards_rate": data.get("rewards_rate", ""),
            "c_card_annual_fee": data.get("annual_fee", ""),
            "c_card_intro_apr": data.get("intro_apr", 0),
            "c_card_ongoing_apr": data.get("ongoing_apr", 0)
        }
        print("credit card")
        print(card)
        creditcardCollection.insert_one(card)
        return {}, 200

    @api.response(204, 'delete creditcard')
    def delete(self):
        query = {}
        card_name = request.args.get("card_name", None)
        print(card_name)
        if card_name is not None:
            query["c_card_name"] = card_name
        if query:
            print(query)
            creditcardCollection.delete_many(query)
        return '', 204