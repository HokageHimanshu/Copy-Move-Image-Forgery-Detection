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

def find_clusters(clusters,size,key_points):
	cluster_list= [[] for i in range(size)]
	for idx in range(len(key_points)):
	    if clusters.labels_[idx]!=-1:
	        cluster_list[clusters.labels_[idx]].append((int(key_points[idx].pt[0]),int(key_points[idx].pt[1])))
	return cluster_list

def draw_line(cluster_list,manipulated_image):
	for points in cluster_list:
	    if len(points)>1:
	        for idx1 in range(1,len(points)):
	            cv2.line(manipulated_image,points[0],points[idx1],(255,255,255),2)
	return manipulated_image

def find_forgery(original_image,key_points,descriptors,eps=40,min_sample=2):
	clusters=DBSCAN(eps=eps, min_samples=min_sample).fit(descriptors)
	size=np.unique(clusters.labels_).shape[0]-1
	manipulated_image=original_image.copy()
	if (size==0) and (np.unique(clusters.labels_)[0]==-1):
		print('No manipulated_image Found!!')
		# return None
		return manipulated_image
	if size==0:
		size=1
	cluster_list=find_clusters(clusters,size,key_points)
	manipulated_image = draw_line(cluster_list,manipulated_image)
	return manipulated_image