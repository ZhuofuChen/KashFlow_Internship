from flask import Flask, request
from flask_restplus import Resource, Namespace
from twilio.rest import Client
# from api import api
import json

api = Namespace('sms', description='SMS related operations')


@api.route('/')
class api_sms(Resource):
    def options(self):
        return json.dumps({})

    @api.response(200, 'sms is successfully sent')
    @api.response(204, 'fail to send')
    def post(self):
        if 'phone_number' in request.form:
            phone_number = request.form['phone_number']
            print("request sending sms to : " + phone_number)
            account_sid = "ACe0df9532253b32f7f3ddf86fbe581b94"
            auth_token = "1621a1fc772f9e90770e3b0d2f170832"
            client = Client(account_sid, auth_token)
            message = client.messages.create(to=phone_number, from_="+12133221432",
                                             body="Kudos on choosing to download Kashflow!!!! \n Android Link:play.google.com \n iOS Link: apple.com")
            return {}, 200
        return {}, 400
