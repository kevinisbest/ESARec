import cv2, socket
import time

#the info about deep PC
DeepPCAddress = "192.168.1.131"
DeepPCPort = 12334

#the info about image
ImageName = "image.jpg"
#BIT_LENGTH = 262144
BIT_LENGTH = 1024

#Command between PCs
START_SEND_IMAGE = "start send image"
START_SEND_LIST = "start send list"
END_SEND_IMAGE = "end send image"
END_SEND_LIST = "end send list"

def PCsConnectThread(im):
	"""
		the PC connect thread function
	"""
	#global
	global DeepPCAddress
	global DeepPCPort

	#initialize the socket
	pcSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	pcSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	print "{ PC Connect Thread }: done socket initialization"

	#while loop to continue
	#while True:
		#connect to deep PC
	try:
		print "{ PC Connect Thread }: try to connect to Deep PC..."
		pcSocket.connect((DeepPCAddress, DeepPCPort))
		print "{ PC Connect Thread }: Successfully connect to Deep PC!"

		#keep operate
		#while True:
		twoStateSend(pcSocket, im)

	except:
		print "destination error, check if the address or port wrong..."
		time.sleep(2)


	#done
	pcSocket.close()

def twoStateSend(sock, im):
	"""
		the function send image and the list of position saries
		input	=> socket
	"""
	#global
	global START_SEND_IMAGE
	global START_SEND_LIST
	global END_SEND_IMAGE
	global END_SEND_LIST
	global BIT_LENGTH
	needToDrop = False
	print "!"	
	
	#send request
	sock.send(START_SEND_IMAGE)
	print "!"
	#receive ACK
	ack1 = sock.recv(len(START_SEND_IMAGE))
	if ack1 == START_SEND_IMAGE:
		needToDrop = False
	else:
		needToDrop = True

	print "!"
	#send image
	if needToDrop == False:
		while True:
			bitInfo = im.read(BIT_LENGTH)
			if not bitInfo:
				break
			sock.send(bitInfo)
		print "{ PC Connect Thread }: Transfer Image Done."

		#send end msg
		sock.send(END_SEND_IMAGE)

		#receive ACK
		ack1 = sock.recv(len(START_SEND_IMAGE))
		if ack1 == START_SEND_LIST:
			needToDrop = False
		else:
			needToDrop = True

		#send list
		if needToDrop == False:
			print "complete!!!"

		#send end msg

if __name__ == "__main__":
	im = open("000004.jpg", 'r')
	PCsConnectThread(im)
	
	
