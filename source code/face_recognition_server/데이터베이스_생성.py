import sqlite3

conn = sqlite3.connect("info.db", isolation_level=None)
c = conn.cursor()

# 기존 테이블 삭제
c.execute("DROP TABLE IF EXISTS information")

# 새로운 테이블 생성
c.execute("CREATE TABLE IF NOT EXISTS information(pk INTEGER PRIMARY KEY AUTOINCREMENT, encoding TEXT, name TEXT, sex TEXT, age INTEGER, area TEXT, date TEXT, phone TEXT)")


c.close()
conn.close()