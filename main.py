from flask import request, jsonify
from flask_restful import Api
from resources.user import Users, User
import resources.test1
from resources.account import Accounts, Account
import pymysql
import traceback
from Flask_Practice.api_restful.resources.server import app


api = Api(app)

api.add_resource(Users,'/users')
api.add_resource(User,'/user/<id>')
api.add_resource(Accounts,'/user/<user_id>/accounts')
api.add_resource(Account,'/user/<user_id>/account/<id>')

@app.errorhandler(Exception)
def handle_error(error):
    status_code = 500
    if type(error).__name__ =="NotFound":
        status_code = 404
    elif type(error).__name__ =="TypeError":
        status_code = 500
    return jsonify({'msg': type(error).__name__}), status_code

# @app.before_request
# def auth():
#     token = request.headers.get('auth')
#     # user_id = request.get_json()['user_id']
#     valid_token = jwt.encode({'timestamp': int(time.time())}, 'password', algorithm = 'HS256')
#     # valid_token = jwt.encode({'user_id': user_id, 'timestamp': int(time.time())}, 'password', algorithm='HS256')
#     print(token)
#     print(valid_token)
#     if token == valid_token:
#         pass
#     else:
#         return {
#             'msg': 'invalid token'
#         }

@app.route("/")
def index():
    return "hello world"

@app.route("/user/<user_id>/account/<id>/deposit", methods = ['POST'])
def deposit(user_id, id):
    db, cursor, account = get_account(id)
    print(account)
    response = {}

    try:
        money = request.get_json()['money']
        balance = account['balance'] + int(money)
        sql = 'Update api.accounts Set balance= {} Where id = {} and deleted is not True'.format(balance, id)

        cursor.execute(sql)
        response['msg'] = 'deposit success'
    except:
        traceback.print_exc()
        response['msg'] = 'deposit failed'
    db.commit()
    db.close()
    return jsonify(response)


@app.route("/user/<user_id>/account/<id>/withdraw", methods = ['POST'])

def withdraw(user_id, id):
    db, cursor, account = get_account(id)
    print(account)
    response = {}

    try:
        money = request.get_json()['money']
        balance = account['balance'] - int(money)
        sql = 'Update api.accounts Set balance= {} Where id = {} and deleted is not True'.format(balance, id)


        if balance < 0:
            response['msg'] = 'money not enough'
            return jsonify(response)

        else:
            cursor.execute(sql)
            response['msg'] = 'withdraw success'
    except:
        traceback.print_exc()
        response['msg'] = 'withdraw failed'

    db.commit()
    db.close()
    return jsonify(response)
def get_account(id):
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='root',
                         database='api')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = f'Select * From api.accounts Where id = {id} and deleted is not True'
    cursor.execute(sql)
    return db, cursor, cursor.fetchone()

if __name__ == '__main__':
    app.debug = True
    app.run()
    # app.run(host='0.0.0.0', port=5000)