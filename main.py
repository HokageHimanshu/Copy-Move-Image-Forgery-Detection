import cv2
from CMFDetection import *
from sklearn.cluster import DBSCAN
import numpy as np
import cv2
from datetime import datetime
import math
import matplotlib.pyplot as plt
import numpy as np

def perform_cmfd(fname,original_image,eps,min_samples,wait_time,saveit=False,showit=False):
	key_points,descriptors = run_sift_detection(original_image)

	manipulated_image=find_forgery(original_image,key_points,descriptors,eps,min_samples)

	if manipulated_image is None:
		sys.exit(0) 
	if saveit:
		save_images(original_image,manipulated_image,fname)

	# wait_time=15000
	if showit:
		cv2.imshow('Original original_image',original_image)
		cv2.imshow('manipulated_image',manipulated_image)
		cv2.imshow('SIFT features',show_key_features(original_image,key_points,descriptors))
		keyCode = cv2.waitKey(wait_time)
		cv2.destroyAllWindows()
	return (original_image,manipulated_image)

def format_name(fname):
	return fname.split('/')[1].split('.')[0]

def save_images(original_image,manipulated_image,fname):
	fname = format_name(fname)
	cv2.imwrite('Original'+fname+'.jpg', original_image) 
	cv2.imwrite('Forged'+fname+'.jpg', manipulated_image)

def read_image():
	fname  = input('\nEnter the path/name of the original_image = ')
	fname = fname.rstrip()
	assert(fname!="")

	original_image=cv2.imread(fname)
	# print(original_image)
	# print(original_image.shape)

	if original_image is None:
		print('File path/name entered by you is ',fname,'\nKindly enter a valid file path')
		sys.exit(0)
	return (fname,original_image)

def convert_image_dimensions(image):
	return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# n,m,o = image.shape
	# return image[:,:,1].reshape(n,m)

def test_cmfd(original_image,eps_list,min_samples_list,wait_time,fname):
	# eps_list = [60,100,400]
	# min_samples_list=[2,5,20]
	# wait_time=15000
	titles = ['Original Image'] 
	images = [convert_image_dimensions(original_image)]
	for eps in eps_list:
		for min_samples in min_samples_list:
			# eps = int(input('Enter value of eps (0,500) or 60 for default value = '))
			# min_samples = int(input('Enter value of minimum no of samples (0,50) or 2 for default value = '))
			# print('\nStarting the process of detecting manipulated_image with parameter values as the following')
			print('\nRunning sift algo for')
			print('Eps = ',eps)
			print('minimum no. of samples = ',min_samples)
			original_image,manipulated_image = perform_cmfd(fname,original_image,eps,min_samples,wait_time,saveit=False,showit=False)
			titles.append('FI_eps='+str(eps)+'_minsamples='+str(min_samples))
			images.append(convert_image_dimensions(manipulated_image))
	plot_graph(titles,images,fname)

def plot_graph(titles,images,fname):
	n = len(images)
	nrows = math.ceil(math.sqrt(n))
	ncols = math.ceil(n/nrows)
	x = range(10)
	y = range(10)
	fig, ax = plt.subplots(nrows=nrows, ncols=ncols)
	index =0
	for r in ax:
	    for c in r:
	    	c.axis('off')
	    	if index<n:
		        c.imshow(images[index])
		        c.set_title(titles[index],size=5)
		        # c.text(0.5,-0.1,titles[index], size=10, ha="center")
		        # c.axis('off')
		        index+=1
		    # c.axis('off')
	fname = format_name(fname)
	plt.savefig('analysis_'+fname+'.png')
	plt.show()


print('Welcome to the Copy Move original_image manipulated_image Detection Application!\n')
choice = 'y'
while choice.lower() == 'y':
	print('MENU - ')
	print('1. Apply CMFD for one image')
	print('2. Test CMFD for eps and min_samples')
	menu_option = int(input('Enter your option (1/2): '))
	if menu_option==1:
		fname,original_image = read_image()

		eps =60
		min_samples=2
		wait_time=15000

		eps = int(input('Enter value of eps (0,500) or 60 for default value = '))
		min_samples = int(input('Enter value of minimum no of samples (0,50) or 2 for default value = '))

		print('\nStarting the process of detecting manipulated_image with parameter values as the following')
		print('Eps = ',eps)
		print('minimum no. of samples = ',min_samples)

		original_image,manipulated_image = perform_cmfd(fname,original_image,eps,min_samples,wait_time,saveit=True,showit=True)

	elif menu_option==2:
		eps_list = [60,100,200]
		min_samples_list=[2,5,10,45]
		wait_time=15000
		fname, original_image = read_image()
		test_cmfd(original_image,eps_list,min_samples_list,wait_time,fname)
	else:
		print('Invalid Option entered')
	choice = input('\nEnter (y/Y) to continue = ')