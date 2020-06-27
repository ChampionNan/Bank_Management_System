from flask import Flask, request, jsonify, make_response, Blueprint
from flask_cors import *
import json
import time
import pymysql

register_api = Blueprint('register_api', __name__)

@register_api.route('/register', methods=['POST', 'OPTIONS'])
def register():
    username = request.form['username'].rstrip().replace('\'', '').replace('\"', '').replace('%', '').replace('#','').replace(',', '').replace(')', '').replace('(', '').replace('}', '').replace('[', '').replace(']', '').replace('{', '')
    password = request.form['password'].rstrip().replace('\'', '').replace('\"', '').replace('%', '').replace('#','').replace(',', '').replace(')', '').replace('(', '').replace('}', '').replace('[', '').replace(']', '').replace('{', '')
    account_type = request.form['type'].rstrip().replace('\'', '').replace('\"', '').replace('%', '').replace('#','').replace(',', '').replace(')', '').replace('(', '').replace('}', '').replace('[', '').replace(']', '').replace('{', '')
    city = request.form['city'].rstrip().replace('\'', '').replace('\"', '').replace('%', '').replace('#','').replace(',', '').replace(')', '').replace('(', '').replace('}', '').replace('[', '').replace(']', '').replace('{', '')
    money = request.formp['money'].rstrip().replace('\'', '').replace('\"', '').replace('%', '').replace('#','').replace(',', '').replace(')', '').replace('(', '').replace('}', '').replace('[', '').replace(']', '').replace('{', '')
    name = request.form['name'].rstrip().replace('\'', '').replace('\"', '').replace('%', '').replace('#','').replace(',', '').replace(')', '').replace('(', '').replace('}', '').replace('[', '').replace(']', '').replace('{', '')
    tel = request.form['tel'].rstrip().replace('\'', '').replace('\"', '').replace('%', '').replace('#','').replace(',', '').replace(')', '').replace('(', '').replace('}', '').replace('[', '').replace(']', '').replace('{', '')
    addr = request.form['addr'].rstrip().replace('\'', '').replace('\"', '').replace('%', '').replace('#','').replace(',', '').replace(')', '').replace('(', '').replace('}', '').replace('[', '').replace(']', '').replace('{', '')
    name_link = request.form['name_link'].rstrip().replace('\'', '').replace('\"', '').replace('%', '').replace('#','').replace(',', '').replace(')', '').replace('(', '').replace('}', '').replace('[', '').replace(']', '').replace('{', '')
    tel_link = request.form['tel_link'].rstrip().replace('\'', '').replace('\"', '').replace('%', '').replace('#','').replace(',', '').replace(')', '').replace('(', '').replace('}', '').replace('[', '').replace(']', '').replace('{', '')
    email_link = request.form['email_link'].rstrip().replace('\'', '').replace('\"', '').replace('%', '').replace('#','').replace(',', '').replace(')', '').replace('(', '').replace('}', '').replace('[', '').replace(']', '').replace('{', '')
    relation = request.form['relation'].rstrip().replace('\'', '').replace('\"', '').replace('%', '').replace('#','').replace(',', '').replace(')', '').replace('(', '').replace('}', '').replace('[', '').replace(']', '').replace('{', '')
    dept = request.form['dept'].rstrip().replace('\'', '').replace('\"', '').replace('%', '').replace('#','').replace(',', '').replace(')', '').replace('(', '').replace('}', '').replace('[', '').replace(']', '').replace('{', '')
    date_s = request.form['date_s'].rstrip().replace('\'', '').replace('\"', '').replace('%', '').replace('#','').replace(',', '').replace(')', '').replace('(', '').replace('}', '').replace('[', '').replace(']', '').replace('{', '')
    bankname = request.form['bank_name'].rstrip().replace('\'', '').replace('\"', '').replace('%', '').replace('#','').replace(',', '').replace(')', '').replace('(', '').replace('}', '').replace('[', '').replace(']', '').replace('{', '')
    try:
        db = pymysql.connect('127.0.0.1', 'root', 'Cbn111156789!',"Lab3" , 3306)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        sqlcommand = ""
        if account_type == 'SUB_BANK':
            insert = "(" + "'" + username + "'" + "," + "'" + password + "'," + "'" + city + "'," + "'" + money + "'" + ")"
            sqlcommand = """
                        INSERT INTO SUB_BANK(BANK_NAME, BANK_PASS, CITY, POSSESSION)
                        VALUES""" + insert
        elif account_type == "EMPLOYEE":
            insert = "(" + "'" + username + "'" + "," + "'" + password + "'," + "'" + name + "'," + "'" + dept + "'," + "'" + tel + "'," + "'" + addr + "'," + "'" + bankname + "'," + "STR_TO_DATE('" + date_s + "','%Y-%m-%d')" + ")"
            sqlcommand = """
                        INSERT INTO EMPLOYEE(EMPLOYEE_ID, EMPLOYEE_PASS, EMPLOYEE_NAME, EMPLOYEE_DEPART_ID, EMPLOYEE_PHONE, EMPLOYEE_ADDRESS, EMPLOYEE_BANK_NAME, EMPLOYEE_ENTERDATE) VALUES""" + insert
        else:
            insert = "(" + "'" + username + "'" + "," + "'" + password + "'," + "'" + name + "'," + "'" + tel + "'," + "'" + addr + "'," + "'" + name_link + "'," + "'" + tel_link + "'," + "'" + email_link + "'," + "'" + relation + "'" + ")"
            sqlcommand = """
                        INSERT INTO CUSTOMER(CUSTOMER_ID, CUSTOMER_PASS, CUSTOMER_NAME, CUSTOMER_PHONE, CUSTOMER_ADDRESS, CUSTOMER_CONTACT_NAME, CUSTOMER_CONTACT_PHONE, CUSTOMER_CONTACT_EMAIL, CUSTOMER_CONTACT_RELATION) VALUES""" + insert
        print(sqlcommand)
        cursor.execute(sqlcommand)
        cursor.close()
        db.commit()
        response = make_response(jsonify({
            'code': 200,
            'msg': 'ok'
        }))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    except pymysql.Error as e:
        print("数据库连接失败")
        cursor.close()
        response = make_response(jsonify({
            'code': 400,
            'msg': 'ok'
        }))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response
    finally:
        # 连接成功关闭数据库
        if db:
            db.close()