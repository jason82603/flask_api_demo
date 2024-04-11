from flask_restful import Resource, reqparse
from flask import jsonify, make_response
import pymysql
import traceback
from Flask_Practice.api_restful.resources.models import UserModel
from Flask_Practice.api_restful.resources.server import db

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')
# parser.add_argument('deleted')

class User(Resource):
    print('use User')
    def db_init(self):
        # db = pymysql.connect('localhost', 'root', 'password', 'root')
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    def get(self, id):
        db, cursor = self.db_init()
        # sql = 'Select * From api.users Where id ='
        sql = f'Select * From api.users Where id = {id} and deleted is not True'
        cursor.execute(sql)
        db.commit()
        user = cursor.fetchone()
        db.close()
        return jsonify({'data': user})

    def patch(self, id):
        # db, cursor = self.db_init()
        arg = parser.parse_args()
        # user = {
        #     'name': arg['name'],
        #     'gender': arg['gender'],
        #     'birth': arg['birth'],
        #     'note': arg['note']
        # }
        # query = []
        # for key, value in user.items():
        #     if value != None:
        #         query.append(f"{key} = '{value}'")
        #
        # query = ", ".join(query)
        # # print(query)
        # sql = f"UPDATE `api`.`users` SET {query} WHERE (`id` = '{id}');"
        # print(sql)

        # "UPDATE `api`.`users` SET `name` = 'CoCo', `gender` = '1', `birth` = '1998-02-02', `note` = 'cc' WHERE (`id` = '2');"

        user = UserModel.query.filter_by(id=id, deleted=None).first()
        # print(user)
        if arg['name'] != None:
            user.name = arg['name']
            # user.gender = arg['gender']
            # user.birth = arg['birth']
            # user.note = arg['note']

        response = {}
        try:
            # cursor.execute(sql)
            db.session.commit()
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'
        # db.commit()
        # db.close()

        return jsonify(response)

    def delete(self, id):
        db, cursor = self.db_init()
        # sql = f"DELETE FROM `api`.`users` WHERE (`id` = '{id}');"
        sql = f"UPDATE `api`.`users` SET deleted = True WHERE (`id` = '{id}');"
        # "DELETE FROM `api`.`users` WHERE (`id` = '4');"
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


class Users(Resource):
    def db_init(self):
        # db = pymysql.connect('localhost', 'root', 'password', 'root')
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    def get(self):
        # db, cursor = self.db_init()
        # # arg = parser.parse_args()
        # arg = request.args
        #
        # gender = arg.get('gender')
        # print(f'網址上輸入的gender: {gender}')
        # if gender is not None:
        #     sql = f'SELECT * FROM api.users WHERE gender = "{gender}" AND deleted IS NOT TRUE'
        # else:
        #     sql = 'SELECT * FROM api.users WHERE deleted IS NOT TRUE'

        # print(type(arg))
        # sql = 'Select * From api.users where deleted is not True'
        # print(arg)
        # print(arg['gender'])
        # if arg['gender'] != None:
        #     sql += ' and gender = "{}"'.format(arg['gender'])
        # traceback.print_exc()

        # cursor.execute(sql)
        # db.commit()
        # users = cursor.fetchall()
        # db.close()

        print('aaa')
        # users = UserModel.query.filter(UserModel.deleted.isnot(True)).all()
        # print('AAA')
        # return jsonify({'data': list(map(lambda user: user.serialize(), users))})

        try:
            users = UserModel.query.filter(UserModel.deleted.isnot(True)).all()
            return jsonify({'data': list(map(lambda user: user.serialize(), users))})
        except:
            traceback.print_exc()
            print('UserModel使用失敗')

    def post(self):
        # db, cursor = self.db_init()
        arg = parser.parse_args()
        user = {
            'name': arg['name'],
            'gender': arg['gender'] ,
            'birth': arg['birth'],
            'note': arg['note']
        }
        # sql = """
        #     INSERT INTO `api`.`users` (`name`, `gender`, `birth`, `note`) VALUES ('{}', '{}', '{}', '{}');
        # """.format(user['name'], user['gender'], user['birth'], user['note'])
        #
        response = {}
        status_code = 200
        try:
            new_user = UserModel(name = user['name'], gender = user['gender'], birth = user['birth'], note = user['note'])
            db.session.add(new_user)
            db.session.commit()
            # cursor.execute(sql)
            response['msg'] = 'success'
        except:
            status_code = 400
            traceback.print_exc()
            response['msg'] = 'failed'
        # db.commit()
        # db.close()
        return make_response(jsonify(response), status_code)
