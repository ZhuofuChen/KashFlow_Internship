import json
from flask import Flask
from flask_pymongo import *
from flask import json
from bson.objectid import ObjectId
from flask_pymongo import *
from util.util import JSONEncoder
from util.util import create_token


app = Flask(__name__)

app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = 27017
app.config['MONGO_DBNAME'] = 'users'

mongo = PyMongo(app, config_prefix="MONGO")


class User():
    def getOne(self, id):
        userResult = mongo.db.user.find_one({'_id': ObjectId(id)})
        if userResult == None:
            return {}

        return json.loads(JSONEncoder().encode(userResult))

    def getByObjectId(self, objectId):
        userResult = mongo.db.user.find_one({'_id': objectId})
        if userResult == None:
            return {}

        return userResult

    def get(self):
        users = mongo.db.user.find({})
        if users == None:
            return []

        return json.loads(JSONEncoder().encode(list(users)))

    def getByUsername(self, username):
        userResult = mongo.db.user.find_one({'username': username})
        if userResult == None:
            return {}

        return userResult

    def createOne(self, userData):

        checkUnique = mongo.db.user.find({'email': userData['email']}).limit(1)
        if list(checkUnique) != []:
            return {"error": "email already exists"}

        checkUnique = mongo.db.user.find({'username': userData['username']}).limit(1)
        if list(checkUnique) != []:
            return {"error": "username already exists"}

        newUser = mongo.db.user.insert_one(userData)
        if newUser == None:
            return {}
        return newUser

    def createAuthenticationToken(self, tokenData):
        newToken = mongo.db.authentication_token.insert_one(tokenData)
        if newToken == None:
            return {}
        return newToken

    def searchAuthenticationToken(self, token):
        result = mongo.db.authentication_token.find_one({'authentication_token': token})
        if result == None:
            return {}
        return result

    def killToken(self, token):
        deletedToken = mongo.db.authentication_token.delete_one({'authentication_token': token})
        if deletedToken == None:
            return {}
        return deletedToken

    def createEmailVerficationToken(self, verificationTokenData):
        newToken = mongo.db.verification_token.insert_one(verificationTokenData)
        if newToken == None:
            return {}
        return newToken

    def searchEmailVerificationToken(self, token):
        result = mongo.db.verification_token.find_one({'verification_token': token})
        if result == None:
            return {}

        return json.loads(JSONEncoder().encode(dict(result)))

    def deleteEmailVerificationToken(self, token):
        result = mongo.db.verification_token.delete_one({'verification_token': token})
        if result == None:
            return False
        return True

    def updateOne(self, id, userData):
        updatedUser = mongo.db.user.update_one({'_id': ObjectId(id)}, {"$set": userData})
        if updatedUser == None:
            return {}
        return updatedUser

    def delete(self, id):
        deletedUserCount = mongo.db.user.delete_one({'_id': ObjectId(id)})
        return deletedUserCount.deleted_count

    def search(self, criteria):
        users = mongo.db.user.find(criteria)
        if users == None:
            return []

        return json.loads(JSONEncoder().encode(list(users)))
