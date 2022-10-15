import cv2
import numpy as np
import matplotlib.pyplot as plt

font = cv2.FONT_HERSHEY_SIMPLEX
org = (50, 50)
fontScale = 1
color = (255, 0, 0)
thickness = 2

def process_landmark(landmark):
	# print("landmark", (landmark[8]))
	return 

# fig = plt.figure()
# ax = plt.axes(projection='3d')
def plot_realtime(landmarks):
	x = []
	y = []
	z = []
	for landmark in landmarks:
		x.append(landmark.x)
		y.append(landmark.y)
		z.append(landmark.z)
	# ax.plot3D(x,y,z)
	print(x)
	plt.show(block=False)

def check_mouth_open(landmarks):
	return (landmarks[14].y - landmarks[13].y) > 0.5

def check_jump(landmarks, reference):
	vertical_threshold = 0.1 # If there is a vertical increase by 0.1m, then we consider this a jump
	# TODO: I don't know how this thresholding works, because being close and far from the camera plays a difference
	# return (landmarks[i].y - landmarks[j].y) > vertical_treshold
	return None

def compute_distance(curr, target):
	# Compute the distance between two points
	return np.sqrt((target.x-curr.x)**2 + (target.y-curr.y)**2 + (target.z - curr.z)**2)

def compute_relative_distance(curr, target, curr_reference, target_reference):
	"""
	This is in the case for face, where we need to first compute the relative distance.
	"""
	x = (target.x - target_reference.x) - (curr.x - curr_reference.x)
	y = (target.y - target_reference.y) - (curr.y - curr_reference.y)
	z = (target.z - target_reference.z) - (curr.z - curr_reference.z)

	return np.sqrt(x**2 + y**2 + z**2)

def store_new_pose(landmark, key, stored_keys):
	# Store the new mapping of a key to a pose in the stored_keys dictionary
	stored_keys[key] = landmark

def search_hand_pose(landmark, stored_keys):
	"""
	Search if this landmark is a hand pose we should be detecting.
	
	Expects landmark to be given as relative positions.
	"""
	max_dist = 0.03

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
	
	
	145 - 159 -> left eye (opening / closing)
	374 - 386 -> right eye (opening / closing)
	13 - 14 -> Mouth (opening closing)
	
	This doesn't work super well, we might actually need haars-cascade.

	"""
	max_dist = 0.04

	for key in stored_keys:
		works = True
		for i in [[145, 159], [374, 386], [13, 14]]: #https://google.github.io/mediapipe/solutions/face_mesh.html
			dist = compute_relative_distance(stored_keys[key][i[1]], landmark[i[1]], stored_keys[key][i[0]], landmark[i[0]])
			print(dist)
			if (dist > max_dist):
				works = False
				break
		if works:
			return "Matching key found: " + key
	
	return "No matches found"

def search_body_pose(landmark, stored_keys):
	# print(landmark)
	return ""
	