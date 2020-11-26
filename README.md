Purpose of Project - DBSCAN-Copy-Move-Foregry-Detection

Summary: Copy move manipulated_image detection using DBSCAN clustering algorithm.

Requirements:
* Python3
* OpenCV (pip install opencv-python==3.4.2.16)
* OpenCV-contrib-python  (pip install opencv-contrib-python==3.4.2.16)
* Sklearn (pip install -U scikit-learn)


Type this command in the terminal. (See examples for complete idea)

`python main.py "path to the original_image" eps min_samples`
* (Mandatory) "path to the original_image" - this is the exact path to the original_image file (See examples).
* (Optional) eps - Eps value for DBSCAN algorithm. Increasing this will generate more clusters.(Value should be between 0-500)
* (Optional) min_samples - Min sample for DBSCAN algorithm. Increasing this will reduce clusters.(Value should be between 0-50).
