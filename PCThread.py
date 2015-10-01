import socket, Queue
import cv2
import demo

#the info about deep PC
DeepPCAddress = "192.168.1.0"
DeepPCPort = 12332

#the info about phone
PhonePort = 10017

#the info about image
ImageName = "image.jpg"

#queue
_q = Queue.Queue(10)


def PCsConnectThread(non, non2):
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

	#connect to deep PC
	try:
		print "{ PC Connect Thread }: try to connect to Deep PC..."
		pcSocket.connect((DeepPCAddress, DeepPCPort))
		print "{ PC Connect Thread }: Successfully connect to Deep PC!"
	except:
		print "destination error, check if the address or port wrong..."

	#run

	#done
	pcSocket.close()


def PCPhoneConnectThread(non, non2):
	"""
		the phone connect thread function
	"""
	#global
	global PhonePort

	#initialize the socket
	phoneSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	phoneSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	phoneSocket.bind(("", PhonePort))
	phoneSocket.listen(1)
	print "{ Phone Connect Thread }: done socket initialization"

	#loop to accept the image
	while True:
		#accept the connection
		print "{ Phone Connect Thread }: wait for connection"
		operateSocket, address = phoneSocket.accept()
		print "{ Phone Connect Thread }: Conencted to - " + str(address)

		#create a file
		fp = open(ImageName, "w");

		#receive the info
		while True:
			bitInfo = operateSocket.recv(BIT_LENGTH)

			#check if the bitinfo is error
			if not bitInfo:
				break
			fp.write(bitInfo)

		#receive done
		print "{ Phone Connect Thread }: receive done"

		#put image into queue
		im = imread(ImageName)
		_q.put(im)
		print "{ Phone Connect Thread }: put image into queue"

		fp.close()
		operateSocket.close()


def fastRcnnThread(non, non2):
	"""
		The thread function to conduct Fast-Rcnn
	"""
	while True:
		if not _q.full():
			#conduct demo.py
			pass
		im = _q.get()

