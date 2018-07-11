
import threading 
from threading import Thread,Lock
import MySQLdb
import codecs,RPi.GPIO as GPIO
import time,os
from gtts import gTTS 
from RPLCD import CharLCD
###edited via ssh
#####################QUEUE##############################
GPIO.setwarnings(False)
lock=Lock()
class Queue:
	def __init__(self):
		self.items= []
		self.wait_list=[]	
	def isEmpty(self):
		return self.items ==[]
	def enqueue(self, item):
		global p,q
		self.items.insert(0,item)
		self.wait_list.append(q.e_wait(p.elapsed_time,len(self.items)))#update wait_list
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
	
			
			
class timed_pop(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		global q,p
		while True:
			condition.acquire()
			print "\t\t\ttimed_pop_started"
			if (q.isEmpty()==False):
				if (p.elapsed_time > self.wait_list[0]):
					q.dequeue()
			condition.notify()
			condition.release()	

		
	
		
class stop_watch(threading.Thread):	
	def __init__(self):
		self.elapsed_time=0	
		threading.Thread.__init__(self)
	def pseudo_delay(self,count):
		i=0
		while(i<10000*count):
			i=i+1
	def run(self):
		global q,p
		while(1):
			condition.acquire()
			while(q.isEmpty()==True):
				self.elapsed_time=0
				print("           stop_watch")
				#break
			p.pseudo_delay(1)
			self.elapsed_time=self.elapsed_time+1
			print self.elapsed_time
			condition.release()
			#break
	def get_time(self):
		return self.elapsed_time
	
	
			
		
'''	
def pseudo_delay(self,count):
		i=0
		while(i<10000*count):
			i=i+1
def count(self):
	global q,elapsed_time 
	while(1):
		while(q.isEmpty()==True):
			elapsed_time=0
			print("           stop_watch")
			#break
		pseudo_delay(100) #100 args gives the feel of 1 sec
		elapsed_time=elapsed_time+1
		print elapsed_time			
'''	

###################THREADS############################################
def counter_thread(delay):
	global elapsed_time
	while(1):
		time.sleep(delay)
		elapsed_time=elapsed_time+delay

	
#########################################################################		
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
###########################Variables##############################	
lines=[]
r=();
list_len=0
list_mac=[]
list_ssid=[]
#list_seek=0
thread_list=[]
dev_found_status=0
delay=10
#strt_time=0
elapsed_time=0
#wait_list=[] #consists of numbers ,indicating effective wait time for each elements in the list
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
			#elapsed_time=0
			#strt_time=0
			#del wait_list[:]	
			#wait_list.append(2.5)
def lcd_happy_journey():			
			#print "No device in range"
			lcd.clear()
			lcd.cursor_pos =(0,4)
			lcd.write_string(u'Welcome')
			lcd.cursor_pos =(1,0)
			lcd.write_string(u'Happy Journey!!!')
			


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
				#print "Status=",status
				#print wait_list[:]
				if status==True:
					#try poping using wait list
					print"No VALID device found"
					lcd_happy_journey()
								
				else:	
					if q.isEmpty()==True:
						q.enqueue(mac)
						print "Stacked"
						hindi_noti(r[0][0])
						print '\n\n'
						print '**********'
						print "SSID:-",r[0][0],",has arrived!"
						#wait_list.append(e_wait(0,1))

					else:
						q.enqueue(mac)
						#elapsed_time=time.time()-strt_time #update elapsed time
						#i=q.size()
						hindi_noti(r[0][0])
						print "wait list e-wait update"
						print '\n\n'
						print '**********'
						print "SSID:-",r[0][0],",has arrived!"
						#wait_list.append(e_wait(elapsed_time,i)) #update wait list	

			else:			
				no_device_in_range()
									
			list_seek=list_seek+1
		
	except KeyboardInterrupt:
		db.close()
		GPIO.cleanup()
		lcd.clear()

def Main():
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
					list_seek=0
					condition.acquire()
					search(list_len,list_seek)
					condition.notify()
					condition.release()	
					list_seek=0
					del list_mac[:]
				else:
					no_device_in_range()
					print "No device in range"
					lcd_happy_journey()
					
					
						
			except KeyboardInterrupt:
				print "Program terminated unexpetedly"
				lcd.clear()
				GPIO.cleanup()
				exit()	

	
global a
a=0	
def one():
	while(1):
		lock.acquire()
		a=a+1
		print"happy ........... and satisfied\t",a
		lock.release()
		
def two():
	while(1):
		
		print".......... sad ...........\t",a
		
q=Queue()
p=stop_watch()

db = MySQLdb.connect("localhost","root","raspberry","busid" )
t4=threading.Thread(target=one,args=())
t4.start()
t5=threading.Thread(target=two,args=())
t5.start()
#t1=threading.Thread(target=p.count(),args=())
#t1.start()
#t2=threading.Thread(target=q.timed_pop(),args=())
#t2.start()
#t3=threading.Thread(target=Main(),args=())
#t3.start()


print "Check check"
