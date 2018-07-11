import threading, time

def fun_one():
	i=0
	while(1):
		print "\n",i
		i=i+1

def fun_two():
	i=0
	while(1):
		print "\n\t\t\t\tHappy",i
		#time.wait(1)
		i=i+1

t1 = threading.Thread(target=fun_one)
t2 = threading.Thread(target=fun_two)

print("abcd")
t1.start()
t2.start()
'''
a=100
while (a<400):
	print "\n\t\t",a
	a=a+1
	if(a==175):
		t2.start()
	'''	


