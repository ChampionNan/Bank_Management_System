import pymysql

try:
    db = pymysql.connect(host = '127.0.0.1', user = 'root', password = 'Cbn111156789!',db = "Lab3" ,port = 3306)
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    print("ok")

except pymysql.Error as e:
    print("连接失败")

finally:
    if db:
        db.close()