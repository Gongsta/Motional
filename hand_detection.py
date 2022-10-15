from re import search
from typing import List
import cv2
import mediapipe as mp
from helper import *

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

stored_keys = {}

cap = cv2.VideoCapture(0)

TOTAL_TRAINING_COUNT = 50
training_count = 0

X = None
y = None
start_training = False
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
					print("Key pressed: " + "a")
					store_new_pose(hand_landmarks.landmark, 'a', stored_keys)
					print(stored_keys)

				text = search_hand_pose(hand_landmarks.landmark, stored_keys) # TODO: Add counter if this is too slow

			for hand_landmarks in results.multi_hand_landmarks:
				mp_drawing.draw_landmarks(
					image,
					hand_landmarks,
					mp_hands.HAND_CONNECTIONS,
					mp_drawing_styles.get_default_hand_landmarks_style(),
					mp_drawing_styles.get_default_hand_connections_style())

			# Flip the image horizontally for a selfie-view display.
			image = cv2.flip(image, 1)
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