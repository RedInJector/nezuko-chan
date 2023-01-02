import sqlite3 as sql


con = sql.connect('test.db')
table = 'test1'

with con:
	cur = con.cursor()

check = cur.execute(f"SELECT * FROM {table} WHERE Discord_tag = 'RedInJector#5506'").fetchone()
print(check)
con.commit()
