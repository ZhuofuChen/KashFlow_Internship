from pymongo import MongoClient, errors
from flask import Flask, request
from flask_restplus import Resource, Namespace
# from api import api
from database.db import accountCollection


api = Namespace('account', description='Accounts related operations')


@api.route('/')
class AccountApi(Resource):
    def get(self):
        query = {}
        id = request.args.get("id", None)
        number = request.args.get("number", None)
        fin_institution = request.args.get("fin_institution", None)
        type = request.args.get("type", None)
        sub_type = request.args.get("sub_type", None)

        if id != None:
            query["acc_id"] = id
        if number != None:
            query["acc_number"] = number
        if fin_institution != None:
            query["acc_fin_institution"] = fin_institution
        if type != None:
            query["acc_type"] = type
        if sub_type != None:
            query["acc_sub_type"] = sub_type
        cursor = accountCollection.find(query)
        result = []
        for document in cursor:
            print(document)
            document.pop('_id', None)
            result.append(document)
        return result, 200

    @api.response(200, 'account is successfully created')
    @api.response(204, 'account is already in database with same id')
    def post(self):
        print(request.json)
        data = request.json
        account = {
            "acc_id": data.get("id", ""),
            "acc_number": data.get("number", ""),
            "acc_fin_institution": data.get("fin_institution", ""),
            "acc_sub_type": data.get("sub_type", ""),
            "acc_type": data.get("type", ""),
            "acc_balance": data.get("balance", 0)
        }
        print("account")
        print(account)
        try:
            accountCollection.insert_one(account)
        except errors.DuplicateKeyError:
            return {"acc_id": account['acc_id']}, 201
        return {}, 200
