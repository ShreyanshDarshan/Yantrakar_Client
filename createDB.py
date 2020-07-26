import mysql.connector as mysql

passFile = open("pass.txt","r")
mysql_pass = passFile.readline()
passFile.close()

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = mysql_pass
)

## creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
cursor = db.cursor()

## creating a databse called 'datacamp'
## 'execute()' method is used to compile a 'SQL' statement
## below statement is used to create tha 'datacamp' database
cursor.execute("CREATE DATABASE test")