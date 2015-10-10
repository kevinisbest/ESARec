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

def DeepJudgeInitial():
	"""
		Launch a thread to determine deep
	"""
	thread.start_new_thread(DeepJudgeThread ,("",1))


if __name__ == "__main__":
	#raise the connection between PCs
	PCsConnect()

	#raise the connection between phone and PC
	PCPhoneConnect()

	#start fast-rcnn
	DeepJudgeInitial()

	#keep looping
	while programEnd == False:
		pass
	
