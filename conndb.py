import pymysql
import sys
import base64
import pickle

class database:
    host = "localhost"
    user = "root"
    pasw = ""
    db   = "animelist"

    # Konek database
    try:
        conn = pymysql.connect(host = host, user = user, password = pasw, db = db, use_unicode=True, charset='utf8')
        print("TERKONEKSI DENGAN DATABASE")
        print("#####################################################")
    except Exception as e:
        sys.exit("KONEKSI DENGAN DATABASE GAGAL !!!!!", e)

    # kursor
    dbcursor = conn.cursor()
    print("----------------------------------------------------------------------")
