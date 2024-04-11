from flask_restful import Resource, reqparse
from flask import jsonify
import pymysql
import traceback
from flask import request

parser = reqparse.RequestParser()
parser.add_argument('balance')
parser.add_argument('account_number')
parser.add_argument('user_id')

# parser.add_argument('deleted')

class Account(Resource):
    def db_init(self):
        # db = pymysql.connect('localhost', 'root', 'password', 'root')
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    def get(self, id, user_id):
        db, cursor = self.db_init()
        # sql = 'Select * From api.accounts Where id ='
        sql = f'Select * From api.accounts Where id = {id} and deleted is not True'
        cursor.execute(sql)
        db.commit()
        account = cursor.fetchone()
        db.close()
        return jsonify({'data': account})

    def patch(self, id, user_id):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        account = {
            'balance': arg['balance'],
            'account_number': arg['account_number'],
            'user_id': arg['user_id']
        }
        query = []
        for key, value in account.items():
            if value != None:
                query.append(f"{key} = '{value}'")

        query = ", ".join(query)
        # print(query)
        sql = f"UPDATE `api`.`accounts` SET {query} WHERE (`id` = '{id}');"
        print(sql)
        # "UPDATE `api`.`accounts` SET `name` = 'CoCo', `gender` = '1', `birth` = '1998-02-02', `note` = 'cc' WHERE (`id` = '2');"

        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'
        db.commit()
        db.close()
        return jsonify(response)

    def delete(self, id, user_id):
        db, cursor = self.db_init()
        # sql = f"DELETE FROM `api`.`accounts` WHERE (`id` = '{id}');"
        sql = f"UPDATE `api`.`accounts` SET deleted = True WHERE (`id` = '{id}');"
        # "DELETE FROM `api`.`accounts` WHERE (`id` = '4');"
        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'
        db.commit()
        db.close()
        return jsonify(response)


class Accounts(Resource):
    def db_init(self):
        # db = pymysql.connect('localhost', 'root', 'password', 'root')
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    def get(self, user_id):
        db, cursor = self.db_init()
        # arg = parser.parse_args()
        sql = 'SELECT * FROM api.accounts WHERE user_id = "{}" and deleted IS NOT TRUE'.format(user_id)

        cursor.execute(sql)
        db.commit()
        accounts = cursor.fetchall()
        db.close()
        return jsonify({'data': accounts})

    def post(self, user_id):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        account = {
            'balance': arg['balance'],
            'account_number': arg['account_number'],
            'user_id': arg['user_id']
        }
        sql = """
            INSERT INTO `api`.`accounts` (`balance`, `account_number`, `user_id`) VALUES ('{}', '{}', '{}');
        """.format(account['balance'], account['account_number'], account['user_id'])

        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'
        db.commit()
        db.close()
        return jsonify(response)
