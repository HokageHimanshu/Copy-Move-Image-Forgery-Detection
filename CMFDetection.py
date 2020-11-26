from sklearn.cluster import DBSCAN
import numpy as np
import cv2

class ForgeryDetector(object):

	def __init__(self, original_image):
		self.original_image = original_image
		self.key_points = None
		self.descriptors = None

	def run_sift_detection(self):
	    sift = cv2.xfeatures2d.SIFT_create()
	    # print('sift is')
	    # print(sift)
	    gray= cv2.cvtColor(self.original_image,cv2.COLOR_BGR2GRAY) 
	    self.key_points,self.descriptors = sift.detectAndCompute(gray, None)
	    # print('key_points are ')
	    # print(self.key_points)
	    # print(self.descriptors)
	    # print()
	    return self.key_points,self.descriptors

	def show_sift_features(self):
	    gray_original_image=cv2.cvtColor(self.original_image,cv2.COLOR_BGR2GRAY)
	    sift_original_image=cv2.drawKeypoints(self.original_image,self.key_points,self.original_image.copy())
	    # sift_original_image=cv2.drawMatches(self.original_image,self.key_points,self.original_image.copy())
	    return sift_original_image
		
	def find_forgery(self,eps=40,min_sample=2):
		clusters=DBSCAN(eps=eps, min_samples=min_sample).fit(self.descriptors)
		size=np.unique(clusters.labels_).shape[0]-1
		manipulated_image=self.original_image.copy()
		if (size==0) and (np.unique(clusters.labels_)[0]==-1):
			print('No manipulated_image Found!!')
			return None
		if size==0:
			size=1
		cluster_list= [[] for i in range(size)]
		for idx in range(len(self.key_points)):
		    if clusters.labels_[idx]!=-1:
		        cluster_list[clusters.labels_[idx]].append((int(self.key_points[idx].pt[0]),int(self.key_points[idx].pt[1])))
		for points in cluster_list:
		    if len(points)>1:
		        for idx1 in range(1,len(points)):
		            cv2.line(manipulated_image,points[0],points[idx1],(0,255,0),2)
		return manipulated_image