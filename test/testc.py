#import cv2
import socket
import time

#the info about deep PC
DeepPCAddress = "192.168.0.102"
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

def PCsConnectThread(im, _l):
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
		twoStateSend(pcSocket, im, _l)

	except:
		print "destination error, check if the address or port wrong..."
		time.sleep(2)


	#done
	pcSocket.close()

def twoStateSend(sock, im, _l):
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

	
	#send request
	sock.send(START_SEND_IMAGE)
	print "{ PC Connect Thread }: Send Request(IMGE)"

	#receive ACK
	ack1 = sock.recv(BIT_LENGTH)
	if ack1.find(START_SEND_IMAGE) != -1:
		needToDrop = False
		print "{ PC Connect Thread }: Receive Correct ACK(IMGE)"
	else:
		needToDrop = True
		print "{ PC Connect Thread }: Receive Wrong ACK !!!(IMGE)"


	#send image(if accept correct ACK)
	if needToDrop == False:
		print "{ PC Connect Thread }: Start Transferring(IMGE)"
		while True:
			bitInfo = im.read(BIT_LENGTH)
			if not bitInfo:
				break
			sock.send(bitInfo)
		print "{ PC Connect Thread }: Transfer Image Done"

		#send end msg
		sock.send(END_SEND_IMAGE)

		#receive ACK
		ack1 = sock.recv(BIT_LENGTH)
		if ack1.find(START_SEND_LIST) != -1:
			needToDrop = False
			print "{ PC Connect Thread }: Receive Correct ACK(LIST)"
		else:
			needToDrop = True
			print "{ PC Connect Thread }: Receive Wrong ACK !!!(LIST)"

		#send list
		if needToDrop == False:
			_s = PassTransferListToString(_l)
			sock.send(_s)

			#send end msg
			sock.send(END_SEND_LIST)
			print "{ PC Connect Thread }: Complete All Step"			
		else:
			print "{ PC Connect Thread }: Wrong ACK, Next Step...(LIST)"


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
	im = open("000004.jpg", 'r')
	_l = ['h', 'i', 12.345, 16.789]
	PCsConnectThread(im, _l)
	
	
