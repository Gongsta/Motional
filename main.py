import tkinter as tk
import customtkinter
import cv2
import mediapipe as mp
from PIL import ImageTk, Image
from hand_detection import process_image_hand_detection

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
	WIDTH = 950
	HEIGHT = 600

	def __init__(self):
		super().__init__()

		self.title("Montional")
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
  
			frame.grid(row = 0, column = 0, sticky ="nsew")
  
		self.show_page(LoginPage)

	def show_page(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

	def on_closing(self, event=0):
		self.destroy()

class LoginPage(customtkinter.CTkFrame):
	def __init__(self, parent, controller):
		super().__init__(master = parent)
  
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)

		button = customtkinter.CTkButton(self, text ="Login with Google",
		command = lambda : controller.show_page(CapturePage))
		button.grid(row = 0, column = 0, padx = 10, pady = 10)

class CapturePage(customtkinter.CTkFrame):
	def __init__(self, parent, controller):
		super().__init__(master = parent)
		
		self.mp_drawing = mp.solutions.drawing_utils
		self.mp_drawing_styles = mp.solutions.drawing_styles
		self.mp_hands = mp.solutions.hands
		self.stored_hand_keys = {}
		self.hands = self.mp_hands.Hands(
		static_image_mode=False,
		max_num_hands=2, # TODO: Implement Multiplayer with multiple hands
		model_complexity=0, # for faster speed
		min_detection_confidence=0.8,
		min_tracking_confidence=0.5)

		
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
											  text="CustomTkinter",
											  text_font=("Roboto Medium", -16))  # font name and size in px
		self.label_1.grid(row=1, column=0, pady=10, padx=10)

		self.button_1 = customtkinter.CTkButton(master=self.frame_left,
												text="CTkButton",
												command=self.button_event)
		self.button_1.grid(row=2, column=0, pady=10, padx=20)

		self.button_2 = customtkinter.CTkButton(master=self.frame_left,
												text="CTkButton",
												command=self.button_event)
		self.button_2.grid(row=3, column=0, pady=10, padx=20)

		self.button_3 = customtkinter.CTkButton(master=self.frame_left,
												text="CTkButton",
												command=self.button_event)
		self.button_3.grid(row=4, column=0, pady=10, padx=20)

		self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:")
		self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

		self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
														values=["Light", "Dark", "System"],
														command=self.change_appearance_mode)
		self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

		# # ============ frame_right ============

		# # configure grid layout (3x7)
		self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
		self.frame_right.rowconfigure(7, weight=10)
		self.frame_right.columnconfigure((0, 1), weight=1)
		self.frame_right.columnconfigure(2, weight=0)

		self.frame_info = customtkinter.CTkFrame(master=self.frame_right, width=1000)
		self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

		# ============ frame_info ============

		# configure grid layout (1x1)
		self.frame_info.rowconfigure(0, weight=1)
		self.frame_info.columnconfigure(0, weight=1)


		#Capture video frames
		self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
												   text="CTkLabel: Lorem ipsum dolor sit,\n" +
														"amet consetetur sadipscing elitr,\n" +
														"sed diam nonumy eirmod tempor" ,
												   height=540,
												   width=960,
												   corner_radius=6,  # <- custom corner radius
												   )
		self.label_info_1.grid(column=0, row=0, padx=5, pady=10)

		# self.progressbar = customtkinter.CTkProgressBar(master=self.frame_info)
		# self.progressbar.grid(row=1, column=0, sticky="ew", padx=15, pady=15)

		# # ============ frame_right ============

		# self.radio_var = tkinter.IntVar(value=0)

		# self.label_radio_group = customtkinter.CTkLabel(master=self.frame_right,
		# 												text="CTkRadioButton Group:")
		# self.label_radio_group.grid(row=0, column=2, columnspan=1, pady=20, padx=10, sticky="")

		# self.radio_button_1 = customtkinter.CTkRadioButton(master=self.frame_right,
		# 												   variable=self.radio_var,
		# 												   value=0)
		# self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")

		# self.radio_button_2 = customtkinter.CTkRadioButton(master=self.frame_right,
		# 												   variable=self.radio_var,
		# 												   value=1)
		# self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")

		# self.radio_button_3 = customtkinter.CTkRadioButton(master=self.frame_right,
		# 												   variable=self.radio_var,
		# 												   value=2)
		# self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

		# self.slider_1 = customtkinter.CTkSlider(master=self.frame_right,
		# 										from_=0,
		# 										to=1,
		# 										number_of_steps=3,
		# 										command=self.progressbar.set)
		# self.slider_1.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky="we")

		# self.slider_2 = customtkinter.CTkSlider(master=self.frame_right,
		# 										command=self.progressbar.set)
		# self.slider_2.grid(row=5, column=0, columnspan=2, pady=10, padx=20, sticky="we")

		# self.switch_1 = customtkinter.CTkSwitch(master=self.frame_right,
		# 										text="CTkSwitch")
		# self.switch_1.grid(row=4, column=2, columnspan=1, pady=10, padx=20, sticky="we")

		# self.switch_2 = customtkinter.CTkSwitch(master=self.frame_right,
		# 										text="CTkSwitch")
		# self.switch_2.grid(row=5, column=2, columnspan=1, pady=10, padx=20, sticky="we")

		# self.combobox_1 = customtkinter.CTkComboBox(master=self.frame_right,
		# 											values=["Value 1", "Value 2"])
		# self.combobox_1.grid(row=6, column=2, columnspan=1, pady=10, padx=20, sticky="we")

		self.check_box_1 = customtkinter.CTkCheckBox(master=self.frame_right,
													 text="CTkCheckBox")
		self.check_box_1.grid(row=6, column=0, pady=10, padx=20, sticky="w")

		self.check_box_2 = customtkinter.CTkCheckBox(master=self.frame_right,
													 text="CTkCheckBox")
		self.check_box_2.grid(row=6, column=1, pady=10, padx=20, sticky="w")

		self.entry = customtkinter.CTkEntry(master=self.frame_right,
											width=120,
											placeholder_text="CTkEntry")
		self.entry.grid(row=8, column=0, columnspan=2, pady=20, padx=20, sticky="we")

		# self.button_5 = customtkinter.CTkButton(master=self.frame_right,
		# 										text="CTkButton",
		# 										border_width=2,  # <- custom border_width
		# 										fg_color=None,  # <- no fg_color
		# 										command=self.button_event)
		# self.button_5.grid(row=8, column=2, columnspan=1, pady=20, padx=20, sticky="we")

		# set default values
		self.optionmenu_1.set("System")
		self.button_3.configure(state="disabled", text="Disabled CTkButton")
		# self.combobox_1.set("CTkCombobox")
		# self.radio_button_1.select()
		# self.slider_1.set(0.2)
		# self.slider_2.set(0.7)
		# self.progressbar.set(0.5)
		# self.switch_2.select()
		# self.radio_button_3.configure(state=tkinter.DISABLED)
		# self.check_box_1.configure(state=tkinter.DISABLED, text="CheckBox disabled")
		# self.check_box_2.select()

		self.show_frame()

	def show_frame(self):
		_, image = self.cap.read()
		image = process_image_hand_detection(self.hands, image, self.stored_hand_keys)
		image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
		image = cv2.resize(image, (640, 360))
		image = Image.fromarray(image)
		imgtk = ImageTk.PhotoImage(image=image)
		self.label_info_1.imgtk = imgtk
		self.label_info_1.configure(image=imgtk)
		self.label_info_1.after(50, self.show_frame) 

	def button_event(self):
		print("Button pressed")

	def change_appearance_mode(self, new_appearance_mode):
		customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
	app = App()
	app.mainloop()