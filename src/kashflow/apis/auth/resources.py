from ..users import model, resources
from flask_restplus import Namespace, Resource, fields
from . import model


api = Namespace('auth', description='Authentication related operations')


authentication_token = api.model('authentication_token', {
    'user_id': fields.String(description="User id associated with the token"),
    'authentication_token': fields.String(),
    'salt': fields.String()
})

verification_token = api.model('verification_token', {
    'user_id': fields.String(description="User id associated with the token"),
    'verification_token': fields.String()
})

deletion_success = api.model('deletion_success', {
    'message': fields.String(description="Status message")
})

login_input = api.model('user_login_input', {
    'username': fields.String(description='Username of a user', location='json'),
    'password': fields.String(description='Password of a user', location='json')
})

reset_input = api.model('reset_input', {
    'temp_password': fields.String(description='Temporary password', location='json'),
    'new_password': fields.String(description='New password', location='json')
})

forgot_input = api.model('forgot_input', {
    'user_id': fields.String(description='User id', location='json'),
    'email': fields.String(description='email address of the user', location='json')
})

login_success = api.model('login_success', {
    'user_id': fields.String(description='User id of a user'),
    'authentication_token': fields.String(description='Authentication token for a user')
})

logout_success = api.model('logout_success', {
    'message': fields.String(description="Status message")
})

logout_input = api.model('logout_input', {
    'user_id': fields.String(description="User Id")
})

verification_failure = {
    'message': 'could not verify'
}


# @api.route('/login')
# class Login(Resource):
#     @api.expect(login_input)
#     @api.response(200, 'Login Successful', login_success)
#     @api.response(401, 'username or password does not match')
#     @api.doc('user login')
#     def post(self):
#         '''Accepts a username and password to create a new token'''
#         args = user_login_post.parse_args()
#         userData = users.get(args['username'])
#
#         if bcrypt.checkpw(args['password'].encode('utf8'), userData['password']):
#             key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
#             token, key = model.create_token(str(userData['_id']))
#             tokenObj = {
#                 'user_id': userData['_id'],
#                 'authentication_token': token,
#                 'salt': key
#             }
#             insertedToken = userModel.createAuthenticationToken(tokenObj)
#             response = {'user_id': str(userData['_id']), 'authentication_token': token}
#             return response
#         else:
#             api.abort(401, 'username or password does not match')
#
#
# logout_post = api.parser()
# logout_post.add_argument('user_id', required=True)
# logout_post.add_argument('x-access-token', required=True, location='headers')
#
#
# @api.route('/logout')
# class Logout(Resource):
#     @api.response(200, 'Logout Successful', logout_success)
#     @api.response(404, 'Token not found')
#     @api.expect(logout_input)
#     @api.header('x-access-token', 'authentication token', required=True)
#     @api.doc('user logout')
#     def post(self):
#         '''kills the access token'''
#         token = logout_post.parse_args()['x-access-token']
#         user_id = logout_post.parse_args()['user_id']
#         killedToken = userModel.killToken(token)
#         if killedToken == {}:
#             return api.abort(404, 'Token not found')
#         return {'message': 'LOgout Successful'}
#
#
# verify_get = api.parser()
# verify_get.add_argument('token', location='args')
#
#
# @api.route('/verify')
# class Verify(Resource):
#     @api.expect(verify_get)
#     @api.response(200, 'Email verified')
#     @api.response(404, 'Token not found')
#     def get(self):
#         '''Verify email'''
#         token = verify_get.parse_args()['token']
#         verificationTokenLookup = userModel.searchEmailVerificationToken(token)
#         if verificationTokenLookup == {}:
#             return verification_failure
#
#         userData = userModel.getOne(verificationTokenLookup['user_id'])
#         userData['email_verified'] = True
#         del userData['_id']
#
#         updatedUserData = userModel.updateOne(verificationTokenLookup['user_id'], userData)
#         if updatedUserData == {}:
#             return verification_failure
#
#         deleteVerificationToken = userModel.deleteEmailVerificationToken(verificationTokenLookup['verification_token'])
#         if deleteVerificationToken == {}:
#             return verification_failure
#
#         return {'message': 'Verified'}
#
#
# forgot_post = api.parser()
# forgot_post.add_argument('x-access-token', required=True, location='headers')
# forgot_post.add_argument('user_id', required=True)
# forgot_post.add_argument('email', required=True)
#
#
# @api.route('/forgot')
# class Forgot(Resource):
#     @api.expect(forgot_input)
#     @api.response(200, 'Email successfully sent')
#     @api.response(404, 'Email not found')
#     @api.response(401, 'Not authenticated')
#     def post(self):
#         '''Send email to reset password'''
#         token = forgot_post.parse_args()['x-access-token']
#         user_id = forgot_post.parse_args()['user_id']
#         email = forgot_post.parse_args()['email']
#
#         search_token = userModel.searchAuthenticationToken(token)
#         print(type(str(search_token['user_id'])), user_id)
#         if search_token == False:
#             api.abort(401, "Not authenticated")
#         if str(search_token['user_id']) != user_id:
#             api.abort(401, "Not authenticated")
#
#         user_output = userModel.getOne(user_id)
#
#         if email == user_output['email']:
#             tempPassword = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])
#             tempPasswordObj = {
#                 'user_id': user_id,
#                 'verification_token': tempPassword
#             }
#             insertedVerificationToken = userModel.createEmailVerficationToken(tempPasswordObj)
#             if insertedVerificationToken == {}:
#                 api.abort(500, 'Internal server error')
#
#             # send email with temp password
#             emailResponse = send_email('mightyhost0@gmail.com', email, 'New Password', tempPassword)
#             if emailResponse == {}:
#                 api.abort(500, 'Internal server error')
#         else:
#             api.abort(404, "Email not found")
#
#         return {"message": "Temporary password emailed"}
#
#
# reset_post = api.parser()
# reset_post.add_argument('temp_password', required=True)
# reset_post.add_argument('new_password', required=True)
#
#
# @api.route('/reset')
# class Reset(Resource):
#     @api.expect(reset_input)
#     @api.response(200, 'Password successfully sent')
#     @api.response(404, 'User not found')
#     def post(self):
#         '''Reset password'''
#         temp_password = reset_post.parse_args()['temp_password']
#         new_password = reset_post.parse_args()['new_password']
#         tempPasswordLookup = userModel.searchEmailVerificationToken(temp_password)
#         if tempPasswordLookup == {}:
#             api.abort(401, "Password not found")
#
#         hashedPassword = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt())
#
#         userData = userModel.getOne(tempPasswordLookup['user_id'])
#
#         if userData == {}:
#             api.abort(404, 'User Not found')
#
#         userData['password'] = hashedPassword
#
#         userId = ''
#         if '_id' in userData.keys():
#             userId = userData['_id']
#             del userData['_id']
#         else:
#             api.abort(500, 'Internal server error')
#
#         updatedUserData = userModel.updateOne(userId, userData)
#
#         if (updatedUserData == {}):
#             api.abort(404, 'User Not found')
#
#         return {'message': 'Password successfully reset'}
