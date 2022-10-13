# import psycopg2

# conn = psycopg2.connect(host="localhost", database="regdb", user="admin", password="admin")
# # conn.autocommit = True
  
# # cursor = conn.cursor()
  
# # cursor.execute('CREATE database regdb')
# # print("Database has been created successfully !!");
# conn.close()


# import psycopg2

# conn = psycopg2.connect(host="localhost", database="regdb", user="admin", password="admin")
# conn.autocommit = True
  
# cursor = conn.cursor()
  
# cursor.execute('CREATE TABLE IF NOT EXISTS requests(ID  SERIAL PRIMARY KEY, hash TEXT NOT NULL, region TEXT NOT NULL, \
#     commune TEXT NOT NULL, type TEXT NOT NULL, surface REAL NOT NULL, prix REAL NOT NULL, date timestamp NOT NULL DEFAULT NOW())')
# print("table has been created successfully !!");
# conn.close()

import psycopg2

conn = psycopg2.connect(host="localhost", database="regdb", user="admin", password="admin")
conn.autocommit = True
cursor = conn.cursor()

cursor.execute('''SELECT * from requests''')

#Fetching 1st row from the table
result = cursor.fetchall();
print(result)
conn.close()