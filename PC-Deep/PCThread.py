import socket, Queue
#import cv2, os

#the info about deep PC
DeepPCPort = 12332

#variable to interrupt looping in PCsConnectThread


def PCsConnectThread(non, non2):
	"""
		the PC connect thread function
	"""
	#global
	global DeepPCPort
	global isInterrupt

	#initialize the socket
	rcnnSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	rcnnSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	rcnnSocket.bind(("", DeepPCPort))
	rcnnSocket.listen(1)
	print "{ Phone Connect Thread }: done socket initialization"

	#loop to accept the connection
	while True:
		#accept the connection
		print "{ Phone Connect Thread }: wait for connection"
		operateSocket, address = rcnnSocket.accept()
		print "{ Phone Connect Thread }: Conencted to - " + str(address)

		while isInterrupt:
			2StateAccept(operateSocket)

		operateSocket.close()

def 2StateAccept(sock):
	pass


def PCPhoneConnectThread(non, non2):
	"""
		the phone connect thread function
	"""
	pass

def DeepJudgeThread(non, non2):
	"""
		the thread to determine deep
	"""
	pass
