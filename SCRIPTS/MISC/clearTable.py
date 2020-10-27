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
query = "DELETE FROM cameradatabasefinal"

## executing the query
cursor.execute(query)

## final step to tell the database that we have changed the table data
db.commit()