import thread, sys
from PCThread import *

programEnd = False;

def PCsConnect():
	"""
		Launch a thread to connect with PC
	"""
	thread.start_new_thread(PCsConnectThread ,("",1))

def PCPhoneConnect():
	"""
		Launch a thread to connect with phone
	"""
	thread.start_new_thread(PCPhoneConnectThread ,("",1))

def fastRcnn():
	"""
		Launch a thread to deal with Fast-Rcnn
	"""
	thread.start_new_thread(fastRcnnThread ,("",1))


if __name__ == "__main__":
	#raise the connection between PCs
	PCsConnect()

	#raise the connection between phone and PC
	PCPhoneConnect()

	#start fast-rcnn
	fastRcnn()

	#keep looping
	while programEnd == False:
		pass

