from sklearn.cluster import DBSCAN
import numpy as np
import cv2

def run_sift_detection(original_image):
    sift = cv2.xfeatures2d.SIFT_create()
    # print('sift is')
    # print(sift)
    gray= cv2.cvtColor(original_image,cv2.COLOR_BGR2GRAY) 
    key_points,descriptors = sift.detectAndCompute(gray, None)
    # print('key_points are ')
    # print(self.key_points)
    # print(self.descriptors)
    # print()
    return key_points,descriptors

def show_sift_features(original_image,key_points,descriptors):
    gray_original_image=cv2.cvtColor(original_image,cv2.COLOR_BGR2GRAY)
    temp_image = original_image.copy()
    sift_original_image=cv2.drawKeypoints(original_image,key_points,temp_image)
    # sift_original_image=cv2.drawMatches(self.original_image,self.key_points,self.original_image.copy())
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
			for idx1 in range(1,n):
				color = (255,255,255)
				line_width = 2
				cv2.line(manipulated_image,points[0],points[idx1],color,line_width)
	return manipulated_image

def find_forgery(original_image,key_points,descriptors,eps=40,min_sample=2):
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
	cluster_list=find_clusters(clusters_formed,size,key_points)
	manipulated_image = draw_line(cluster_list,manipulated_image)
	return manipulated_image