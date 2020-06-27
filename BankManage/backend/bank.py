from flask import Flask, request, jsonify, make_response, Blueprint
from flask_cors import *
import json
import time
import pymysql

bank_api = Blueprint('bank_api', __name__)

@bank_api.route('/bank', methods=['POST'])
def bank():
    rstype = request.form['type']
    if rstype == 'Search':
        db = pymysql.connect('127.0.0.1', 'root', 'Cbn111156789!', "Lab3", 3306)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        bankSearch = request.form['bankSearch']
        citySearch = request.form['citySearch']
        lowerBound = request.form['lowerBound']
        upperBound = request.form['upperBound']
        sqlcommand = "SELECT" + " BANK_NAME AS name" + "," + "CITY as city" + "," + "POSSESSION AS money" + " FROM" + " SUB_BANK" + " WHERE" + " BANK_NAME IS NOT NULL"
        if len(bankSearch) > 0:
            sqlcommand = sqlcommand + " AND BANK_NAME LIKE '%" + bankSearch + "%'"
        if len(citySearch) > 0:
            sqlcommand = sqlcommand + " AND CITY LIKE '%" + citySearch + "%'"
        if len(lowerBound) > 0:
            sqlcommand = sqlcommand + " AND POSSESSION >" + lowerBound
        if len(upperBound) > 0:
            sqlcommand = sqlcommand + " AND POSSESSION <" + upperBound

        print(sqlcommand)
        cursor.execute(sqlcommand)
        result = cursor.fetchall()
        if result:
            response = make_response(jsonify({
                'code': 200,
                'list': result
            }))
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response
        response = make_response(jsonify({
            'code': 400
        }))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response
    if rstype == 'Update':
        db = pymysql.connect('127.0.0.1', 'root', 'Cbn111156789!', "Lab3", 3306)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

        name = request.form['name'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        city = request.form['city'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        money = request.form['money']
        old_primary = request.form['old_primary'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        sqlcommand = ""
        # 改
        if len(old_primary) > 0:
            if name != old_primary:
                args = [old_primary, name, 0]
                result_args = cursor.callproc('CHANGE_BANK_NAME', args)
                print(result_args[2], result_args[2].getvalue())
                if result_args[2] == 2:
                    cursor.close()
                    db.close()
                    response = make_response(jsonify({
                        'code': 402,
                        'msg': 'old name do not find'
                    }))
                    response.headers['Access-Control-Allow-Origin'] = '*'
                    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
                    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
                    return response
                if result_args[2] == 1:
                    cursor.close()
                    db.close()
                    response = make_response(jsonify({
                        'code': 401,
                        'msg': 'new name used'
                    }))
                    response.headers['Access-Control-Allow-Origin'] = '*'
                    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
                    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
                    return response
            sqlcommand = sqlcommand + " UPDATE SUB_BANK SET"
            if len(city) > 0:
                sqlcommand = sqlcommand + " CITY = '" + city + "',"
            if len(money) > 0:
                sqlcommand = sqlcommand + " POSSESSION = '" + money + "',"
            sqlcommand = sqlcommand[:len(sqlcommand) - 1]
            sqlcommand = sqlcommand + " WHERE BANK_NAME = '" + name + "'"
        # 增
        else:
            insert = "(" + "'" + name + "'" + "," + "'" + city + "','" + money + "')"
            sqlcommand = sqlcommand + "INSERT INTO SUB_BANK(BANK_NAME, CITY, POSSESSION) VALUES " + insert

        print(sqlcommand)
        try:
            cursor.execute(sqlcommand)
        except:
            cursor.close()
            db.close()
            response = make_response(jsonify({
                'code': 400,
                'msg': 'fail'
            }))
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response
        cursor.close()
        db.commit()
        db.close()
        response = make_response(jsonify({
            'code': 200,
            'msg': 'ok'
        }))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response
    if rstype == 'Delete':
        db = pymysql.connect('127.0.0.1', 'root', 'Cbn111156789!', "Lab3", 3306)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        primary = request.form['primary'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')

        sqlcommand = "SELECT * FROM EMPLOYEE WHERE " + "EMPLOYEE_BANK_NAME = '" + primary + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)
        result = cursor.fetchall()
        if len(result) > 0:
            cursor.close()
            db.close()
            response = make_response(jsonify({
                'code': 405,
                'msg': '有关联员工信息'
            }))
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response
        sqlcommand = "SELECT * FROM CUSTOMER_CHECK_ACCOUNT WHERE " + "BANK_NAME = '" + primary + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)
        result = cursor.fetchall()
        if len(result) > 0:
            cursor.close()
            db.close()
            response = make_response(jsonify({
                'code': 405,
                'msg': '有关联支票账户信息'
            }))
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response
        sqlcommand = "SELECT * FROM CUSTOMER_DEPOSIT_ACCOUNT WHERE " + "BANK_NAME = '" + primary + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)
        result = cursor.fetchall()
        if len(result) > 0:
            cursor.close()
            db.close()
            response = make_response(jsonify({
                'code': 406,
                'msg': '有关联存款账户信息'
            }))
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response
        sqlcommand = "DELETE FROM SUB_BANK WHERE " + "BANK_NAME = '" + primary + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)
        cursor.close()
        db.commit()
        db.close()
        response = make_response(jsonify({
            'code': 200,
            'msg': 'ok'
        })
        )
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response


