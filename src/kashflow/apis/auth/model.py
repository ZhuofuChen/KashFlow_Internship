import json
from json import JSONEncoder


class Auth:
    def __init__(self, db):
        self.db = db.auth

    def create_token(self, token_data):
        new_token = self.db.token.insert_one(token_data)
        if new_token is None:
            return {}
        return new_token

    def get_token(self, token):
        result = self.db.token.find_one({'authentication_token': token})
        if result is None:
            return {}
        return result

    def delete_token(self, token):
        deleted_token = self.db.token.delete_one({'authentication_token': token})
        if deleted_token is None:
            return {}
        return deleted_token

    def create_email_token(self, data):
        new_token = self.db.verification_token.insert_one(data)
        if new_token is None:
            return {}
        return new_token

    def get_email_token(self, token):
        result = self.db.verification_token.find_one({'verification_token': token})
        if result is None:
            return {}

        return json.loads(JSONEncoder().encode(dict(result)))

    def delete_email_token(self, token):
        result = self.db.verification_token.delete_one({'verification_token': token})
        if result is None:
            return False
        return True