import mysql.connector
mydb=mysql.connector.connect(host="localhost",
                             port="3306",
                             user="root",
                             password="sam@2004@",
                             database="patient"
                             )
mycursor=mydb.cursor()
#mycursor.execute("INSERT INTO students(name,age) VALUES(%s,%s)",("SAm",18))
mycursor.execute("DELETE FROM pat1")
mydb.commit()

#mycursor.execute("SELECT time,heart,temperature,room FROM pat1")
#a=[]
#for x in mycursor:
  #  for y in x:
    #    a.append(y)
#print(a)


