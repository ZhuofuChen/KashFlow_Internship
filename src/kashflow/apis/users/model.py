from flask import Flask
from flask_pymongo import *
from bson.objectid import ObjectId
from pymongo import MongoClient
from database.db import userCollection
from database.db import authenticationCollection
from database.db import verificationCollection
import json
from util.util import JSONEncoder

class UserModel():
    #objectId in String format
    def get_by_id_string(self, id):
        # will return None if not found
        res = userCollection.find_one({'_id': ObjectId(id)})
        if res is None:
            return {}
        return res

    def get_by_object_id(self, objectId):
        res = userCollection.find_one({'_id': ObjectId(id)})
        if res is None:
            return {}
        return res

    # return whole user collection with list format
    def get_all(self):
        find_documentation = userCollection.find({})
        if find_documentation is None:
            return {}
        res = list(find_documentation)
        return res
    
    # return the document with username
    def get_by_username(self, username):
        res = userCollection.find_one({'username': username})
        if res is None:
            return{}
        return res
    
    #check whether the user has already exsit by checking email

    def create_user(self, incoming_user):
        check_unique = userCollection.find_one({'email': incoming_user['email']})
        if check_unique is None:
            return {"error": "Internal Server Error: email already exists"}
        check_unique = userCollection.find_one({'username': incoming_user['username']})
        if check_unique is None:
            return {"error": "Internal Server Error: username already exists"}
        res = userCollection.insert_one(incoming_user)
        if res is None:
            return {}
        return newUser

    # return a insertion result
    def insert_user(self, incoming_user):
        #return None or insertResult == insertID
        res = userCollection.insert_one(incoming_user)
        if res is None:
            return {}
        return res
    
    # return a update result
    def update_user(self, id, incoming_user):
        res = userCollection.update_one({"_id" : ObjectId(id)}, {"$set":incoming_user})
        if res is None:
            return {}
        return res

    def delete_user_by_id(self, id):
        res = userCollection.delete_one({'_id': ObjectId(id)})
        return res

    # def delete_by_name(self, name):
    #     return userCollection.delete_one({'name': name})

    #return all collection satisfied criteria
    def search(self, criteria):
        find_documentation = userCollection.find(criteria)
        if find_documentation is None:
            return {}
        # do not know whether accept list(None)
        res = list(find_documentation)
        return res
        # return json.loads(JSONEncoder().encode(res))
        # return json.loads(JSONEncoder().encode({ 'user' : res}))
        # return { 'user' : res}

    ###Authntication token part
    def create_authentication_token(self, tokenData):
        token_res = authenticationCollection.insert_one(tokenData)
        if token_res == None:
            return {}
        return token_res

    def search_authentication_token(self, token):
        token_res = authenticationCollection.find_one({'authentication_token': token})
        if token_res == None:
            return {}
        return result

    def delete_authentication_token(self, token):
	    token_res = authenticationCollection.delete_one({'authentication_token': token})
        if token_res == None:
            return {}
        return token_res
    
    ###email verification
    def create_email_verfication_token(self, verification_token):
        token_res = verificationCollection.insert_one(verification_token)
        if token_res == None:
            return {}
        return token_res

    def search_email_verification_token(self, token):
	    token_res = verificationCollection.find_one({'verification_token': token})
	    if token_res == None:
		    return {}
        return token_res


    def delete_email_verification_token(self, token):
        token_res = verificationCollection.delete_one({'verification_token': token})
        if token_res == None:
            return {}
        return token_res

    def delete_email_verification_token_by_id(self, user_id):
        token_res = verificationCollection.delete_one({'user_id': user_id})
        if token_res == None:
            return {}
        return token_res


    
