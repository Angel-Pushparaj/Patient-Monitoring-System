from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui
import sys
import pyttsx3
import serial
import time
import pyttsx3
from patentmonitor import Ui_Dialog
from datetime import date
from datetime import datetime
import mysql.connector
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
mydb=mysql.connector.connect(host="localhost",
                             port="3306",
                             user="root",
                             password="",
                             database="patient"
                             )
a=[]
class mainFile(QDialog):
    def __init__(self):
        super(mainFile,self).__init__()
        print("Setting up GUI")
        self.firstUI = Ui_Dialog()
        self.firstUI.setupUi(self)
        self.firstUI.pushButton_4.clicked.connect(self.measure)
        self.firstUI.pushButton_2.clicked.connect(self.speak)
        self.firstUI.pushButton_3.clicked.connect(self.exit)
        self.firstUI.pushButton_5.clicked.connect(self.graph)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.firstUI.verticalLayout.addWidget(self.canvas)
          # Replace 'COM3' with your Arduino's port
          # Allow time for the connection to establish
    def measure(self):
        #ro = 36.8
        #te = 98.4
        date1=date.today()
        time1=datetime.now()
        curr = time1.strftime("%H:%M:%S")
        ser = serial.Serial('COM5', 9600)
        ser.write(b'1')  # Send a signal to start the measurement on Arduino
        distance = ser.readline().decode().strip()
        a=distance.split()
        #self.firstUI.label_13.setText(a[0])
        self.firstUI.label_10.setText(a[1]+"F")
        self.firstUI.label_12.setText(a[0])
        self.firstUI.label_11.setText(a[2]+"%")
        heart = self.firstUI.label_12.text()
        room = self.firstUI.label_11.text()
        temp = self.firstUI.label_10.text()
        mycursor=mydb.cursor()
        mycursor.execute("INSERT INTO pat1(date,time,heart,temperature,room) VALUES(%s,%s,%s,%s,%s)",(date1,curr,heart,temp,room))
        mydb.commit()
        
          # Wait before taking the next measurement
    def speak(self):
        en=pyttsx3.init()
        #aq=self.firstUI.label_13.text()
        tem=self.firstUI.label_10.text()
        hum=self.firstUI.label_11.text()
        heart=self.firstUI.label_12.text()
        en.setProperty("rate",200)
        en.say("Your Body temperature is "+tem+"Farenheat "+"and")
        en.say("Room humidity is"+hum+"and")
        en.say("your heart rate is"+heart+"beatsperminute")
        #en.say("Sam")
        en.runAndWait()
    def exit(self):
        sys.exit()
    def graph(self):
        mycursor=mydb.cursor()
        mycursor.execute("SELECT time,heart FROM pat1")
        he=[]
        x1=[]
        y1=[]
        for x in mycursor:
            for y in x:
                he.append(y)
        mydb.commit()
        for i in range(0,len(he),2):
            x1.append(he[i])
        for i in range(1,len(he),2):
            y1.append(he[i])
        mycursor.execute("SELECT time,temperature FROM pat1")
        temp=[]
        x2=[]
        y2=[]
        for x in mycursor:
            for y in x:
                temp.append(y)
        mydb.commit()
        for i in range(0,len(he),2):
            x2.append(temp[i])
        for i in range(1,len(he),2):
            y2.append(temp[i])
        mycursor.execute("SELECT time,room FROM pat1")
        room=[]
        for x in mycursor:
            for y in x:
                room.append(y)
        x3=[]
        y3=[]
        for x in mycursor:
            for y in x:
                temp.append(y)
        mydb.commit()
        for i in range(0,len(he),2):
            x3.append(temp[i])
        for i in range(1,len(he),2):
            y3.append(temp[i])
        # Plot the data
        self.ax.set_xticks(range(0,100,10))
        self.ax.plot(x1,y1, marker='o', linestyle='-')
        self.ax.plot(x1,y2, marker='o', linestyle='-')
        self.ax.plot(x1,y3, marker='o', linestyle='-')

        # Set labels and title
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Sensor Reading')
        self.ax.set_title('Patient Monitor')
        self.ax.legend(['Heart','Room humidity'])
        # Show the plot
        self.canvas.draw() 


if __name__=='__main__':
    app=QApplication(sys.argv)
    ui=mainFile()
    ui.show()
    sys.exit(app.exec_())
