from flask import Flask, request, jsonify, make_response, Blueprint
from flask_cors import *
import json
import time
import pymysql

account_api = Blueprint('account_api', __name__)

@account_api.route('/account', methods=['POST'])
def account():
    rstype = request.form['type']
    if rstype == 'Search':
        print('Search')
        db = pymysql.connect('127.0.0.1', 'root', 'Cbn111156789!', "Lab3", 3306)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        # 请求数据处理
        bankSearch = request.form['bankSearch'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        idSearch = request.form['idSearch'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        ownerSearch = request.form['ownerSearch'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        typeSearch = request.form['typeSearch'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        money_lo = request.form['money_lo'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        money_up = request.form['money_up'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        open_lo = request.form['open_lo'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        open_up = request.form['open_up'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        visit_lo = request.form['visit_lo'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        visit_up = request.form['visit_up'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')

        checkresult = []
        depositresult = []

        if typeSearch == 'any' or typeSearch == 'check':
            sqlcommand = ""
            sqlcommand = sqlcommand + " SELECT" + " CHECK_ACCOUNT.CHECK_ACCOUNT_ID AS id" + "," + " CUSTOMER_CHECK_ACCOUNT.BANK_NAME AS bank" + "," + " CHECK_ACCOUNT.CHECK_ACCOUNT_MONEY AS money" + "," + " CHECK_ACCOUNT.CHECK_ACCOUNT_REGDATE AS open_date" + "," + " CHECK_ACCOUNT.CHECK_ACCOUNT_OVERDRAFT AS overdraft" + " FROM" + " CHECK_ACCOUNT" + "," + " CUSTOMER" +","+ " CUSTOMER_CHECK_ACCOUNT" + " WHERE" + " CHECK_ACCOUNT.CHECK_ACCOUNT_ID = CUSTOMER_CHECK_ACCOUNT.CHECK_ACCOUNT_ID" + " AND CUSTOMER.CUSTOMER_ID = CUSTOMER_CHECK_ACCOUNT.CUSTOMER_ID"
            if len(bankSearch) > 0:
                sqlcommand = sqlcommand + " AND CUSTOMER_CHECK_ACCOUNT.BANK_NAME LIKE '%" + bankSearch + "%'"
            if len(idSearch) > 0:
                sqlcommand = sqlcommand + " AND CHECK_ACCOUNT.CHECK_ACCOUNT_ID LIKE '%" + idSearch + "%'"
            if len(ownerSearch) > 0:
                sqlcommand = sqlcommand + " AND CUSRTOMER.CUSTOMER_NAME LIKE '%" + ownerSearch + "%'"
            if len(money_lo) > 0:
                sqlcommand = sqlcommand + " AND CHECK_ACCOUNT.CHECK_ACCOUNT_MONEY > " + money_lo
            if len(money_up) > 0:
                sqlcommand = sqlcommand + " AND CHECK_ACCOUNT.CHECK_ACCOUNT_MONEY < " + money_up
            if len(open_lo) > 0:
                sqlcommand = sqlcommand + " AND CHECK_ACCOUNT.CHECK_ACCOUNT_REGDATE > STR_TO_DATE('" + open_lo + "','%Y-%m-%d')"
            if len(open_up) > 0:
                sqlcommand = sqlcommand + " AND CHECK_ACCOUNT.CHECK_ACCOUNT_REGDATE < STR_TO_DATE('" + open_up + "','%Y-%m-%d')"

            print(sqlcommand)
            cursor.execute(sqlcommand)
            checkresult = cursor.fetchall()
            print(checkresult)
            for line in checkresult:
                line['type'] = "1"
                line['open_date'] = line['open_date'].strftime('%Y-%m-%d')

        if typeSearch == "any" or typeSearch == "saving":
            sqlcommand = ""
            sqlcommand = sqlcommand + " SELECT" + " DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_ID AS id" + "," + " CUSTOMER_DEPOSIT_ACCOUNT.BANK_NAME AS bank" + "," + "DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_MONEY as money" + "," + " DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_REGDATE AS open_date" + "," + " DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_INTERESTRATE AS interest" + "," + " DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_CURRENCYTYPE AS cashtype" + " FROM"
            sqlcommand = sqlcommand + " DEPOSIT_ACCOUNT" + "," + " CUSTOMER" + "," + " CUSTOMER_DEPOSIT_ACCOUNT" + " WHERE" + " DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_ID = CUSTOMER_DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_ID" + " AND CUSTOMER.CUSTOMER_ID = CUSTOMER_DEPOSIT_ACCOUNT.CUSTOMER_ID"
            # print('Begin:',sqlcommand)
            if len(bankSearch) > 0:
                sqlcommand = sqlcommand + " AND CUSTOMER_DEPOSIT_ACCOUNT.BANK_NAME LIKE '%" + bankSearch + "%'"
            if len(idSearch) > 0:
                sqlcommand = sqlcommand + " AND DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_ID LIKE '%" + idSearch + "%'"
            if len(ownerSearch) > 0:
                sqlcommand = sqlcommand + " AND CUSTOMER.CUSTOMER_NAME LIKE '%" + ownerSearch + "%'"
            if len(money_lo) > 0:
                sqlcommand = sqlcommand + " AND DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_MONEY > " + money_lo
            if len(money_up) > 0:
                sqlcommand = sqlcommand + " AND DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_MONEY < " + money_up
            if len(open_lo) > 0:
                sqlcommand = sqlcommand + " AND DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_REGFATE > STR_TO_DATE('" + open_lo + "','%Y-%m-%d')"
            if len(open_up) > 0:
                sqlcommand = sqlcommand + " AND DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_REGDATE < STR_TO_DATE('" + open_up + "','%Y-%m-%d')"

            print(sqlcommand)
            cursor.execute(sqlcommand)
            depositresult = cursor.fetchall()
            print(checkresult)
            for line in depositresult:
                line['type'] = 0
                line['cashtype'] = str(line['cashtype'])
                line['open_date'] = line['open_date'].strftime('%Y-%m-%d')
        print(checkresult)
        print(depositresult)
        # result = list(set(list(checkresult) + list(depositresult)))
        result = list(checkresult) + list(depositresult)
        result = [dict(t) for t in set([tuple(d.items()) for d in result])]
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
        #实现数据库操作，返回查询结果
        print('Update')
        db = pymysql.connect('127.0.0.1', 'root', 'Cbn111156789!',"Lab3" , 3306)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        # 请求数据处理
        id_s = request.form['id'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        money = request.form['money'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        acctype = request.form['acctype'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        interest = request.form['interest'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        overdraft = request.form['overdraft'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        old_primary = request.form['old_primary'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        open_date = request.form['open_date'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        cashtype = request.form['cashtype'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        bank = request.form['bank'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        ownerid = request.form['ownerid'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        sqlcommand = ""
        # 改
        if len(old_primary) > 0:
            print('Change')
            if acctype == "0":
                sqlcommand = sqlcommand + "UPDATE DEPOSIT_ACCOUNT SET"
                if len(money) > 0:
                    sqlcommand = sqlcommand + " DEPOSIT_ACCOUNT_MONEY = '" + money + "',"
                if len(interest) > 0:
                    sqlcommand = sqlcommand + " DEPOSIT_ACCOUNT_INTERESTRATE = '" + interest + "',"
                sqlcommand = sqlcommand[:len(sqlcommand) - 1]
                sqlcommand = sqlcommand + " WHERE DEPOSIT_ACCOUNT_ID = '" + id_s + "'"
            else:
                sqlcommand = sqlcommand + " UPDATE CHECK_ACCOUNT SET"
                if len(money) > 0:
                    sqlcommand = sqlcommand + " CHECK_ACCOUNT_MONEY = '" + money + "',"
                if len(overdraft) > 0:
                    sqlcommand = sqlcommand + " CHECK_ACCOUNT_OVERDRAFT = '" + overdraft + "',"
                sqlcommand = sqlcommand[:len(sqlcommand) - 1]
                sqlcommand = sqlcommand + " WHERE CHECK_ACCOUNT_ID = '" + id_s + "'"
        # 增
        else:
            print('Insert')
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            if acctype == "0":
                insert = "(" + "'" + id_s + "'" + "," + "'" + money + "'" + "," + "STR_TO_DATE('" + open_date + "','%Y-%m-%d')" + "," + "'" + interest + "'" + "," + "'" + cashtype + "'" + ")"
                sqlcommand = sqlcommand + "INSERT INTO DEPOSIT_ACCOUNT(DEPOSIT_ACCOUNT_ID, DEPOSIT_ACCOUNT_MONEY, DEPOSIT_ACCOUNT_REGDATE, DEPOSIT_ACCOUNT_INTERESTRATE, DEPOSIT_ACCOUNT_CURRENCYTYPE) VALUES" + insert
                print(sqlcommand)
                cursor.execute(sqlcommand)
                sqlcommand = ""
                insert = "(" + "'" + bank + "'" + "," + "'" + ownerid + "'" + "," + "'" + id_s + "'" + "," + "STR_TO_DATE('" + open_date + "','%Y-%m-%d')" + ")"
                sqlcommand = sqlcommand + " INSERT INTO CUSTOMER_DEPOSIT_ACCOUNT(BANK_NAME, CUSTOMER_ID, DEPOSIT_ACCOUNT_ID, LAST_VIEW) VALUES" + insert

            else:
                insert = "(" + "'" + id_s + "'" + "," + "'" + money + "'" + "," + "STR_TO_DATE('" + open_date + "','%Y-%m-%d')" + "," + "'" + overdraft + "'" + ")"
                sqlcommand = sqlcommand + "INSERT INTO CHECK_ACCOUNT(CHECK_ACCOUNT_ID, CHECK_ACCOUNT_MONEY, CHECK_ACCOUNT_REGDATE, CHECK_ACCOUNT_OVERDRAFT) VALUES" + insert
                print(sqlcommand)
                cursor.execute(sqlcommand)
                sqlcommand = ""
                insert = "(" + "'" + bank + "'" + "," + "'" + ownerid + "'" + "," + "'" + id_s + "'" + "," + "STR_TO_DATE('" + open_date + "','%Y-%m-%d')" + ")"
                sqlcommand = sqlcommand + "INSERT INTO CUSTOMER_CHECK_ACCOUNT(BANK_NAME, CUSTOMER_ID, CHECK_ACCOUNT_ID, LAST_VIEW) VALUES" + insert
            
            print(sqlcommand)
        try:
            cursor.execute(sqlcommand)
            cursor.execute('SET FOREIGN_KEY_CHECKS=1;')
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
        db = pymysql.connect('127.0.0.1', 'root', 'Cbn111156789!',"Lab3", 3306)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

        primary = request.form['primary'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        acctype = request.form['acctype'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')

        cursor.execute("SET FOREIGN_KEY_CHECKS=0;")

        if acctype == "0":
            sqlcommand = " SELECT * FROM DEPOSIT_ACCOUNT WHERE" + " DEPOSIT_ACCOUNT_ID = '" + primary + "'" + " AND DEPOSIT_ACCOUNT_MONEY > 0"
            print(sqlcommand)
            cursor.execute(sqlcommand)
            result = cursor.fetchall()
            if len(result) > 0:
                cursor.close()
                db.close()
                response = make_response(jsonify({
                    'code': 413,
                    'msg': '尚有余额不能删除'
                }))
                response.headers['Access-Control-Allow-Origin'] = '*'
                response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
                response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
                return response
            sqlcommand = " DELETE FROM CUSTOMER_DEPOSIT_ACCOUNT WHERE " + " DEPOSIT_ACCOUNT_ID = '" + primary + "'"
            print(sqlcommand)
            cursor.execute(sqlcommand)

            sqlcommand = " DELETE FROM DEPOSIT_ACCOUNT WHERE " + "DEPOSIT_ACCOUNT_ID = '" + primary + "'"
            print(sqlcommand)
            cursor.execute(sqlcommand)
            cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
            cursor.close()
            db.commit()
            db.close()
        else:
            sqlcommand = "SELECT * FROM CHECK_ACCOUNT WHERE " + "CHECK_ACCOUNT_ID = '" + primary + "'" + " AND CHECK_ACCOUNT_MONEY > 0"
            print(sqlcommand)
            cursor.execute(sqlcommand)
            result = cursor.fetchall()
            if len(result) > 0:
                cursor.close()
                db.close()
                response = make_response(jsonify({
                    'code': 413,
                    'msg': '尚有余额不能删除'
                }))
                response.headers['Access-Control-Allow-Origin'] = '*'
                response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
                response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
                return response
            sqlcommand = "DELETE FROM CUSTOMER_CHECK_ACCOUNT WHERE " + "CHECK_ACCOUNT_ID = '" + primary + "'"
            print(sqlcommand)
            cursor.execute(sqlcommand)

            sqlcommand = "DELETE FROM CHECK_ACCOUNT WHERE" + " CHECK_ACCOUNT_ID = '" + primary + "'"
            print(sqlcommand)
            cursor.execute(sqlcommand)
            cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
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

@account_api.route('/accountCustomer', methods=['POST'])
def accountCustomer():
    rstype = request.form['type']
    print(rstype)
    if rstype == 'Search':
        print('Search')
        db = pymysql.connect('127.0.0.1', 'root', 'Cbn111156789!',"Lab3", 3306)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

        accid = request.form['accid'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        bank = request.form['bank'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        acctype = request.form['acctype'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        sqlcommand = ""
        if acctype == "0":
            sqlcommand = "SELECT CUSTOMER_DEPOSIT_ACCOUNT.LAST_VIEW AS visit_date" + "," + " CUSTOMER.CUSTOMER_NAME AS ownername" + "," + " CUSTOMER_DEPOSIT_ACCOUNT.CUSTOMER_ID AS ownerid" + " FROM" + " CUSTOMER_DEPOSIT_ACCOUNT," + " CUSTOMER" + " WHERE" + " CUSTOMER.CUSTOMER_ID = CUSTOMER_DEPOSIT_ACCOUNT.CUSTOMER_ID" + " AND CUSTOMER_DEPOSIT_ACCOUNT.BANK_NAME = '" + bank + "'" + " AND CUSTOMER_DEPOSIT_ACCOUNT.DEPOSIT_ACCOUNT_ID = '" + accid + "'"
        else:
            sqlcommand = "SELECT CUSTOMER_CHECK_ACCOUNT.LAST_VIEW AS visit_date" + "," + " CUSTOMER.CUSTOMER_NAME AS ownername" + "," + " CUSTOMER_CHECK_ACCOUNT.CUSTOMER_ID AS ownerid" + " FROM" + " CUSTOMER_CHECK_ACCOUNT," + " CUSTOMER" + " WHERE" + " CUSTOMER.CUSTOMER_ID = CUSTOMER_CHECK_ACCOUNT.CUSTOMER_ID" + " AND CUSTOMER_CHECK_ACCOUNT.BANK_NAME = '" + bank + "'" + " AND CUSTOMER_CHECK_ACCOUNT.CHECK_ACCOUNT_ID = '" + accid + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)
        result = cursor.fetchall()
        for line in result:
            line['visit_date'] = line['visit_date'].strftime('%Y-%m-%d')
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

    if rstype == 'Insert':
        print('Insert')
        db = pymysql.connect('127.0.0.1', 'root', 'Cbn111156789!', "Lab3", 3306)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

        accid = request.form['accid'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
        bank = request.form['bank'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
        ownerid = request.form['ownerid'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
        visit_date = request.form['visit_date'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
        acctype = request.form['acctype'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')  
        sqlcommand = ""
        
        if acctype == "0":
            insert = "(" + "'" + bank + "'" + "," + "'" + ownerid + "'" + "," + "'" + accid + "'" + "," + "STR_TO_DATE('" + visit_date + "','%Y-%m-%d')" + ")"
            sqlcommand = sqlcommand + "INSERT INTO CUSTOMER_DEPOSIT_ACCOUNT(BANK_NAME, CUSTOMER_ID, DEPOSIT_ACCOUNT_ID, LAST_VIEW) VALUES" + insert
        else:
            insert = "(" + "'" + bank + "'" + "," + "'" + ownerid + "'" + "," + "'" + accid + "'" + "," + "STR_TO_DATE('" + visit_date + "','%Y-%m-%d')" + ")"
            sqlcommand = sqlcommand + "INSERT INTO CUSTOMER_CHECK_ACCOUNT(BANK_NAME, CUSTOMER_ID, CHECK_ACCOUNT_ID, LAST_VIEW) VALUES" + insert
        print(sqlcommand)
        try:
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            cursor.execute(sqlcommand)
            cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
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
        sqlcommand = " SELECT" + " CUSTOMER_NAME AS ownername" + " FROM" + " CUSTOMER" + " WHERE" + " CUSTOMER_ID = '" + ownerid + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)
        result = cursor.fetchone()
        result['id'] = accid
        result['bank'] = bank
        result['ownerid'] = ownerid

        cursor.close()
        db.commit()
        db.close()
        response = make_response(jsonify({
            'code': 200,
            'record': result
        })
        )
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response
    if rstype == 'Delete':
        print('Delete')
        db = pymysql.connect('127.0.0.1', 'root', 'Cbn111156789!', "Lab3", 3306)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

        accid = request.form['accid'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        bank = request.form['bank'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        ownerid = request.form['ownerid'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        acctype = request.form['acctype'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')

        if acctype == "0":
            sqlcommand = "DELETE FROM CUSTOMER_DEPOSIT_ACCOUNT WHERE DEPOSIT_ACCOUNT_ID = '" + accid + "'" + " AND CUSTOMER_ID = '" + ownerid + "'" + " AND BANK_NAME = '" + bank + "'"
            print(sqlcommand)
            cursor.execute(sqlcommand)
        else:
            sqlcommand = "DELETE FROM CUSTOMER_CHECK_ACCOUNT WHERE CHECK_ACCOUNT_ID = '" + accid + "'" + " AND CUSTOMER_ID = '" + ownerid + "'" + " AND BANK_NAME = '" + bank + "'"
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


