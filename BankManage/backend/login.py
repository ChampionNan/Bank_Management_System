from flask import Flask, request, jsonify, make_response
from flask_cors import *
import json
import time
import pymysql

from register import register_api
from bank import bank_api
from staff import staff_api
from summary import summary_api
from loan import loan_api
from customer import customer_api
from account import account_api

app = Flask(__name__)
app.register_blueprint(register_api)
app.register_blueprint(bank_api)
app.register_blueprint(staff_api)
app.register_blueprint(summary_api)
app.register_blueprint(loan_api)
app.register_blueprint(customer_api)
app.register_blueprint(account_api)

CORS(app, supports_credential = True)

def makeDictFactory(cursor):
    '''
    :param cursor: 游标
    :return: 字典化后的数据
    '''
    columnNames = [d[0].lower() for d in cursor.description]
    def createRow(*args):
        return dict(zip(columnNames, args))
    return createRow

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    custype = request.form['custype']
    print(username, password, custype)

    try:
        db = pymysql.connect(host = '127.0.0.1', user = 'root', password = 'Cbn111156789!',db = "Lab3" ,port = 3306)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        sqlcommand = ''
        if custype == 'SUB_BANK':
            sqlcommand = """
                        SELECT BANK_NAME AS username, BANK_PASS AS password FROM SUB_BANK WHERE BANK_NAME = '""" + username + "'"
        elif custype == 'EMPLOYEE':
            sqlcommand = """
                        SELECT EMPLOYEE_ID AS username, EMPLOYEE_PASS AS password FROM EMPLOYEE WHERE EMPLOYEE_ID = '""" + username + "'"
        else:
            sqlcommand = """
                        SELECT CUSTOMER_ID AS username, CUSTOMER_PASS AS password FROM CUSTOMER WHERE CUSTOMER_ID = '""" + username + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)
        result = cursor.fetchone()
        print(result)
        cursor.close()
        # db.close() finally中写
        # 登陆成功
        if result and len(password) > 0 and result['password'][:len(password)] == password:
            print("登陆成功")
            response = make_response(jsonify({
                'code': 200,
                'msg': 'get',
                'token': username
            }))
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS, HEAD, GET, POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response
        # 登陆失败
        response = make_response(jsonify({
            'code': 400,
            'msg': 'error'
        }))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS, HEAD, GET, POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response

    except pymysql.Error as e:
        print("数据库连接失败")
        print(pymysql.Error)
        response = make_response(jsonify({
            'code': 400,
            'msg': 'error'
        }))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS, HEAD, GET, POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response
    finally:
        # 连接成功关闭数据库
        if db:
            db.close()
if __name__ == '__main__':
    app.run(host='0.0.0.0')




