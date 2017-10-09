from flask_restplus import Namespace, Resource, fields
from .model import UserModel
from api import api
from bson.objectid import ObjectId

user_ns = api.namespace('user', description='Operations related to user')

'''Response Marshals'''
user_output = api.model('user_output', {
    'user_id': fields.String(description='User Id'),
    'username': fields.String(description='Username of a user'),
    'first_name': fields.String(description='First name of a user'),
    'last_name': fields.String(description='Last Name of a user'),
    'email': fields.String(description='Email Address'),
    'date_of_birth': fields.DateTime(description='Date of birth of a user'),
    'active': fields.Boolean(description='Is the user active'),
    'creation_date': fields.DateTime(description='Date when the user was created'),
    'email_verified': fields.Boolean(description='Is the email verified'),
    'address_line_one': fields.String(description='First line of the address'),
    'address_line_two': fields.String(description='Second line of the address'),
    'city': fields.String(description='City'),
    'state': fields.String(description='State'),
    'zip': fields.Integer(description='Zip code'),
    'license': fields.String(description='license number')
    })

user_input = api.model('user_input', {
    'username': fields.String(description='Username of a user'),
    'password': fields.String(description='Password of a user'),
    'first_name': fields.String(description='First name of a user'),
    'last_name': fields.String(description='Last Name of a user'),
    'email': fields.String(description='Email Address'),
    'date_of_birth': fields.DateTime(description='Date of birth of a user'),
    'address_line_one': fields.String(description='First line of the address'),
    'address_line_two': fields.String(description='Second line of the address'),
    'city': fields.String(description='City'),
    'state': fields.String(description='State'),
    'zip': fields.Integer(description='Zip code'),
    'ssn': fields.Integer(description='social security number'),
    'license': fields.String(description='license number')
    })
#authentication and verification
authentication_token = api.model('authentication_token', {
    'user_id': fields.String(description="User id associated with the token"),
    'authentication_token': fields.String(),
    'salt': fields.String()
})

verification_token = api.model('verification_token', {
    'user_id': fields.String(description="User id associated with the token"),
    'verification_token': fields.String(description='Verification token for a user')
})
#successful_response_model
successful_response_model = api.model('successful_response_model', {
    'message': fields.String(description="Status message")
})

response_success = {
    'message': 'Successful'
}
#login
login_input = api.model('user_login_input', {
    'username': fields.String( description='Username of a user', location='json'),
    'password': fields.String( description='Password of a user', location='json')
})

login_success = api.model('login_success', {
    'user_id': fields.String( description='User id of a user'),
    'authentication_token': fields.String( description='Authentication token for a user')
})

#LIST ALL THE USERS
@api.route('/users')
class UserList(Resource):
    @api.doc('List Users')
    # match every eles in output list
    @api.marshal_list_with(user_output)
    @api.response(200, 'Users Fetched Successfully', [user_output])
    @api.response(403, "Not authenticated")
    #extra @
    @api.header('x-access-token', 'authentication token', required=True)
    @requires_auth
    def get(self):
        #docStr
        '''List all user'''
        users = UserModel.get_all(self)
        return users

#CREATE USER
user_get_parser = api.parser()
# I do not add license state
user_post_parser = api.parser()
user_parser.add_argument(
    'data',
    type = user_input
    # require = True
)
@api.route('/user')
class UserPost(Resource):
    @api.doc('Post/Add User')
    # @api.marshal_with(user_output)
    @api.response(200, 'User Added to User List Successfully')
    # @api.response(500, 'Cannot Insert the User')
    @api.response(500, 'Internal Server Error: email already exists')
    @api.response(500, 'Internal Server Error: username already exists')
    @api.response(500, 'Internal Server Error: Can Not Create the User')
    @api.response(500, 'Internal Server Error: Can not create authentication token')
    @api.response(500, 'Internal server error: Can not create verification token')
    #extra @
    @api.expect(user_post_parser)  #for input
    def post(self):
        '''Add a New User'''
        args = user_post_parser.parse_args()
        incomingUserData = args['data']

        # Hashing Password before store into the db!
        hashed_password = bcrypt.hashpw(str(args['password']).encode('utf8'), bcrypt.gensalt())
        incomingUserData['password'] = hashed_password
        insert_one_result = UserModel.create_user(self, incomingUserData)
        if isinstance(insert_one_result, dict) and 'error' in insert_one_result.keys():
            api.abort(500, newUser['error'])
        # Have not confirmed the usage of insertOneResult.key() !!!
        if insert_one_result == {}:
            api.abort(500, 'Internal Server Error: Can Not Create the User')
        user_inserted_id = insert_one_result.inserted_id

        #create authentication token for the user
        token = create_token(str(user_inserted_id), key).decode("utf-8")
        key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        expiration = datetime.datetime.utcnow() + datetime.timedelta(days=30)

        tokenObj = {
            'user_id': user_inserted_id,
            'authentication_token': token,
            'salt': key,
            'expires': expiration 
        }
        # create it/put it into database
        auth_res = UserModel.create_authentication_token(tokenObj)
        if auth_res == {}:
            api.abort(500, 'Internal Server Error: Can not create authentication token')

        # create verification token and send email to verify user
        verificationToken = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        verificationTokenObj = {
            'user_id': user_inserted_id,
            'verification_token': str(verificationToken)
        }
        veri_res = UserModel.create_email_verfication_token(verificationTokenObj)
        if veri_res == {}:
            api.abort(500, 'Internal server error: Can not create verification token')
        
        emailResponse = sendEmail(CONFIG['email'], args['email'], 'Verify email address', CONFIG['host']+'user/verify?token='+verificationToken)
        if emailResponse == {}:
            api.abort(500, 'Email could not be delivered')
        # expose only user_id and user authentication toekn 
        # not necessary return all user's information
        response = {'user_id': str(user_inserted_id), 'authentication_token': token}
        return response, 200

user_delete_parser = api.parser()
user_delete_parser.add_argument(
    'data',
    type = user_input
    # require = True
)

@api.route('/user/<id>')
class User(Resource):
    @api.doc('Get User')
    @api.marshal_with(user_output)
    @api.param('id', 'The User ID')
    @api.response(401, "Not authenticated")
    @api.response(404, 'User Not Found')
    @api.response(200, 'User Found Successfully', user_output)
    #extra @
    @api.header('x-access-token', 'authentication token', required=True)
    @requires_auth
    
    def get(self, id):
        '''Fetch a User with Given ID'''
        target_user = UserModel.get_by_id_string(self, id)
        if target_user == {}:
            api.abort(404, 'User Not Found')
        return target_user, 200

#UserModel.post
    #Put method should be idempotent
    #principal of this product => the _id should not be specified by Client
    @api.doc('Put/Update User')
    @api.marshal_with(user_output)
    @api.param('id', 'The User ID')
    @api.response(200, 'User Updated Successfully', user_output)
    @api.response(500, 'Cannot Updated the User')
    @api.response(401, "Not authenticated")
    @api.response(404, 'User Not Found')
    #extra @
    @api.expect(user_put)
    @api.header('x-access-token', 'authentication token', required=True)
    requires_auth
    def put(self, id): 
        '''Update an Existinng User'''
        #check whether it's existed or not
        checkResult = UserModel.get_by_id_string(self, id)
        if (checkResult is None):
            api.abort(404, 'User Not Found')
        args = user_parser.parse_args()
        incomingUserData = args['data']
        upserted_res = UserModel.update_user(self, id, incomingUserData)
        if upserted_res == {}:
            api.abort(500, 'Cannot Updated the User')
        res = UserModel.get_by_id_string(self, id)
        return res, 
    

    @api.doc('delete_user')
    @api.param('id', 'The User ID')
    @api.response(500, 'Cannot Delete the Specified User')
    @api.response(200, 'Specified User Does Not Exist Anymore')
    #extra @
    @api.header('x-access-token', 'authentication token', required=True)
    @requires_auth
    def delete(self, id):
        '''Delete a User with Given ID'''
        checkResult = UserModel.get_by_id_string(self, id)
        if (checkResult is None):
            return {"No Specified User Found" : "Equal to Deleted"}, 200
        delete_one_result = UserModel.delete_by_id(self, id)
        deleted_count = delete_one_result.deleted_count
        if (deleted_count == 0):
            api.abort(500, 'Cannot Delete the Specified User')
        return {"Specified User Deleted" : "Done"}, 200

    #Search User
    user_search_parser = api.parser()
    user_search_parser.add_argument(
        'data',
        type = dict,
        # requre = True
    )
    @api.route('/user/search')
    class UserSearch(Resource):
        
        @api.doc('search_user')
        @api.marshal_with(user_output)
        # @api.expect(user_output)
        @api.response(200, 'Loading Search Result Successfully')
        
        def post(self):
            '''Search Users'''
            args = user_search_parser.parse_args()
            criteria = args['data']
            res = UserModel.search(self, criteria)
            print(res)
            print("second time")
            return res, 200

#From here
login_post = api.parser() 
login_post.add_argument('username', required=True)
login_post.add_argument('password', required=True)

@api.route('/login')
class Login(Resource):

    @api.expect(login_post)
    @api.response(200, 'Login Successful', login_success)
    @api.response(401, 'username or password does not match')
    @api.doc('user login')
    def post(self):
        '''Accepts a username and password to create a new token'''
        args = login_post.parse_args()
        userData = userModel.getByUsername(args['username'])
        expiration = datetime.datetime.utcnow() + datetime.timedelta(days=30)

        if bcrypt.checkpw(args['password'].encode('utf8'), userData['password']):

            '''delete any existing tokens if any'''
            deletedTokensCount = userModel.delete_authentication_token(userData['_id'])
            if deletedTokensCount != 0:
                print(deletedTokensCount, "Tokens removed")

            key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
            token = create_token(str(userData['_id']), key).decode('utf8')

            '''Adding expiration to expand functionality for the future'''

            tokenObj = {
                'user_id': userData['_id'],
                'authentication_token': token,
                'salt': key,
                'expires': expiration
            }
            insertedToken = userModel.createAuthenticationToken(tokenObj)
            if insertedToken == {}:
                api.abort(500, 'Internal Server Error')
                response = {'user_id': str(userData['_id']), 'authentication_token': token}
                '''Since mongo is fire and forget, use the id and token generated before insertion'''
                return response
            else:
                api.abort(401, 'username or password does not match')


logout_post = api.parser()
logout_post.add_argument('user_id', required=True)
logout_post.add_argument('x-access-token', required=True, location='headers')


@api.route('/logout')
class Logout(Resource):
  
    @api.response(200, 'Logout Successful', successful_response_model)
    @api.response(404, 'Token not found')
    @api.expect(logout_post)
    @api.header('x-access-token', 'authentication token', required=True)
    @api.doc('user logout')
    def post(self):
        '''kills the access token'''
        token = logout_post.parse_args()['x-access-token']
        user_id = logout_post.parse_args()['user_id']
        killedToken = userModel.delete_authentication_token(token)
        if killedToken == {}:
            return api.abort(404, 'Token not found')

        return response_success


verify_get = api.parser()
verify_get.add_argument('token', location='args')


@api.route('/verify')
class Verify(Resource):
    @api.expect(verify_get)
    @api.response(200, 'Email verified', successful_response_model)
    @api.response(404, 'Token not found')
    @api.doc("Verify email")
    def get(self):
        '''Verify email'''
        token = verify_get.parse_args()['token']
        verificationTokenLookup = userModel.search_email_verification_token(token)
        if verificationTokenLookup == {}:
            api.abort(404, 'Token not found')

        userData = userModel.get_by_id_string(verificationTokenLookup['user_id'])
        userData['email_verified'] = True
        del userData['_id']

        updatedUserData = userModel.update_user(verificationTokenLookup['user_id'], userData)
        if updatedUserData == {}:
            api.abort(404, 'User not found')

        deleteVerificationToken = userModel.delete_email_verification_token(verificationTokenLookup['verification_token'])
        if deleteVerificationToken == {}:
            api.abort(500, 'Internal Server Error')

        return response_success


forgot_post = api.parser()
forgot_post.add_argument('user_id', required=True)
forgot_post.add_argument('email', required=True)


@api.route('/forgot')
class Forgot(Resource):
  
    @api.expect(forgot_post)
    @api.response(200, 'Email successfully sent')
    @api.response(404, 'Email not found')
    @api.response(401, 'Not authenticated')
    def post(self):
        '''Send email to reset password'''
        user_id = forgot_post.parse_args()['user_id']
        email = forgot_post.parse_args()['email']

        user_output = userModel.getOne(user_id)

        if email == user_output['email']:
            #what if this delete is not succssful?
            delete_email_verification_token_by_id(self, user_id)
            tempPassword = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])
            tempPasswordObj = {
                'user_id': user_id,
                'verification_token': tempPassword
            }
            insertedVerificationToken = userModel.create_email_verfication_token(tempPasswordObj)
            if insertedVerificationToken == {}:
                api.abort(500, 'Internal server error')
            
            #if temp password has been updated 
            


            '''send email with temp password'''
            emailResponse = sendEmail('mightyhost0@gmail.com', email, 'New Password', tempPassword)
            if emailResponse == {}:
                api.abort(500, 'Internal server error')
        else:
            api.abort(404, "Email not found")

        return response_success


reset_post = api.parser()
reset_post.add_argument('old_password', required=True)
reset_post.add_argument('new_password', required=True)


@api.route('/reset')
class Reset(Resource):

    @api.expect(reset_post)
    @api.response(200, 'Password successfully sent')
    @api.response(404, 'User not found')
    def post(self):
        '''Reset password'''
        old_password = reset_post.parse_args()['old_password']
        new_password = reset_post.parse_args()['new_password']
        # Here toekn is same as the temp_password
        tempPasswordLookup = userModel.searchEmailVerificationToken(old_password)
        if tempPasswordLookup == {}:
            api.abort(401, "Password not found")

        #update verification data for future reset code
        delete_email_verification_token(self, old_password)
        newPasswordObj = {
                'user_id': user_id,
                'verification_token': new_password
            }
        insertedVerificationToken = userModel.create_email_verfication_token(newPasswordObj)
        if insertedVerificationToken == {}:
            api.abort(500, 'Internal server error')

        hashedPassword = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt())

        userData = userModel.get_by_id_string(tempPasswordLookup['user_id'])

        if userData == {}:
            api.abort(404, 'User Not found')

        userData['password'] = hashedPassword

        userId = ''
        if '_id' in userData.keys():
            userId = userData['_id']
            del userData['_id']
        else:
            api.abort(500, 'Internal server error')

        updatedUserData = userModel.update_user(userId, userData)

        if (updatedUserData == {}):
            api.abort(404, 'User Not found')

        return response_success