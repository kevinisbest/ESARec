#import cv2
import socket
import time

#the info about deep PC
DeepPCPort = 12334

#interrupt judge
isInterrupt1 = False
isInterrupt2 = False

#the info about image
ImageName = "image.jpg"
#BIT_LENGTH = 262144
BIT_LENGTH = 1024

#Command between PCs
START_SEND_IMAGE = "start send image"
START_SEND_LIST = "start send list"
END_SEND_IMAGE = "end send image"
END_SEND_LIST = "end send list"


def PCsConnectThread():
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

	#accept the connection
	print "{ Phone Connect Thread }: wait for connection"
	operateSocket, address = rcnnSocket.accept()
	print "{ Phone Connect Thread }: Conencted to - " + str(address)

	#while isInterrupt:
	twoStateSend(operateSocket)

	operateSocket.close()


def twoStateSend(sock):
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
	ack1 = sock.recv(len(START_SEND_IMAGE))

	#send ACK
	if ack1 == START_SEND_IMAGE:
		sock.send(START_SEND_IMAGE)
	else:
		needToDrop = True

	if needToDrop == False:
		#receive image
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
				break
			fp.write(bitInfo)

		im = cv2.imread("image.jpg")
		cv2.imshow("show", im)
		#cv2.waitKey()
		fp.close()

		#send recv ACK
		sock.send(START_SEND_LIST)

		#receive list
		bitInfo = sock.recv(BIT_LENGTH)
		endInfo = sock.recv(len(END_SEND_LIST))
		ll = PassTransferStringToList(bitInfo)
		print ll


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


if __name__ == "__main__":
	PCsConnectThread()
