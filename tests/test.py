# from db import *
#
#
# db = SessionLocal()
# bestiaries = db.query(BestiariesList).all()
# for bestiary in bestiaries:
#     print(f"ID: {bestiary.id}, Name: {bestiary.name}, Author: {bestiary.author}, Date Creation: {bestiary.date_creation}, Latest Update: {bestiary.latest_update}")
# db.close()


import psycopg2

db_params = {
    "host": "217.71.129.139",
    "database": "bistimakerdb",
    "user": "client",
    "password": "password",
    "port": "4872"
}
conn = psycopg2.connect(**db_params)
cur = conn.cursor()


# cur.execute('DELETE FROM entities WHERE id = 1;')
# conn.commit()

cur.execute('select * from bestiaries;')
result = cur.fetchall()
print(*result, sep='\n')


# cur.execute('''ALTER TABLE bestiaries
# ADD COLUMN is_published BOOLEAN DEFAULT FALSE;''')
# conn.commit()



# cur.execute('DROP TABLE entities;')
# cur.execute('DROP TABLE categories;')
# cur.execute('DROP TABLE bestiaries;')
# conn.commit()



