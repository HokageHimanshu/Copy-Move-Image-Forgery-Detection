from sklearn.cluster import DBSCAN
import numpy as np
import cv2


def single_channel_image(original_image):
	image_color = cv2.COLOR_BGR2GRAY
	gray_image= cv2.cvtColor(original_image,image_color) 
	return gray_image

def run_sift_detection(original_image):
    sift = cv2.xfeatures2d.SIFT_create()
    gray_image=  single_channel_image(original_image)
    keypts,descriptors = sift.detectAndCompute(gray_image, None)
    return keypts,descriptors

def mark_keypts(original_image,keypts,copy_image):
	# radius = 2
	sift_transformed_image = cv2.drawKeypoints(original_image,keypts,copy_image)
	return sift_transformed_image

def show_key_features(original_image,keypts,descriptors):
	gray_original_image=single_channel_image(original_image)
	temp_image = original_image.copy()
	sift_original_image= mark_keypts(original_image,keypts,temp_image)
	return sift_original_image

def find_clusters(clusters,size,keypts):
	cluster_list= [[] for i in range(size)]
	n = len(keypts)
	for idx in range(n):
		index = clusters.labels_[idx]
		if index != -1:
			pt1 = keypts[idx].pt[0]
			pt2 = keypts[idx].pt[1]
			cluster_list[index].append((int(pt1),int(pt2)))
	return cluster_list

def draw_line(cluster_list,manipulated_image):
	for points in cluster_list:
		n = len(points)
		if n >1:
			starting_point = points[0]
			for idx1 in range(1,n):
				for idx2 in range(1,n):
					color = (255,255,255)
					line_width = 2
					end_point = points[idx1]
					cv2.line(manipulated_image,starting_point,end_point,color,line_width)
	return manipulated_image

def find_forgery(original_image,keypts,descriptors,eps=40,min_sample=2):
	dbscaner = DBSCAN(min_samples=min_sample,eps=eps)
	manipulated_image=original_image.copy()
	clusters_formed=dbscaner.fit(descriptors)
	size=np.unique(clusters_formed.labels_).shape[0]
	size = size-1
	if (size==0):
		if (np.unique(clusters_formed.labels_)[0]==-1):
			print('No Manipulation is found in the image!!')
			return manipulated_image
	if size==0:
		size=1
	cluster_list=find_clusters(clusters_formed,size,keypts)
	manipulated_image = draw_line(cluster_list,manipulated_image)
	return manipulated_image