import sys

class imageInfo(object):
	"""
		The class contain image & the name
	"""
	imagePtr = None
	imageName = ""

	#constructoion
	def __init__(self, ptr, n):
		imagePtr = ptr
		imageName = n
