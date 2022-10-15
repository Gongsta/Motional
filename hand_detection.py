from re import search
from typing import List
import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

stored_keys = {}

# To delete
font = cv2.FONT_HERSHEY_SIMPLEX
org = (50, 50)
fontScale = 1
color = (255, 0, 0)
thickness = 2

def process_landmark(landmark):
	# print("landmark", type(landmark[0]))
	return 

def compute_distance(curr, target):
	# Compute the distance between two points
	return np.sqrt((target.x-curr.x)**2 + (target.y-curr.y)**2 + (target.z-curr.z)**2)

def store_new_pose(landmark, key):
	# Store the new mapping of a key to a pose in the stored_keys dictionary
	stored_keys[key] = landmark

def search_pose(landmark):
	# Search if this landmark is a hand pose we should be detecting
	max_dist = 0.9

	for key in stored_keys:
		works = True
		for i in range(21):
			if (compute_distance(stored_keys[key][i], landmark[i]) > max_dist):
				print(compute_distance(stored_keys[key][i], landmark[i]))
				works = False
				break
		if works:
			return "Matching key found: " + key
	
	return "No matches found"
	
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
	static_image_mode=False,
	max_num_hands=1, # TODO: Implement Multiplayer with multiple hands
	model_complexity=0, # for faster speed
	min_detection_confidence=0.8,
	min_tracking_confidence=0.5) as hands:
	while cap.isOpened():
		success, image = cap.read()
		if not success:
			print("Ignoring empty camera frame.")
			# If loading a video, use 'break' instead of 'continue'.
			continue

		# To improve performance, optionally mark the image as not writeable to
		# pass by reference.
		image.flags.writeable = False
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		results = hands.process(image)

		# Draw the hand annotations on the image.
		image.flags.writeable = True
		image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
		if results.multi_hand_landmarks:
			for hand_landmarks in results.multi_hand_world_landmarks:
				process_landmark(hand_landmarks.landmark)
				if cv2.waitKey(33) == ord('a'):
					store_new_pose(hand_landmarks.landmark, 'a')

			for hand_landmarks in results.multi_hand_landmarks:
				mp_drawing.draw_landmarks(
					image,
					hand_landmarks,
					mp_hands.HAND_CONNECTIONS,
					mp_drawing_styles.get_default_hand_landmarks_style(),
					mp_drawing_styles.get_default_hand_connections_style())

			# Flip the image horizontally for a selfie-view display.
			image = cv2.flip(image, 1)
			text = search_pose(hand_landmarks.landmark) # TODO: Add counter if this is too slow
			image = cv2.putText(image, text, org, font, 
								fontScale, color, thickness, cv2.LINE_AA)
		else:
			image = cv2.flip(image, 1)
			text = "No Hands Detected"
			image = cv2.putText(image, text, org, font, 
								fontScale, color, thickness, cv2.LINE_AA)

		cv2.imshow('MediaPipe Hands', image)
		if cv2.waitKey(5) & 0xFF == 27:
			break

cap.release()