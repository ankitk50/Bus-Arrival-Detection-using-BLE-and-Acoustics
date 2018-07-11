import MySQLdb
import time
from gtts import gTTS #to create mp3 file for SSID
try:
	db = MySQLdb.connect("localhost","root","raspberry","busid" )
	
	k=input("Enter the num of entries\n")
	for num in range(k):
		var1=raw_input("Enter MAC value \n")
		var2=raw_input("Enter SSID value \n")	
		print var1,var2
		seek = db.cursor()
		sql = ('INSERT INTO macssid(MAC, SSID) VALUES (%s ,%s )',(var1,var2))	
		seek.execute(*sql)
		db.commit()
	#sql=('SELECT * from macssid ORDER BY %s %s', ('SSID','ASC'))
	#sql=('SELECT * from macssid ORDER BY %s %s', ('ID', 'ASC'))
	#seek.execute(*sql)
	#seek.execute(*sql)
	with open("Output.txt", "a") as text_file:
		text_file.write("MAC: {0}\nSSID: {1}\n".format(var1,var2))

	print '\n All entries saved to database and Output.txt \n'
	db.close()

	
	
except KeyboardInterrupt:
	pass
	db.close()

def mp3_noti(SSID):
	#SSID to file input
	#

	#log/TODO
	#algo for MP3 notification creation for different SSID
	#no further changes needed
