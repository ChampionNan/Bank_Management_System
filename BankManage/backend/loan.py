from flask import Flask, request, jsonify, make_response, Blueprint
from flask_cors import *
import json
import time
import pymysql

loan_api = Blueprint('loan_api', __name__)

@loan_api.route('/loan', methods=['POST'])
def loan():
    rstype = request.form['type']
    if rstype == 'Search':
        print('Search')

        db = pymysql.connect('127.0.0.1', 'root', 'Cbn111156789!', "Lab3", 3306)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

        idSearch = request.form['idSearch'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        bankSearch = request.form['bankSearch'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        statusSearch = request.form['statusSearch'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        custSearch = request.form['custSearch'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        upperBound = request.form['upperBound'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        lowerBound = request.form['lowerBound'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        sqlcommand = " SELECT LOAN.LOAN_ID AS id" + "," + " CUSTOMER.CUSTOMER_NAME AS customer" + "," + " LOAN.LOAN_MONEY AS amount" + "," + "LOAN.STATUS AS status" + "," + "LOAN.BANK_NAME AS bank" + " FROM LOAN, CUSTOMER, LOAN_CUSTOMER" + " WHERE" + " LOAN_CUSTOMER.CUSTOMER_ID = CUSTOMER.CUSTOMER_ID " + " AND LOAN_CUSTOMER.LOAN_ID = LOAN.LOAN_ID"

        statusdict = {
            "none": "0",
            "part": "1",
            "all": "2"
        }
        if len(statusSearch) > 0 and statusSearch != "any":
            sqlcommand = sqlcommand + " AND LOAN.STATUS = " + statusdict[statusSearch]
        if len(idSearch) > 0:
            sqlcommand = sqlcommand + " AND LOAN.LOAN_ID LIKE '%" + idSearch + "%'"
        if len(bankSearch) > 0:
            sqlcommand = sqlcommand + " AND LOAN.BANK_NAME LIKE '%" + bankSearch + "%'"
        if len(custSearch) > 0:
            sqlcommand = sqlcommand + " AND CUSTOMER.CUSRTOMER_NAME LIKE '%" + custSearch + "%'"
        if len(upperBound) > 0:
            sqlcommand = sqlcommand + " AND LOAN.LOAN_MONEY < " + upperBound
        if len(lowerBound) > 0:
            sqlcommand = sqlcommand + " AND LOAN.LOAN_MONEY > " + lowerBound

        print(sqlcommand)
        cursor.execute(sqlcommand)
        result = cursor.fetchall()
        for line in result:
            line['id'] = str(line['id'])
        print(result)
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
        print('Update')
        db = pymysql.connect('127.0.0.1', 'root', 'Cbn111156789!', "Lab3", 3306)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        print('ok')
        id_s = request.form['id'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        print('ok11')
        bank = request.form['bank'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        print('ok12')
        amount = request.form['amount'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        print('ok13')
        status = request.form['status'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        print('ok14')
        old_primary = request.form['old_primary'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        print('ok15')
        # customer = []
        customer = request.form['customer'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        # customer = request.form['customer']
        print('ok16')
        customer = customer.split(',')
        print('ok2')
        sqlcommand = ""
        insert = "('" + id_s + "','" + bank + "'," + amount + "," + status + ")"
        sqlcommand = sqlcommand + "INSERT LOAN(LOAN_ID, BANK_NAME, LOAN_MONEY, STATUS) VALUES" + insert
        print(sqlcommand)

        try:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            cursor.execute(sqlcommand)
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
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
        print(customer)
        print('part-ok1')
        for cus in customer:
            sqlcommand = ""
            insert = "('" + cus + "','" + id_s + "')"
            sqlcommand = sqlcommand + "INSERT INTO LOAN_CUSTOMER (CUSTOMER_ID, LOAN_ID) VALUES" + insert
            print(sqlcommand)
            try:
                cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
                cursor.execute(sqlcommand)
                cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
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
        sqlcommand = " SELECT * FROM LOAN WHERE LOAN.LOAN_ID = '" + primary + "'" + " AND LOAN.STATUS = 1"
        print(sqlcommand)
        cursor.execute(sqlcommand)
        result = cursor.fetchall()

        if len(result) > 0:
            cursor.close()
            db.close()
            response = make_response(jsonify({
                'code': 417,
                'msg': '贷款正在发放，无法删除'
            }))
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response

        cursor.execute('SET FOREIGN_KEY_CHECKS=0;')
        # sqlcommand = "ALTER TABLE LOAN_CUSTOMER"
        # cursor.execute(sqlcommand)
        # sqlcommand = "ALTER TABLE LOAN_CUSTOMER"
        # cursor.execute(sqlcommand)

        sqlcommand = "DELETE FROM LOAN_CUSTOMER WHERE " + "LOAN_ID = '" + primary + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)
        sqlcommand = "DELETE FROM LOAN WHERE " + "LOAN_ID = '" + primary + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand) 

        sqlcommand = "DELETE FROM PAY WHERE LOAN_ID = '" + primary + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)

        cursor.execute('SET FOREIGN_KEY_CHECKS=1;')
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

@loan_api.route('/pay', methods=['POST'])
def pay():
    rstype = request.form['type']
    if rstype == 'Search':
        print('Search')
        db = pymysql.connect('127.0.0.1', 'root', 'Cbn111156789!', "Lab3", 3306)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        loanid = request.form['loanid'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        sqlcommand = " SELECT " + "PAY_DATE AS date_s" + "," + " PAY_MONEY AS money " + " FROM PAY" + " WHERE LOAN_ID = '" + loanid + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)
        result = cursor.fetchall()
        for line in result:
            line['date_s'] = line['date_s'].strftime('%Y-%m-%d')
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
            'code': 400,
            'list': []
        }))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response
    if rstype == 'Insert':
        print('Insert')
        db = pymysql.connect('127.0.0.1', 'root', 'Cbn111156789!', "Lab3", 3306)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

        loanid = request.form['loanid'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        date = request.form['date'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        money = request.form['money'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')

        sqlcommand = "SELECT STATUS AS status, LOAN_MONEY AS money FROM LOAN WHERE LOAN_ID = '" + loanid + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)
        result = cursor.fetchone()

        if result:
            loanlimit = result['money']
            if result['status'] == 2:
                response = make_response(jsonify({
                    'code': 422,
                    'msg': '贷款已全部发放'
                }))
                response.headers['Access-Control-Allow-Origin'] = '*'
                response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
                response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
                return response
            else:
                sqlcommand = "SELECT LOAN_ID, SUM(PAY_MONEY) AS alreadypay FROM (" + " SELECT * FROM PAY WHERE LOAN_ID = '" + loanid + "'" + ")PAY_THIS GROUP BY LOAN_ID"
                print(sqlcommand)
                cursor.execute(sqlcommand)
                result = cursor.fetchone()
                alreadypay = 0
                if result:
                    alreadypay = result['alreadypay']
                    print(loanlimit, alreadypay, money)

                if float(loanlimit) < float(alreadypay) + float(money):
                    response = make_response(jsonify({
                        'code': 423,
                        'msg': '超过贷款额度'
                    }))
                    response.headers['Access-Control-Allow-Origin'] = '*'
                    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
                    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
                    return response
                if float(loanlimit) == float(alreadypay) + float(money):
                    sqlcommand = "UPDATE LOAN SET STATUS = 2 WHERE LOAN_ID = '" + loanid + "'"
                    print(sqlcommand)
                    cursor.execute(sqlcommand)
                else:
                    sqlcommand = "UPDATE LOAN SET STATUS = 1 WHERE LOAN_ID = '" + loanid + "'"
                    print(sqlcommand)
                    cursor.execute(sqlcommand)

                sqlcommand = ""
                insert = "('" + loanid + "'," + "STR_TO_DATE('" + date + "','%Y-%m-%d')" + "," + str(money) + ")"
                sqlcommand = sqlcommand + "INSERT INTO PAY(LOAN_ID, PAY_DATE, PAY_MONEY) VALUES" + insert
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
        response = make_response(jsonify({
            'code': 400
        }))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response






