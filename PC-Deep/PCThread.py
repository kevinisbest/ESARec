import socket, Queue
import cv2, os

#the info about deep PC
DeepPCPort = 12332

#variable to interrupt looping in PCsConnectThread
isInterrupt = True

#queue
imageQueue = []
DeepQueue = []

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
			twoStateAccept(operateSocket)

		operateSocket.close()

def twoStateAccept(sock):
	"""
		test to accept image
		input	=> socket
	"""
	global BIT_LENGTH
	global START_SEND_IMAGE
	global START_SEND_LIST
	global END_SEND_IMAGE
	global END_SEND_LIST
	needToDrop = False


	#receive request
	ack1 = sock.recv(BIT_LENGTH)


	#send ACK
	if ack1.find(START_SEND_IMAGE) != -1:
		sock.send(START_SEND_IMAGE)
		print "{ PC Connect Thread }: Receive Correct Request(IMGE)"
	else:
		needToDrop = True
		print "{ PC Connect Thread }: Receive Wrong Request !!!(IMGE)"


	#receive image(if accept correct request)
	if needToDrop == False:
		print "{ PC Connect Thread }: Start Receiving"
		fp = open("image.jpg", 'w')

		#set timeout
		sock.settimeout(0.1)
		while True:
			try:
				bitInfo = sock.recv(BIT_LENGTH)
			except timeout:
				break

			#check close
			endString = bitInfo[len(bitInfo)-len(END_SEND_IMAGE):]
			elseString = bitInfo[:len(bitInfo)-len(END_SEND_IMAGE)]
			print endString
			if endString == END_SEND_IMAGE:
				print endString
				fp.write(elseString)
				break
			fp.write(bitInfo)

		print "{ PC Connect Thread }: Receiving Done"
		im = cv2.imread("image.jpg")
		#cv2.waitKey()
		imageQueue.put(im)
		fp.close()

		#send recv ACK
		sock.send(START_SEND_LIST)

		#receive list
		bitInfo = sock.recv(BIT_LENGTH)
		endInfo = sock.recv(BIT_LENGTH)
		ll = PassTransferStringToList(bitInfo)
		print ll
		DeepQueue.put(ll)
		print "{ PC Connect Thread }: Complete All Step"			


	#recover timeout
	sock.settimeout(None)


def PassTransferListToString(ll):
	"""
		the function that can convert list to string(Socket Use)
		input	=> list
		output	=> string
	"""
	string = ""
	for i in ll:
		string += str(i)
		string += ","
	return string


def PassTransferStringToList(ss):
	"""
		the function that can convert string to list(Socket Use)
		input	=> string
		output	=> list
	"""
	ll = []
	curr = 0
	prev = 0
	for i in ss:
		if i == ',':
			sub = ss[prev:curr]
			ll.append(sub)
			prev = curr+1
		curr += 1
	return ll


def PCPhoneConnectThread(non, non2):
	"""
		the phone connect thread function
	"""
	pass

def DeepJudgeThread(non, non2):
	"""
		the thread to determine deep
	"""
	#global
	global isInterrupt

	while True:
		if imageQueue.qsize() != 0 and DeepQueue.qsize() != 0:
			im = imageQueue.get()
			cv2.imshow("show", im)
			print DeepQueue.get()



