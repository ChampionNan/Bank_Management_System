from flask import Flask, request, jsonify, make_response, Blueprint
from flask_cors import *
import json
import time
import pymysql

customer_api = Blueprint('customer_api', __name__)

@customer_api.route('/customer', methods=['POST'])
def customer():
    rstype = request.form['type']
    if rstype == 'Search':
        print('Search')
        db = pymysql.connect('127.0.0.1', 'root', 'Cbn111156789!', "Lab3", 3306)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

        nameSearch = request.form['nameSearch'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        idSearch = request.form['idSearch'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        telSearch = request.form['telSearch'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        addrSearch = request.form['addrSearch'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        linknameSearch = request.form['linknameSearch'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        linktelSearch = request.form['linktelSearch'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        emailSearch = request.form['emailSearch'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        sqlcommand = "SELECT CUSTOMER_ID AS id, CUSTOMER_NAME AS name, CUSTOMER_PHONE AS tel, CUSTOMER_ADDRESS AS addr, CUSTOMER_CONTACT_NAME AS name_link, CUSTOMER_CONTACT_PHONE AS tel_link, CUSTOMER_CONTACT_EMAIL AS email_link, CUSTOMER_CONTACT_RELATION AS relation FROM CUSTOMER WHERE CUSTOMER_ID IS NOT NULL"

        if len(nameSearch) > 0:
            sqlcommand = sqlcommand + " AND CUSTOMER_NAME LIKE '%" + nameSearch + "%'"
        if len(idSearch) > 0:
            sqlcommand = sqlcommand + " AND CUSTOMER_ID LIKE '%" + idSearch + "%'"
        if len(telSearch) > 0:
            sqlcommand = sqlcommand + " AND CUSTOMER_PHONE LIKE '%" + telSearch + "%'"
        if len(addrSearch) > 0:
            sqlcommand = sqlcommand + " AND CUSTOMER_ADDRESS LIKE '%" + addrSearch + "%'"
        if len(linknameSearch) > 0:
            sqlcommand = sqlcommand + " AND CUSTOMER_CONTACT_NAME LIKE '%" + linknameSearch + "%'"
        if len(linktelSearch) > 0:
            sqlcommand = sqlcommand + " AND CUSTOMER_CONTACT_PHONE LIKE '%" + linktelSearch + "%'"
        if len(emailSearch) > 0:
            sqlcommand = sqlcommand + " AND CUSTOMER_CONTACT_EMAIL LIKE '%" + emailSearch + "%'"
        print(sqlcommand)
        cursor.execute(sqlcommand)
        result = cursor.fetchall()
        print(result)
        response = make_response(jsonify({
            'code': 200,
            'list': result
        }))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response
    if rstype == 'Update':
        print('Update')
        db = pymysql.connect('127.0.0.1', 'root', 'Cbn111156789!', "Lab3", 3306)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

        id_s = request.form['id']
        name = request.form['name'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        tel = request.form['tel'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        addr = request.form['addr'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        name_link = request.form['name_link'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        tel_link = request.form['tel_link'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        email_link = request.form['email_link'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        relation = request.form['relation'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        old_primary = request.form['old_primary'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')

        sqlcommand = ""
        # 改
        if len(old_primary) > 0:
            if id_s != old_primary:
                args = [old_primary, id_s, 0]
                result_args = cursor.callproc('CHANGE_CUSTOMER_NAME', args)
                print(result_args[2])
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
            sqlcommand = sqlcommand + "UPDATE CUSTOMER SET"
            if len(name) > 0:
                sqlcommand = sqlcommand + " CUSTOMER_NAME = '" + name  + "',"
            if len(tel) > 0:
                sqlcommand = sqlcommand + " CUSTOMER_PHONE = '" + tel + "',"
            if len(addr):
                sqlcommand = sqlcommand + " CUSTOMER_ADDRESS = '" + addr + "',"
            if len(name_link):
                sqlcommand = sqlcommand + " CUSTOMER_CONTACT_NAME = '" + name_link + "',"
            if len(tel_link):
                sqlcommand = sqlcommand + " CUSTOMER_CONTACT_PHONE = '" + tel_link + "',"
            if len(email_link):
                sqlcommand = sqlcommand + " CUSTOMER_CONTACT_EMAIL = '" + email_link + "',"
            if len(relation):
                sqlcommand = sqlcommand + "CUSTOMER_CONTACT_RELATION = '" + relation + "',"

            sqlcommand = sqlcommand[:len(sqlcommand) - 1]
            sqlcommand = sqlcommand + " WHERE CUSTOMER_ID = '" + id_s + "'"

        # 增
        else:
            insert = "(" + "'" + id_s + "','" + name + "','" + tel + "','" + addr + "','" + name_link + "','" + tel_link + "','" + email_link + "','" + relation + "')"
            sqlcommand = sqlcommand + "INSERT INTO CUSTOMER(CUSTOMER_ID, CUSTOMER_NAME, CUSTOMER_PHONE, CUSTOMER_ADDRESS, CUSTOMER_CONTACT_NAME, CUSTOMER_CONTACT_PHONE, CUSTOMER_CONTACT_EMAIL, CUSTOMER_CONTACT_RELATION) VALUES" + insert

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
        print('Delete')
        db = pymysql.connect('127.0.0.1', 'root', 'Cbn111156789!', "Lab3", 3306)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

        primary = request.form['primary'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        sqlcommand = " SELECT * FROM EMPLOYEE_CUSTOMER WHERE " + " CUSTOMER_ID = '" + primary + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)
        result = cursor.fetchall()
        if len(result) > 0:
            cursor.close()
            db.close()
            response = make_response(jsonify({
                'code': 407,
                'msg': '有关联员工信息'
            }))
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response
        sqlcommand = " SELECT * FROM CUSTOMER_DEPOSIT_ACCOUNT WHERE " + " CUSTOMER_ID = '" + primary + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)
        result = cursor.fetchall()
        if len(result):
            cursor.close()
            db.close()
            response = make_response(jsonify({
                'code': 408,
                'msg': '有关联存储账户信息'
            }))
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response
        sqlcommand = " SELECT * FROM CUSTOMER_CHECK_ACCOUNT WHERE " + " CUSTOMER_ID = '" + primary  + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)
        result = cursor.fetchall()
        if len(result) > 0:
            cursor.close()
            db.close()
            response = make_response(jsonify({
                'code': 409,
                'msg': '有关联支票账户信息'
            }))
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response

        sqlcommand = " SELECT * FROM LOAN_CUSTOMER WHERE CUSTOMER_ID = '" + primary + "'"
        cursor.execute(sqlcommand)
        result = cursor.fetchall()
        if len(result) > 0:
            cursor.close()
            db.close()
            response = make_response(jsonify({
                'code': 410,
                'msg': '有关联贷款信息'
            }))
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response
        sqlcommand = " DELETE FROM CUSTOMER WHERE " + " CUSTOMER_ID = '" + primary + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)
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



