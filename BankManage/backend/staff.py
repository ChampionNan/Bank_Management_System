from flask import Flask, request, jsonify, make_response, Blueprint
from flask_cors import *
import json
import time
import pymysql

staff_api = Blueprint('staff_api', __name__)

@staff_api.route('/staff', methods=['POST'])
def staff():
    rstype = request.form['type']
    if rstype == 'Search':
        print('Search')
        db = pymysql.connect('127.0.0.1', 'root', 'Cbn111156789!', "Lab3", 3306)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

        nameSearch = request.form['nameSearch'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        idSearch = request.form['idSearch'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        bankSearch = request.form['bankSearch'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        deptSearch = request.form['deptSearch'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        telSearch = request.form['telSearch'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        addrSearch = request.form['addrSearch'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        lowerBound = request.form['lowerBound']
        upperBound = request.form['upperBound']

        print(deptSearch)

        sqlcommand = "SELECT EMPLOYEE_ID AS id, EMPLOYEE_NAME AS name, EMPLOYEE_BANK_NAME AS bank, EMPLOYEE_DEPART_ID AS dept, EMPLOYEE_PHONE AS tel, EMPLOYEE_ADDRESS AS addr, EMPLOYEE_ENTERDATE AS date_s FROM EMPLOYEE WHERE EMPLOYEE_ID IS NOT NULL"
        if len(nameSearch) > 0:
            sqlcommand = sqlcommand + " AND EMPLOYEE_NAME LIKE '%" + nameSearch + "%'"
        if len(idSearch) > 0:
            sqlcommand = sqlcommand + " AND EMPLOYEE_ID LIKE '%" + idSearch + "%'"
        if len(bankSearch) > 0:
            sqlcommand = sqlcommand + " AND EMPLOYEE_BANK_NAME LIKE '%" + bankSearch + "%'"
        if len(deptSearch) > 0:
            sqlcommand = sqlcommand + " AND EMPLOYEE_DEPART_ID LIKE '%" + deptSearch + "%'"
        if len(telSearch) > 0:
            sqlcommand = sqlcommand + " AND EMPLOYEE_PHONE LIKE '%" + telSearch + "%'"
        if len(addrSearch) > 0:
            sqlcommand = sqlcommand + " AND EMPLOYEE_ADDRESS LIKE '%" + addrSearch + "%'"
        if len(lowerBound) > 0:
            sqlcommand = sqlcommand + " AND EMPLOYEE_ENTERDATE > STR_TO_DATE('" + lowerBound + "','%Y-%m-%d')"
        if len(upperBound) > 0:
            sqlcommand = sqlcommand + " AND EMPLOYEE_ENTERDATE < STR_TO_DATE('" + upperBound + "','%Y-%m-%d')"

        print(sqlcommand)
        cursor.execute(sqlcommand)
        result = cursor.fetchall()
        print(result)
        for line in result:
            line['id'] = str(line['id'])
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
        # print('ok12')
        id_s = request.form['id']
        name = request.form['name'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        bank = request.form['bank'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        dept = request.form['dept']
        tel = request.form['tel']
        addr = request.form['addr'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        date_s = request.form['date_s']
        old_primary = request.form['old_primary'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')

        sqlcommand = ""
        # 改
        # print('hello', old_primary)
        if len(old_primary) > 0:
            if id_s != old_primary:
                args = [old_primary, id_s, 0]
                print('ok1')
                result_args = cursor.callproc('CHANGE_EMPLOYEE_NAME', args)
                print(result_args[2])
                print('ok2')

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
            sqlcommand = sqlcommand + " UPDATE EMPLOYEE SET"
            if len(name) > 0:
                sqlcommand = sqlcommand + " EMPLOYEE_NAME = '" + name + "',"
            if len(bank) > 0:
                sqlcommand = sqlcommand + " EMPLOYEE_BANK_NAME = '" + bank + "',"
            if len(dept) > 0:
                sqlcommand = sqlcommand + " EMPLOYEE_DEPART_ID = '" + dept + "',"
            if len(tel) > 0:
                sqlcommand = sqlcommand + " EMPLOYEE_PHONE = '" + tel + "',"
            if len(addr) > 0:
                sqlcommand = sqlcommand + " EMPLOYEE_ADDRESS = '" + addr + "',"
            if len(date_s) > 0:
                sqlcommand = sqlcommand + " EMPLOYEE_ENTERDATE = STR_TO_DATE('" + date_s + "','%Y-%m-%d'),"

            sqlcommand = sqlcommand[:len(sqlcommand) - 1]
            sqlcommand = sqlcommand + " WHERE EMPLOYEE_ID = '" + id_s + "'"
            # print(sqlcommand)
        # 增
        else:
            insert = "('" + id_s + "','" + name + "','" + bank + "','" + dept + "','" + tel + "','" + addr + "'," + "STR_TO_DATE('" + date_s + "','%Y-%m-%d'))"
            sqlcommand = sqlcommand + " INSERT EMPLOYEE(EMPLOYEE_ID, EMPLOYEE_NAME, EMPLOYEE_BANK_NAME, EMPLOYEE_DEPART_ID, EMPLOYEE_PHONE, EMPLOYY_ADDRESS, EMPLOYEE_ENTERDATE) VALUES" + insert
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
        sqlcommand = "SELECT * FROM EMPLOYEE_CUSTOMER WHERE EMPLOYEE_ID = '" + primary + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)
        result = cursor.fetchall()
        if len(result) > 0:
            cursor.close()
            db.close()
            response = make_response(jsonify({
                'code': 403,
                'msg': '有关联客户信息'
            }))
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response
        sqlcommand = "DELETE FROM EMPLOYEE WHERE EMPLOYEE_ID = '" + primary + "'"
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

# 客户关系查询
@staff_api.route('/staffCustomer', methods=['POST'])
def staffCustomer():
    rstype = request.form['type']
    if rstype == 'SearchByStaff':
        print('SearchByStaff')
        db = pymysql.connect('127.0.0.1', 'root', 'Cbn111156789!', "Lab3", 3306)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        staffID = request.form['staffid'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')

        sqlcommand = "SELECT EMPLOYEE_CUSTOMER.CUSTOMER_ID AS id, CUSTOMER.CUSTOMER_NAME AS name, EMPLOYEE_CUSTOMER.SERVICETYPE AS type FROM EMPLOYEE_CUSTOMER, CUSTOMER WHERE EMPLOYEE_CUSTOMER.CUSTOMER_ID = CUSTOMER.CUSTOMER_ID AND EMPLOYEE_CUSTOMER.EMPLOYEE_ID = '" + staffID + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)
        result = cursor.fetchall()
        for line in result:
            line['id'] = str(line['id'])

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

    if rstype == 'SearchByCustomer':
        custID = request.form['custid'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        print('SearchByCustomer')
        print(custID)

        db = pymysql.connect('127.0.0.1', 'root', 'Cbn111156789!', "Lab3", 3306)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

        sqlcommand = "SELECT EMPLOYEE_CUSTOMER.EMPLOYEE_ID AS staffid, EMPLOYEE.EMPLOYEE_NAME AS staffname, EMPLOYEE_CUSTOMER.SERVICETYPE AS type FROM EMPLOYEE_CUSTOMER, EMPLOYEE WHERE EMPLOYEE_CUSTOMER.EMPLOYEE_ID = EMPLOYEE.EMPLOYEE_ID AND EMPLOYEE_CUSTOMER.CUSTOMER_ID = '" + custID + "'"
        print(sqlcommand)
        cursor.execute(sqlcommand)
        result = cursor.fetchall()

        for line in result:
            line['staffid'] = str(line['staffid'])

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
        print("ok11")
        db = pymysql.connect('127.0.0.1', 'root', 'Cbn111156789!', "Lab3", 3306)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        print("ok12")
        custID      = request.form['custID']
        print("ok13")
        custID      = custID.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        print("ok14")
        staffID     = request.form['staffID']
        print("ok15")
        staffID     = staffID.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        print("ok16")
        serviceType = request.form['serviceType']
        print("ok17")
        serviceType = serviceType.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        print("ok18")
        old_custID  = request.form['old_custID']
        print("ok19")
        old_custID  = old_custID.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        print("ok20")
        old_staffID = request.form['old_staffID']
        print("ok21")
        old_staffID = old_staffID.rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')

        sqlcommand = ""
        print("ok1")
        if len(old_custID) > 0 and len(old_staffID) > 0:
            print('改')
            sqlcommand = sqlcommand + "UPDATE EMPLOYEE_CUSTOMER SET"
            if len(custID) > 0:
                sqlcommand = sqlcommand + " CUSTOMER_ID = '" + custID + "',"
            if len(staffID) > 0:
                sqlcommand = sqlcommand + " EMPLOYEE_ID = '" + staffID + "',"
            if len(serviceType) > 0:
                sqlcommand = sqlcommand + " SERVICETYPE = '" + serviceType + "',"

            sqlcommand = sqlcommand[:len(sqlcommand) - 1]
            sqlcommand = sqlcommand + " WHERE CUSTOMER_ID = '" + old_custID + "'"
            sqlcommand= sqlcommand + " AND EMPLOYEE_ID = '" + old_staffID + "'"
        # 增
        else:
            insert = "('" + custID + "','" + staffID + "','" + serviceType + "')"
            sqlcommand = sqlcommand + " INSERT INTO EMPLOYEE_CUSTOMER(CUSTOMER_ID, EMPLOYEE_ID, SERVICETYPE) VALUES" + insert
        print("ok2")
        print(sqlcommand)

        try:
            cursor.execute(sqlcommand)
        except:
            print('Error:400')
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

        custID = request.form['custid'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')
        staffID = request.form['staffid'].rstrip().replace('\'','').replace('\"','').replace('%','').replace('#','').replace(',','').replace(')','').replace('(','').replace('}','').replace('[','').replace(']','').replace('{','')

        sqlcommand = "DELETE FROM EMPLOYEE_CUSTOMER WHERE EMPLOYEE_ID = '" + staffID + "'" + "  AND CUSTOMER_ID = '" + custID + "'"
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







