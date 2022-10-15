import cv2
import mediapipe as mp
from helper import *
from matplotlib.animation import FuncAnimation


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def process_image_body_detection(image, stored_keys, key=None):
		# To improve performance, optionally mark the image as not writeable to
		# pass by reference.
		image.flags.writeable = False
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		results = pose.process(image)

		# Draw the pose annotation on the image.
		image.flags.writeable = True
		image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

		# process_landmark(results.pose_landmarks.landmark)
		if results.pose_landmarks:
			if key:
				print("Key pressed: " + key)
				store_new_pose(results.pose_landmarks.landmark, key, stored_keys)
				print(stored_keys)

			

			plot_realtime(results.pose_landmarks.landmark)
			# plot_realtime(results.pose_landmarks.landmark)
			text = search_body_pose(results.pose_landmarks.landmark, stored_keys)
		else:
			text = "No Body Detected"

		mp_drawing.draw_landmarks(
				image,
				results.pose_landmarks,
				mp_pose.POSE_CONNECTIONS,
				landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
		# Flip the image horizontally for a selfie-view display.

		image = cv2.flip(image, 1)
		image = cv2.putText(image, text, org, font, 
							fontScale, color, thickness, cv2.LINE_AA)
		return image


if __name__ == "__main__":
	stored_keys = {}
	# For webcam input:
	cap = cv2.VideoCapture(0)
	with mp_pose.Pose(
			min_detection_confidence=0.5,
			min_tracking_confidence=0.5) as pose:
		while cap.isOpened():
			success, image = cap.read()
			if not success:
				print("Ignoring empty camera frame.")
				# If loading a video, use 'break' instead of 'continue'.
				continue

			if cv2.waitKey(33) == ord('a'):
				image = process_image_body_detection(image, stored_keys, 'a')
			else:
				image = process_image_body_detection(image, stored_keys)

			cv2.imshow('MediaPipe Pose', image)

			if cv2.waitKey(5) & 0xFF == 27:
				break

	cap.release()