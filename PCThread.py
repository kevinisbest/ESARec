import socket, Queue
import cv2
import demo
from FastRCNN import *
import _init_paths
#from fast_rcnn.config import cfg


#the info about deep PC
DeepPCAddress = "192.168.1.0"
DeepPCPort = 12332

#the info about phone
PhonePort = 10017

#the info about image
ImageName = "image.jpg"
BIT_LENGTH = 65536

#queue
_q = Queue.Queue(10)

#interrupt judge
isInterrupt = False

#TCP error limit
TCPErrorMax = 1000000


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
	global isInterrupt


	#initialize the socket
	phoneSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	phoneSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	phoneSocket.bind(("", PhonePort))
	phoneSocket.listen(1)
	print "{ Phone Connect Thread }: done socket initialization"

	#loop to accept the image
	while True:
		#initialize
		isInterrupt = False

		#accept the connection
		print "{ Phone Connect Thread }: wait for connection"
		operateSocket, address = phoneSocket.accept()
		print "{ Phone Connect Thread }: Conencted to - " + str(address)

		#keep receive the info
		while not isInterrupt:
			print "{ Phone Connect Thread }: wait for command"
			#check if want to send image
			if checkCommand(operateSocket) == "0100":
				#receive image
				receiveImageProcess(operateSocket)

		operateSocket.close()


def fastRcnnThread(non, non2):
	"""
		The thread function to conduct Fast-Rcnn
	"""

"""
	#import the object protocol file and caffe model
	prototxt = os.path.join(cfg.ROOT_DIR, 'models', NETS	[args.demo_net][0], 'test.prototxt')
    caffemodel = os.path.join(cfg.ROOT_DIR, 'data', 'fast_rcnn_models', NETS[args.demo_net][1])

	#set GPU & build the CNN net
	caffe.set_mode_gpu()
	net = caffe.Net(prototxt, caffemodel, caffe.TEST)

	# Load pre-computed Selected Search object proposals
    box_file = os.path.join(cfg.ROOT_DIR, 'mat', 'rootBoxes.mat')
    obj_proposals = sio.loadmat(box_file)['boxes']


	while True:
		if not _q.empty():
			im = _q.get()

		if not _q.full():
			FastRCNN(im, net, obj_proposals)
	"""		


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
	while True:
		bitInfo = checkCommand(sock)

		
		#check if the bitinfo is error
		if not bitInfo:
			print "bitInfo: ", bitInfo
			break
		

		#check if receive end command
		endString = str( bitInfo[ len(bitInfo)-4 : len(bitInfo) ] )
		elseString = bitInfo[:len(bitInfo)-4]
		if endString == "0101":
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

	fp.close()

def checkCommand(sock):
	"""
		receive the command and change it into string
		input	=> socket
		output	=> command string
	"""
	#global
	global BIT_LENGTH
	global isInterrupt

	#receive the command
	command = sock.recv(BIT_LENGTH)
	#print command
	if command == "":
		print "interrupt!"
		isInterrupt = True

	#check if it's command
	if len(command) == 4:
		print command
		return str(command)
	else:
		return command
	
