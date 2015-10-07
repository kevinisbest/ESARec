import socket, Queue
import cv2, os
import demo
from FastRCNN import *
import _init_paths
from fast_rcnn.config import cfg
import caffe
import scipy.io as sio
import time

#the info about deep PC
DeepPCAddress = "192.168.1.0"
DeepPCPort = 12332

#the info about phone
PhonePort = 10017

#the info about image
ImageName = "image.jpg"
#BIT_LENGTH = 262144
BIT_LENGTH = 1024

#queue
_q = Queue.Queue(10)
__q = Queue.Queue(10)

#interrupt judge
isInterrupt1 = False
isInterrupt2 = False


#TCP error limit
TCPErrorMax = 1000000

#threshhold run RCNN
canRun = False

#Fast-RCNN class name and net name
CLASSES = ('__background__',
           'aeroplane', 'bicycle', 'bird', 'boat',
           'bottle', 'bus', 'car', 'cat', 'chair',
           'cow', 'diningtable', 'dog', 'horse',
           'motorbike', 'person', 'pottedplant',
           'sheep', 'sofa', 'train', 'tvmonitor')

NETS = {'vgg16': ('VGG16',
                  'vgg16_fast_rcnn_iter_40000.caffemodel'),
        'vgg_cnn_m_1024': ('VGG_CNN_M_1024',
                           'vgg_cnn_m_1024_fast_rcnn_iter_40000.caffemodel'),
        'caffenet': ('CaffeNet',
                     'caffenet_fast_rcnn_iter_40000.caffemodel')}


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

	#while loop to continue
	while True:
		#connect to deep PC
		try:
			print "{ PC Connect Thread }: try to connect to Deep PC..."
			pcSocket.connect((DeepPCAddress, DeepPCPort))
			print "{ PC Connect Thread }: Successfully connect to Deep PC!"

			#keep operate
			while isInterrupt2:
				2StateSend(pcSocket)

		except:
			print "destination error, check if the address or port wrong..."
			time.sleep(2)


	#done
	pcSocket.close()


def 2StateSend(sock):
	"""
	"""
	pass


def PCPhoneConnectThread(non, non2):
	"""
		the phone connect thread function
	"""
	#global
	global PhonePort
	global isInterrupt1


	#initialize the socket
	phoneSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	phoneSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	phoneSocket.bind(("", PhonePort))
	phoneSocket.listen(1)
	print "{ Phone Connect Thread }: done socket initialization"

	#loop to accept the image
	while True:
		#initialize
		isInterrupt1 = False

		#accept the connection
		print "{ Phone Connect Thread }: wait for connection"
		operateSocket, address = phoneSocket.accept()
		print "{ Phone Connect Thread }: Conencted to - " + str(address)

		#keep receive the info
		while not isInterrupt1:
			print "{ Phone Connect Thread }: wait for command"
			#check if want to send image
			if checkCommand(operateSocket) == "IMAGEA":
				#receive image
				print "wait ACK"
				#operateSocket.send("IMAGE2")
				receiveImageProcess(operateSocket)

		operateSocket.close()


def fastRcnnThread(non, non2):
	"""
		The thread function to conduct Fast-Rcnn
	"""
	#global
	global canRun


	#import the object protocol file and caffe model
	prototxt = os.path.join(cfg.ROOT_DIR, 'models', NETS	['caffenet'][0], 'test.prototxt')
	caffemodel = os.path.join(cfg.ROOT_DIR, 'data', 'fast_rcnn_models', NETS['caffenet'][1])

	#set GPU & build the CNN net
	caffe.set_mode_gpu()
	net = caffe.Net(prototxt, caffemodel, caffe.TEST)

	# Load pre-computed Selected Search object proposals
	box_file = os.path.join(cfg.ROOT_DIR, 'mat', 'rootBoxes.mat')
	obj_proposals = sio.loadmat(box_file)['boxes']


	while True:
		if not _q.empty():
			canRun = True
		if canRun:
			if not _q.empty():
				im = _q.get()

			if not _q.full():
				posLine = FastRCNN(im, net, obj_proposals)
				print posLine

			if _q.empty():
				canRun = False
			


def receiveImageProcess(sock):
	"""
		The function to receive the Image
		Input	=> socket
	"""
	#global
	global BIT_LENGTH
	global ImageName
	global TCPErrorMax

	#create a file
	fp = open(ImageName, "w");

	#receive the info
	errorTime = 0;
	print "{ Phone Connect Thread }: start to receive image"
	sock.setblocking(True)
	sock.settimeout(1)
	while True:
		try:
			bitInfo = sock.recv(BIT_LENGTH)
		except timeout:
			print 'time-out. Judge as end transferring!'
			break

		
		#check if the bitinfo is error
		#if not bitInfo:
		print "bitInfo: ", bitInfo
		#	break
		

		#check if receive end command
		
		endString = str( bitInfo[ len(bitInfo)-6 : len(bitInfo) ] )
		elseString = bitInfo[:len(bitInfo)-6]
		if endString == "IMAGEC":
			print "image end"
			fp.write(elseString)
			break
		
		fp.write(bitInfo)

	#receive done
	print "{ Phone Connect Thread }: receive done"

	#put image into queue
	im = cv2.imread(ImageName)
	_q.put(im)
	print "{ Phone Connect Thread }: put image into queue"

	#recover the block mode
	sock.settimeout(None)

	fp.close()

def checkCommand(sock):
	"""
		receive the command and change it into string
		input	=> socket
		output	=> command string
	"""
	#global
	global BIT_LENGTH
	global isInterrupt1

	#receive the command
	command = sock.recv(BIT_LENGTH)
	print command
	if command == "":
		print "interrupt!"
		isInterrupt1 = True

	#check if it's command
	if len(command) == 6:
		print command
		return str(command)
	else:
		return command
	
