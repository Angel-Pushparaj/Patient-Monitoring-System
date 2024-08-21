import mysql.connector
mydb=mysql.connector.connect(host="localhost",port="3306",user="root",password="sam@2004@")
mycursor=mydb.cursor()
mycursor.execute("CREATE DATABASE patient")
