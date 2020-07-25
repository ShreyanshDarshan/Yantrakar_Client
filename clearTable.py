import mysql.connector as mysql

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "darshan_sql",
    database = "test"
)

cursor = db.cursor()

## defining the Query
query = "DELETE FROM cameradatabasefinal"

## executing the query
cursor.execute(query)

## final step to tell the database that we have changed the table data
db.commit()