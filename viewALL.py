import mysql.connector as mysql

passFile = open("pass.txt","r")
mysql_pass = passFile.readline()
passFile.close()

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = mysql_pass,
    database = "test"
)

cursor = db.cursor()

## defining the Query
query = "SELECT * FROM cameradatabasefinal"

## getting records from the table
cursor.execute(query)

## fetching all records from the 'cursor' object
records = cursor.fetchall()

## Showing the data
for record in records:
    print(record)