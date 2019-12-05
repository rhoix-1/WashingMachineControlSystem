# Platt Tech Nasa Hunch Team (Ethan Feldman <3 Josepher Shunaula)
# + Justin Kelly (Outside Partner <3)

import mysql.connector
import datetime

# Gets the current dataTime in the MySQL dateTime format
def Now():
	return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Connects to justin's MySQL server on his computer
# His IP-Addess: 24.2.213.138
mydb = mysql.connector.connect(
	host="mysql.kellyweb.space",
	user="roboto",
	passwd="@Plattist1",
	database="hunch"
)

# This is execute commands
mycursor = mydb.cursor()

# sql commands and %s passes in val data
sql = "INSERT INTO logs (info, dateTime) VALUES (%s, %s)"
val = ("Whatever information we want to send", Now())
mycursor.execute(sql, val)

mydb.commit()
