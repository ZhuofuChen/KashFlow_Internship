import jwt
import random
import string
import json
from bson import ObjectId


def create_token(user_id):
    """Create JWT token"""

    key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    token = jwt.encode({'user_id': user_id}, key).decode('utf8')
    return token, key


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
