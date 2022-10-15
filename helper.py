import cv2
import numpy as np

font = cv2.FONT_HERSHEY_SIMPLEX
org = (50, 50)
fontScale = 1
color = (255, 0, 0)
thickness = 2

def process_landmark(landmark):
	# print("landmark", (landmark[8]))
	return 

def compute_distance(curr, target):
	# Compute the distance between two points
	return np.sqrt((target.x-curr.x)**2 + (target.y-curr.y)**2 + (target.z - curr.z)**2)

def store_new_pose(landmark, key, stored_keys):
	# Store the new mapping of a key to a pose in the stored_keys dictionary
	stored_keys[key] = landmark

def search_hand_pose(landmark, stored_keys):
	"""
	Search if this landmark is a hand pose we should be detecting.
	
	Expects landmark to be given as relative positions.
	"""
	max_dist = 0.02

	for key in stored_keys:
		works = True
		for i in [4,8,12,16,20]:
			print(compute_distance(stored_keys[key][i], landmark[i]))
			if (compute_distance(stored_keys[key][i], landmark[i]) > max_dist):
				works = False
				break
		if works:
			return "Matching key found: " + key
	
	return "No matches found"

def search_face_pose(landmark, stored_keys):
	"""
	Search if this landmark is a face pose we should be detecting
	
	Expects
	
	"""
	max_dist = 0.02

	for key in stored_keys:
		works = True
		for i in [4,8,12,16,20]:
			print(compute_distance(stored_keys[key][i], landmark[i]))
			if (compute_distance(stored_keys[key][i], landmark[i]) > max_dist):
				works = False
				break
		if works:
			return "Matching key found: " + key
	
	return "No matches found"

	