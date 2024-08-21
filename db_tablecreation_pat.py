import mysql.connector
mydb=mysql.connector.connect(host="localhost",
                             port="3306",
                             user="root",
                             password="",
                             database="patient"
                             )
mycursor=mydb.cursor()
mycursor.execute("CREATE TABLE pat1(date varchar(10),time varchar(10),heart INTEGER(10),temperature FLOAT,room FLOAT)")
