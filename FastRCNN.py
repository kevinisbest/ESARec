def FastRCNN(im, net, obj_proposals):
	"""
		Fast R-CNN main function
		input	=> image fileptr
		output	=> ??
	"""
	# Detect all object classes and regress object bounds
	timer = Timer()
	timer.tic()
	scores, boxes = im_detect(net, im, obj_proposals)
	timer.toc()
	print ('Detection took {:.3f}s for ' '{:d} object proposals').format(timer.total_time, boxes.shape[0])

	# Visualize detections for each class
	CONF_THRESH = 0.6
	NMS_THRESH = 0.3
	for cls in classes:
		cls_ind = CLASSES.index(cls)
		cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
		cls_scores = scores[:, cls_ind]
		keep = np.where(cls_scores >= CONF_THRESH)[0]
		cls_boxes = cls_boxes[keep, :]
		cls_scores = cls_scores[keep]
		dets = np.hstack((cls_boxes, cls_scores[:, np.newaxis])).astype(np.float32)
		keep = nms(dets, NMS_THRESH)
		dets = dets[keep, :]
		print 'All {} detections with p({} | box) >= {:.1f}'.format(cls, cls,
                                                                    CONF_THRESH)
		vis_detections(im, cls, dets, thresh=CONF_THRESH)

def vis_detections(im, class_name, dets, thresh=0.5):
	"""Draw detected bounding boxes."""
	inds = np.where(dets[:, -1] >= thresh)[0]
	if len(inds) == 0:
		return

	im = im[:, :, (2, 1, 0)]
	fig, ax = plt.subplots(figsize=(12, 12))
	ax.imshow(im, aspect='equal')
	for i in inds:
		bbox = dets[i, :4]
		score = dets[i, -1]

		ax.add_patch(plt.Rectangle((bbox[0], bbox[1]), bbox[2] - bbox[0], bbox[3] - bbox[1], fill=False, edgecolor='red', linewidth=3.5))
		ax.text(bbox[0], bbox[1] - 2, '{:s} {:.3f}'.format(class_name, score), bbox=dict(facecolor='blue', alpha=0.5), fontsize=14, color='white')

    ax.set_title(('{} detections with '
		'p({} | box) >= {:.1f}').format(class_name, class_name, thresh), fontsize=14)
	plt.axis('off')
	plt.tight_layout()
	plt.draw()
