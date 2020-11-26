import sys
import cv2
from CMFDetection import ForgeryDetector
import re
from datetime import datetime


print('Welcome to the Copy Move original_image manipulated_image Detection Application!\n')
choice = 'y'
while choice.lower() == 'y':
	fname  = input('\nEnter the path/name of the original_image = ')
	fname = fname.rstrip()
	assert(fname!="")

	original_image=cv2.imread(fname)
	# print(original_image)
	# print(original_image.shape)

	if original_image is None:
		print('File path/name entered by you is ',fname,'\nKindly enter a valid file path')
		sys.exit(0)

	# eps is in range of (0,500)
	# min_sample is in range of (0,50)

	eps =60
	min_samples=2


	eps = int(input('Enter value of eps (0,500) or 60 for default value = '))
	min_samples = int(input('Enter value of minimum no of samples (0,50) or 2 for default value = '))


	print('\nStarting the process of detecting manipulated_image with parameter values as the following')
	print('Eps = ',eps)
	print('minimum no. of samples = ',min_samples)

	forgery_finder=ForgeryDetector(original_image)

	key_points,descriptors = forgery_finder.run_sift_detection()

	manipulated_image=forgery_finder.find_forgery(eps,min_samples)

	if manipulated_image is None:
		sys.exit(0)

	cv2.imwrite('Original.jpg', original_image) 
	cv2.imwrite('Forged.jpg', manipulated_image) 

	cv2.imshow('Original original_image',original_image)
	cv2.imshow('manipulated_image',manipulated_image)
	cv2.imshow('SIFT features',forgery_finder.show_sift_features())

	wait_time=10000
	keyCode = cv2.waitKey(wait_time)
	cv2.destroyAllWindows()
	choice = input('Enter (y/Y) to continue = ')
	# if choice.lower()=='y':
	# 	continue
	# else:
		
	# while(cv2.getWindowProperty('manipulated_image', 0) >= 0) or (cv2.getWindowProperty('Original original_image', 0) >= 0) :
	# 	keyCode = cv2.waitKey(wait_time)
	# 	if (keyCode) == ord('q') or keyCode==ord('Q'):
	# 		cv2.destroyAllWindows()
	# 		break
	# 	elif keyCode == ord('s') or keyCode ==ord('S'):
	# 		name=re.findall(r'(.+?)(\.[^.]*$|$)',fname)
	# 		date=datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
	# 		new_fname=name[0][0]+'_'+str(eps)+'_'+str(min_samples)
	# 		new_fname=new_fname+'_'+date+name[0][1]
	# 		PrintBoundary()
			
	# 		vaue=cv2.imwrite(new_fname,manipulated_image)
	# 		print('original_image Saved as....',new_fname)