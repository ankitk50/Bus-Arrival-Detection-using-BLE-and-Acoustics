
#aim and updates:To  reduce lock release time
#finally: GPIO.cleanup() to be added.

import threading 
from threading import Lock
import MySQLdb
import codecs,RPi.GPIO as GPIO
import time,os
from RPLCD import CharLCD

###########################Variables##############################	
r=();
list_len=0
list_mac=[]
list_ssid=[]
delay=30 #waiting time in the queue (this is a pseudo time ie has no ref from the sys time)
timeout=0# used for saving current time as a shared resource
###################################################################
##############################QUEUE################################
GPIO.setwarnings(False)
lock=Lock()
#a queue is used to make keep track of arrived busses to aviod multiple announcemnts of same bus for a time duration.
class Queue:
	def __init__(self):
		self.items= []
		self.wait_list=[]	
	def isEmpty(self):
		return self.items ==[]
	def enqueue(self, item):
		global p,q,timeout
		self.items.insert(0,item)
		self.wait_list.append(q.e_wait(timeout,len(self.items)))#update wait_list
		print "Wait_list=",self.wait_list
       	def dequeue(self):
		self.items.pop()
		del self.wait_list[0]
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
					
	def e_wait(self,elapsed_time,index):
		a=index*delay-elapsed_time
		return a
	
###################################################################################			
###################################################################################
			
class timed_pop(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		
		global q,p,timeout
		print p.elapsed_time	
		while True:
			lock.acquire()
			#print "timed_pop acquired the lock\n"
			
			if (q.isEmpty()==False):
				print "Current time=,",timeout, 
				print "Waiting Threshold=",q.wait_list
				if(timeout > q.wait_list[0]):
					
					print "something is popped!!!"
					q.dequeue()
			#print "timed_pop releasing the lock\n"
			lock.release()
			time.sleep(.00001)	

#coundn't use this class as the p.elapsed_time and p.get_time failed to update!!![FIXED via timeout variable]		
############################################################################################
############################################################################################		
class stop_watch(threading.Thread):	
	def __init__(self):
		self.elapsed_time=0	
		threading.Thread.__init__(self)
	def pseudo_delay(self,count):
		i=0
		while(i<10000*count):
			i=i+1
	def run(self):
		global q,p,timeout
		while(1):
			lock.acquire()
			#print "Stopwatch acquired the lock\n"
			if q.isEmpty()==True:
				self.elapsed_time=0
				#print "Stopwatch releasing the lock,Queue Empty\n"
				lock.release()#<----ATTENTION
				time.sleep(.00001)	

			else:	
				p.pseudo_delay(100)
				self.elapsed_time=self.elapsed_time+1
				timeout=self.elapsed_time
				print "Elapsed Time=",timeout
				lock.release()
				time.sleep(.00001)
			
	def get_time(self):
		return self.elapsed_time
	
####################################LCD########################################
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[ 23, 29, 31, 33])
lcd.clear()
#'40, 38, 36, 32,'
def lcd_print(ssid):
	lcd.clear()
	lcd.write_string(u'Bus '+ssid)
	lcd.cursor_pos =(1,0)
	lcd.write_string(u'has arrived')
###############################################################################	

######################NOTIFICATION############################################
#todo-dynamic
def hindi_noti(ssid):
		lock.acquire()
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
		lock.release()
		time.sleep(.00001)	

###############################################################################
######################BLE_INIT#################################################		
from bluepy.btle import Scanner, DefaultDelegate

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

###############################################################			
###################MISCLANEOUS#################################

def no_device_in_range():
			lcd_happy_journey()
	
			
def lcd_happy_journey():			
			#print "No device in range"
			lock.acquire()
			lcd.clear()
			lcd.cursor_pos =(0,4)
			lcd.write_string(u'Welcome')
			lcd.cursor_pos =(1,0)
			lcd.write_string(u'Happy Journey!!!')
			lock.release()
			time.sleep(.00001)


def search(list_len,list_seek):	
	try:
		seek = db.cursor()
		while(list_seek<list_len):
			sql = ('SELECT SSID FROM macssid WHERE MAC= %s', list_mac[list_seek])
			seek.execute(*sql);
			db.commit()
			r=seek.fetchall()
			
			if r:
				print r
				print list_mac[list_seek]
				mac=list_mac[list_seek]
				index,status=q.search(mac)
				if status==True:
					#print" Device already present in queue \n No VALID NEW device found\n"
					lcd_happy_journey()
								
				else:	
					if q.isEmpty()==True: #triggerflag
						q.enqueue(mac)
						hindi_noti(r[0][0])
						print "SSID:-",r[0][0],",has arrived!"
					
					else:
						q.enqueue(mac)
						hindi_noti(r[0][0])
						print "SSID:-",r[0][0],",has arrived!"
						

			else:			
				no_device_in_range()
									
			list_seek=list_seek+1
		
	except KeyboardInterrupt:
		db.close()
		GPIO.cleanup()
		lcd.clear()

def scan():
		while(1):
						
			#r=();
			
			try:
				
				scanner = Scanner().withDelegate(ScanDelegate())
				devices = scanner.scan(2.0)
				#print "scan acquired the lock\n"
				if devices:
					#print "\n*****Discovered Devices*****\n"
					for dev in devices:
						#print "Device MAC: %s, RSSI=%d dB" % (dev.addr, dev.rssi)
						list_mac.append(dev.addr)
					#print list_mac
					list_len=len(list_mac)
					#print '\n*****Valid Devices******\n'
					list_seek=0
					search(list_len,list_seek)
					list_seek=0
					del list_mac[:]
				else:
					no_device_in_range()
					print "No device in range"
					lcd_happy_journey()
				#print "\nscan releasing the lock\n"	

			except KeyboardInterrupt:
				print "Program terminated unexpetedly"
				lcd.clear()
				GPIO.cleanup()
				exit()	
				
		
q=Queue()
p=stop_watch()
db = MySQLdb.connect("localhost","root","raspberry","busid" )#database connection establishment
def Main():
	t1=timed_pop()
	t2=stop_watch()
	t2.start()
	t1.start()
	scan()

	
	print "\nMain Complete\n"

if __name__=="__main__":
	Main()

finally:
	print "Closing... cleared all GPIOs"
	GPIO.cleanup();
################################################################
#queue is flushed ambiguously--conlusion left the idea of flushing the queue when no device in range.
#wait time update has some problem ---fixed

