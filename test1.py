import Queue, cv2

_q = Queue.Queue(10)

im = cv2.imread("image.jpg")
print "q size: ", _q.qsize()
_q.put(im)
print "q size: ", _q.qsize()
