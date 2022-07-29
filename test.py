import time
import mariadb
conn = mariadb.connect(user="root", password="1q2w3eazsxdc", host="127.0.0.1", port=3306, database="chatthew_test")
dbcur = conn.cursor()

while True:
    dbcur.execute('select * from blurse where type ="bless"')
    x = 0
    for r in dbcur:
        x+= 1
    print(x)
    time.sleep(1)
