import mysql.connector
print("Enter Password")
pw=input()

#mydb=mysql.connector.connect(host="localhost",user="root",passwd=pw)
mydb=mysql.connector.connect(host="localhost",user="root",passwd=pw, database="testdb")
mycursor=mydb.cursor()

#mycursor.execute("CREATE DATABASE IF NOT EXISTS testdb")

#mydb=mysql.connector.connect(host="localhost",user="root",passwd=pw, database="testdb")


mycursor.execute("CREATE TABLE IF NOT EXISTS students (name VARCHAR(255) , file TEXT) ")

sqlFormula = "INSERT INTO students (name, file) VALUES (%s, %s)"
students=[]

def storingdb():
    print("How many files you wanna store ?, Give interger input")
    a=int(input())
    for i in range(a):
        print("enter the name of the student")
        name=input()
        print("give the path to the file")
        path = input()
        fhand=open(path)
        file=fhand.read()
        fhand.close()
        students.append((name, file))
        
    mycursor.executemany(sqlFormula, students)
    mydb.commit()

def printdb():   
    print("Printing the data stored")
    mycursor.execute("SELECT * FROM students")
    
    myresult = mycursor.fetchall()
    
    for row in myresult:
        print(row)