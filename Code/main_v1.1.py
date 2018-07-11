import pyttsx
import threading
import MySQLdb
import codecs
import time,os
from gtts import gTTS 
from RPLCD import CharLCD
#####################QUEUE#############################
delay=0.6
strt_time=0
elapsed_time=0
wait_list=[] #consists of numbers ,indicating effective wait time for each elements in the list
class Queue:
	def __init__(self):
		self.items= []
	def isEmpty(self):
		return self.items ==[]
	def enqueue(self, item):
		self.items.insert(0,item)
	def dequeue(self):
		self.items.pop()
	def size(self):
		return len(self.items)
	def access(self,index):
		return self.items[index]
	def search(self,mac):
		if self.items== []:
			return 0,False
		else:
			for i in range(len(self.items)):
				if self.items[i]==mac:
					return i, True
			return i, False

def e_wait(elapsed_time,index):
	a=index*delay-elapsed_time
	return a
##########################################################
##################LCD#####################################
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[ 23, 29, 31, 33])
lcd.clear()
#'40, 38, 36, 32,'
def lcd_print(ssid):
	lcd.clear()
	lcd.write_string(u'Bus '+ssid)
	lcd.cursor_pos =(1,0)
	lcd.write_string(u'has arrived')
#################################################	
	
lines=[]
r=();
list_len=0
list_mac=[]
list_ssid=[]
list_seek=0
thread_list=[]
dev_found_status=0
######################NOTIFICATION#################
def hindi_noti(ssid):
	with codecs.open('hindi.txt', encoding='utf-8') as f:
		input = f.read()
		if(ssid=="Eddyston"):
			lcd_print(ssid)
			os.system("mpg321 -g 400 eddystone_hindi.mp3")
			os.system("mpg321 -g 400 eddystone_english.mp3")
		if(ssid=="C2305"):
			lcd_print(ssid)
			os.system("mpg321 -g 400 c2305_hindi.mp3")
			os.system("mpg321 -g 400 c2305_english.mp3")
		if(ssid=="HMSoft"):
			lcd_print(ssid)
			os.system("mpg321 -g 400 hmsoft_hindi.mp3")
			os.system("mpg321 -g 400 hmsoft_english.mp3")
		#audio=ssid+input
		#audio_out(audio) #audio output in hindi
		print '\n\n'
		print '**********'
		print ssid,input
############################################################
		
from bluepy.btle import Scanner, DefaultDelegate
engine = pyttsx.init()
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
		#print "Discovered device:", dev.addr
		list_mac.append(dev.addr)		
	elif isNewData:
			print "\n"
            #print "Received new data from", dev.addr

			
def no_device_in_range():
			lcd_happy_journey()
			while(q.isEmpty()==False):
				q.dequeue()
			elapsed_time=0
			strt_time=0
			del wait_list[:]	
			wait_list.append(2.5)
def lcd_happy_journey():			
			lcd.clear()
			lcd.cursor_pos =(0,4)
			lcd.write_string(u'Welcome')
			lcd.cursor_pos =(1,0)
			lcd.write_string(u'Happy Journey!!!')

def search(list_len,list_seek,strt_time):	
	try:
		
		seek = db.cursor()
		#print argv,script
		while(list_seek<list_len):
			
			sql = ('SELECT SSID FROM macssid WHERE MAC= %s', list_mac[list_seek])
			seek.execute(*sql);
			db.commit()
			r=seek.fetchall()#store_result();#seek.fetchall()
			##

			if r:
				
				print r
				print list_mac[list_seek]
				mac=list_mac[list_seek]
				index,status=q.search(mac)
				print "Status=",status
				print wait_list[:]
				if status==True:
					#try poping using wait list
					lcd_happy_journey() #
					for j in range(len(wait_list)):
						elapsed_time=time.clock()-strt_time
						print "Elapsed_time:",elapsed_time
						if elapsed_time > wait_list[0]:
							q.dequeue()
							print "popped"
							if q.isEmpty()==True:
								#del wait_list[:]
								wait_list[0]=wait_list[0]+delay;
								print "Empty "
							else:	
								wait_list[j]=wait_list[j+1]	
								print "Here"			
				else:	
					if q.isEmpty()==True:
						q.enqueue(mac)
						print "Stacked"
						strt_time=time.time()
						hindi_noti(r[0][0])
						print '\n\n'
						print '**********'
						print "SSID:-",r[0][0],",has arrived!"
						wait_list.append(e_wait(0,1))


					else:
						q.enqueue(mac)
						elapsed_time=time.time()-strt_time #update elapsed time
						i=q.size()
						hindi_noti(r[0][0])
						print "wait list e-wait update"
						print '\n\n'
						print '**********'
						print "SSID:-",r[0][0],",has arrived!"
						wait_list.append(e_wait(elapsed_time,i)) #update wait list	

			else:			
				no_device_in_range()
					
						
				
						
			list_seek=list_seek+1
				
		#return list_seek
		
	except KeyboardInterrupt:
		db.close()
		GPIO.clear()
		lcd.clear()

#list_len=scanner(list_len)
q=Queue()
db = MySQLdb.connect("localhost","root","raspberry","busid" )
while(1):
	r=();
	try:
		scanner = Scanner().withDelegate(ScanDelegate())
		devices = scanner.scan(2.0)
		if devices:
			print "\n*****Discovered Devices*****\n"
			for dev in devices:
				print "Device MAC: %s, RSSI=%d dB" % (dev.addr, dev.rssi)
				list_mac.append(dev.addr)
			print list_mac
			list_len=len(list_mac)
			print '\n*****Valid Devices******\n'
			search(list_len,list_seek,strt_time)
			list_seek=0
			del list_mac[:]
		
			
			
				
	except KeyboardInterrupt:
		print "Program closed unexpetedly"
		exit()	

###############TESTED for one DEVICE################
