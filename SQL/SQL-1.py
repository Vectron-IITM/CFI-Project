import mysql.connector


mydb=mysql.connector.connect(host="localhost",user="root",passwd="Macbookpro",database="testdb")
#print(mydb) to check the connection

mycursor=mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS testdb")
#mycursor.execute("SHOW DATABASES") to see the existing databases

mycursor.execute("CREATE TABLE IF NOT EXISTS students (name VARCHAR(255) , file TEXT) ")

sqlFormula = "INSERT INTO students (name, file) VALUES (%s, %s)"
students=[]
mycursor.executemany(sqlFormula, students)
mydb.commit()


mycursor.execute("SELECT * FROM students")

myresult = mycursor.fetchall()

for row in myresult:
    print(row)
    
sql= "DROP TABLE IF EXITS students"
mycursor.execute(sql)
mydb.commit()