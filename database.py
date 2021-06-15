import sqlite3  

connection = sqlite3.connect('student.db')
#with open('student.sql') as f:
#        connection.executescript(f.read())
cursor = connection.cursor()
#cursor.execute("CREATE TABLE user (s_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL,passwordd VARCHAR NOT NULL);")

#cursor.execute("INSERT INTO user (username, passwordd) VALUES ('nandita', '12345')")
#cursor.execute("INSERT INTO user (username, passwordd) VALUES ('pooja', '5678')")
cursor.execute("SELECT * from user")
r = cursor.fetchall()
print(r)
connection.commit()
connection.close()  