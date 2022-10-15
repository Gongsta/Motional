from re import search
from typing import List
import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

stored_keys = {}
def process_landmark(landmark):
	print("landmark", landmark[0].x)

def compute_distance(curr, target):
	# Compute the distance between two points
	return np.sqrt((target.x-curr.x)**2 + (target.y-curr.y)**2 + (target.z-curr.z)**2 )

def store_new_pose(landmark, key):
	# Store the new mapping of a key to a pose in the stored_keys dictionary
	stored_keys[key] = landmark

def search_pose(landmark):
	# Search if this landmark is a hand pose we should be detecting
	max_dist = 0.1
	for key in stored_keys:
		for i in range(21):
			print(compute_distance(stored_keys[key][i], landmark[i]))


cap = cv2.VideoCapture(0)

counter = 0
with mp_hands.Hands(
	static_image_mode=False,
	max_num_hands=1, # TODO: Implement Multiplayer with multiple hands
	model_complexity=0,
	min_detection_confidence=0.5,
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
				if cv2.waitKey(0) == ord('r'):
					store_new_pose(hand_landmarks.landmark, 'r')
				
				# if counter == 0:
				# 	search_pose(hand_landmarks.landmark)
				# counter += 1
				# counter %= 100
			for hand_landmarks in results.multi_hand_landmarks:
				mp_drawing.draw_landmarks(
					image,
					hand_landmarks,
					mp_hands.HAND_CONNECTIONS,
					mp_drawing_styles.get_default_hand_landmarks_style(),
					mp_drawing_styles.get_default_hand_connections_style())
		# Flip the image horizontally for a selfie-view display.
		cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
		if cv2.waitKey(5) & 0xFF == 27:
			break
cap.release()