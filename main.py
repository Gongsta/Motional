from math import fabs
import tkinter as tk
import customtkinter
import cv2
import mediapipe as mp
from PIL import ImageTk, Image
from hand_detection import process_image_hand_detection
import pyautogui
import random
import string
import json

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

users = {}

# class User():
# 	def __init__(self, username, password):
# 		self.scores = []
# 		self.username = username
# 		self.password = password

# 	def toJSON(self):
# 		return json.dumps(self, default=lambda o: o.__dict__, 
# 			sort_keys=True, indent=4)

# [username, password] using array for easier (de)serialization
current_user = ["", ""]

class App(customtkinter.CTk):
	WIDTH = 930
	HEIGHT = 580

	def __init__(self):
		super().__init__()

		with open("users.json") as infile:
			global users
			users = json.load(infile)

		self.title("Motional: Motion is All You Need")
		self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
		self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
		container = customtkinter.CTkFrame(self)
		container.pack(side = "top", fill = "both", expand = True)

		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		self.frames = {}

		for F in (LoginPage, CapturePage):
  
			frame = F(container, self)
  
			# initializing frame of that object from
			# startpage, page1, page2 respectively with
			# for loop
			self.frames[F] = frame
  
			frame.grid(row=0, column=0, sticky ="nsew")
  
		self.show_page(LoginPage)

	def show_page(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

	def on_closing(self, event=0):
		with open("users.json", "w") as outfile:
			json.dump(users, outfile)
		self.destroy()

class LoginPage(customtkinter.CTkFrame):
	def __init__(self, parent, controller):
		super().__init__(master = parent)
		self.controller = controller
  
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)

		self.grid_rowconfigure((0, 9), weight=1)
		self.grid_columnconfigure(0, weight=1)

		self.text = customtkinter.CTkLabel(self, text="username", justify=tk.LEFT)
		self.text.grid(row=0, column=0, sticky="s")
		self.username_entry = customtkinter.CTkEntry(self)
		self.username_entry.grid(row=1, column=0)
		self.label_1 = customtkinter.CTkLabel(self,
											  text="",
											  height=10,
											  text_font=("Roboto Medium", 8),) 
		self.label_1.grid(row=2, column=0)
		
		self.text = customtkinter.CTkLabel(self, text="password", justify=tk.LEFT)
		self.text.grid(row=2, column=0, sticky="s")
		self.password_entry = customtkinter.CTkEntry(self)
		self.password_entry.grid(row=3, column=0)
		self.label_2 = customtkinter.CTkLabel(self,
											  text="",
											  height=10,
											  text_font=("Roboto Medium", 8),) 
		self.label_2.grid(row=4, column=0)

		self.button = customtkinter.CTkButton(self, text ="Login",
				command = self.login)
		self.button.grid(row=5, column=0, sticky="n")

		# self.login_info = customtkinter.CTkLabel(self, text="placeholder", justify=tk.LEFT, text_font=("Roboto Medium", 8))
		# self.login_info.grid(row=6, column=0, sticky="s")
		
		self.button = customtkinter.CTkButton(self, text ="Sign up",
				command = self.sign_up)
		self.button.grid(row=7, column=0, sticky="n")

		self.sign_up_info = customtkinter.CTkLabel(self, text="placeholder", justify=tk.LEFT, text_font=("Roboto Medium", 8))
		self.sign_up_info.grid(row=8, column=0, sticky="s")

		self.button = customtkinter.CTkButton(self, text ="Authenticate as guest",
				command = self.guest_login)
		self.button.grid(row=9, column=0, sticky="n")

		# button = customtkinter.CTkButton(self, text ="Login with Google",
		# command = lambda : controller.show_page(UsernamePage))
		# button.grid(row=0, column=0, padx=10, pady=10)

	def login(self):
		username = self.username_entry.get()
		password = self.password_entry.get()

		if (username not in users.keys() or users[username][1] != password):
			self.sign_up_info.configure(text="Sorry, wrong username/password.", fg="red")
		else:
			global current_user
			current_user = users[username]
			self.controller.show_page(CapturePage)

	def sign_up(self):
		username = self.username_entry.get()
		password = self.password_entry.get()
		
		if (not len(username) or not len(password)):
			self.sign_up_info.configure(text="Sorry, empty username/password.", fg="red")
		elif (username in users.keys()):
			self.sign_up_info.configure(text="Sorry, this username is already taken. Please try a different one.", fg="red")
		else:
			users[username] = [username, password]
			global current_user
			current_user = users[username]
			self.controller.show_page(CapturePage)

	def guest_login(self):
		suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
		username = "Guest#" + suffix
		password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

		while (username in users.keys()):
			suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
			username = "Guest#" + suffix
		
		users[username] =[username, password]
		global current_user
		current_user = users[username]
		self.controller.show_page(CapturePage)

# class UsernamePage(customtkinter.CTkFrame):
# 	def __init__(self, parent, controller):
# 		super().__init__(master = parent)
# 		self.controller = controller
  
# 		self.grid_rowconfigure((0, 3), weight=1)
# 		self.grid_columnconfigure(0, weight=1)

# 		self.text = customtkinter.CTkLabel(self, text="Create a username", justify=tk.LEFT)
# 		self.text.grid(row=0, column=0, sticky="s")
# 		self.username_entry = customtkinter.CTkEntry(self)
# 		self.username_entry.grid(row=1, column=0)
# 		self.label_1 = customtkinter.CTkLabel(self,
# 											  text="",
# 											  height=10,
# 											  text_font=("Roboto Medium", 8),) 
# 		self.label_1.grid(row=2, column=0)
# 		self.button = customtkinter.CTkButton(self, text ="Submit",
# 				command = self.submit_username)
# 		self.button.grid(row=3, column=0, sticky="n")

# 	def submit_username(self):
# 		# TODO: replace with database check
# 		username = self.username_entry.get()
# 		if (username == "taken"):
# 			self.label_1.configure(text="Sorry, this username is already taken. Please try a different one.",
# 									fg="red")
# 		else:
# 			self.label_1.configure(text="Creation successful. Cool name!",
# 									fg="green")
# 			self.controller.show_page(CapturePage)


class CapturePage(customtkinter.CTkFrame):
	def __init__(self, parent, controller):
		super().__init__(master = parent)
		self.controller = controller
		self.update_username = True
		
		self.mp_drawing = mp.solutions.drawing_utils
		self.mp_drawing_styles = mp.solutions.drawing_styles
		self.mp_hands = mp.solutions.hands
		self.hands = self.mp_hands.Hands(
		static_image_mode=False,
		max_num_hands=2, # TODO: Implement Multiplayer with multiple hands
		model_complexity=0, # for faster speed
		min_detection_confidence=0.8,
		min_tracking_confidence=0.5)
		
		self.current_pose = "hand" # Can be "face" or "body"

		self.stored_hand_keys = {}
		self.stored_face_keys = {}
		self.stored_body_keys = {}

		self.running_gesture_keyboard_control = False
		self.storing_key = False # Will be used to check if we are storing hand keys
		
		# self.resizable(False, False) # Remove the option to resize, TODO: Fix it so we can enable that

		self.cap = cv2.VideoCapture(0)

		# ============ create two frames ============

		# configure grid layout (2x1)
		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(0, weight=1)

		self.frame_left = customtkinter.CTkFrame(master=self,
												 width=150,
												 corner_radius=0)
		self.frame_left.grid(row=0, column=0, sticky="nswe")

		self.frame_right = customtkinter.CTkFrame(master=self)
		self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

		# ============ frame_left ============
		# configure grid layout (1x11)
		self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
		self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
		self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
		self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

		self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
											  text="",
											  text_font=("Roboto Medium", -16))  # font name and size in px
		self.label_1.grid(row=1, column=0, pady=10, padx=10)

		self.button_1 = customtkinter.CTkButton(master=self.frame_left,
												text="Flappy Bird",
												command=self.flappy_bird)
		self.button_1.grid(row=2, column=0, pady=10, padx=20)

		self.button_2 = customtkinter.CTkButton(master=self.frame_left,
												text="Pong",
												command=self.button_event)
		self.button_2.grid(row=3, column=0, pady=10, padx=20)

		self.button_3 = customtkinter.CTkButton(master=self.frame_left,
												text="Custom",
												command=self.button_event)
		self.button_3.grid(row=4, column=0, pady=10, padx=20)

		self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:")
		self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

		self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
														values=["Light", "Dark", "System"],
														command=self.change_appearance_mode)
		self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

		self.exit = customtkinter.CTkButton(master=self.frame_left,
												text="Exit",
												command=self.exit_capture,
												fg_color="#D35B58", 
												hover_color="#C77C78")
		self.exit.grid(row=11, column=0, pady=10, padx=20, sticky="w")

		# # ============ frame_right ============
		# # configure grid layout (3x7)
		self.frame_right.rowconfigure((0, 1, 2), weight=1)
		self.frame_right.columnconfigure((0, 1), weight=1)
		self.frame_info = customtkinter.CTkFrame(master=self.frame_right, width=1000)
		self.frame_info.grid(row=0, column=0, columnspan=8, rowspan=4, pady=20, padx=20, sticky="nsew")

		# ============ frame_info ============

		# configure grid layout (1x1)
		self.frame_info.rowconfigure(0, weight=1)
		self.frame_info.columnconfigure(0, weight=1)


		#Capture video frames
		self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
												   height=540,
												   width=960,
												   corner_radius=6,  # <- custom corner radius
												   )
		self.label_info_1.grid(column=0, row=0, padx=5, pady=10)


		# # ============ frame_right ============
		self.text = customtkinter.CTkLabel(master=self.frame_right,
													 text="Key: ",
													 justify=tk.LEFT)
		self.text.grid(row=4, column=0)

		self.key_entry = customtkinter.CTkEntry(master=self.frame_right,
													 text="Enter Key")
		self.key_entry.grid(row=4, column=1, pady=10, padx=20, sticky="w")

		self.save_button = customtkinter.CTkButton(master=self.frame_right,
													 text="Save",
													 command=self.save_key
													 )
		self.save_button.grid(row=4, column=2, pady=10, padx=20, sticky="e")

		self.stored_keys_text = customtkinter.CTkLabel(master=self.frame_right,
													 text=self.stored_hand_keys,
													 justify=tk.LEFT)
		self.stored_keys_text.grid(row=5, column=0)
		
		self.run_button = customtkinter.CTkButton(master=self.frame_right,
													text="Run Gesture-Keyboard Control",
													command=self.toggle_running_gesture_keyboard_control,
													width=230,
													fg_color="#58d35a", 
													hover_color="#78c779"
													)
		self.run_button.grid(row=5, column=2, pady=10, padx=20, sticky="e")

		# set default values
		self.optionmenu_1.set("System")

		self.show_frame()

	def flappy_bird(self):
		print("bird")

	def show_frame(self):
		if (self.update_username and current_user[0]):
			print(current_user[0])
			self.label_1.configure(text=current_user[0])
			self.update_username = False

		_, image = self.cap.read()
		if self.storing_key:
			image, key = process_image_hand_detection(self.hands, image, self.stored_hand_keys, key=self.key_entry.get())
			self.storing_key = False
			self.key_entry.delete(0, tk.END)
			
			# TODO: Put in a function, Update the text
			self.stored_keys_text = customtkinter.CTkLabel(master=self.frame_right,
														text="Registered Keys " + str(list(self.stored_hand_keys.keys())),
														justify=tk.LEFT)
			self.stored_keys_text.grid(row=5, column=0)

		else:
			image, key = process_image_hand_detection(self.hands, image, self.stored_hand_keys)
			if key and self.running_gesture_keyboard_control:
				pyautogui.press(key)
				
		image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
		image = cv2.resize(image, (640, 360))
		image = Image.fromarray(image)
		imgtk = ImageTk.PhotoImage(image=image)
		self.label_info_1.imgtk = imgtk
		self.label_info_1.configure(image=imgtk)
		self.label_info_1.after(50, self.show_frame) 

	def save_key(self):
		self.storing_key = True # This will be updated after self.show_frame, where self.storing_key will be reset to False

	def toggle_running_gesture_keyboard_control(self):
		self.running_gesture_keyboard_control = not self.running_gesture_keyboard_control
		configuration = {
			"text": "Run Gesture-Keyboard Control",
			"fg_color": "#58d35a", 
			"hover_color": "#78c779"
		} if not self.running_gesture_keyboard_control else {
			"text": "Stop Gesture-Keyboard Control",
			"fg_color": "#D35B58", 
			"hover_color": "#C77C78"
		}
		self.run_button.configure(**configuration)

	def button_event(self):
		print("Button pressed")
		
	def change_appearance_mode(self, new_appearance_mode):
		customtkinter.set_appearance_mode(new_appearance_mode)

	def exit_capture(self):
		self.update_username = True
		global current_user
		current_user = ["", ""]
		self.controller.show_page(LoginPage)


if __name__ == "__main__":
	app = App()
	app.mainloop()