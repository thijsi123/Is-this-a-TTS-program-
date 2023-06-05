import tkinter as tk
from tkinter import OUTSIDE
from PIL import ImageGrab, ImageDraw, ImageTk, ImageOps
import colorsys
import math
import pyttsx3
from threading import Thread
from time import sleep
import pygetwindow as gw
import win32gui
import os
import screeninfo
import pytesseract
import PIL.Image as Image
import playsound
from tkinter import Scale


class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)
        self.voices = self.engine.getProperty('voices')
        self.current_voice = self.voices[0].id

    def start_tts(self, text, speed=1.0, pitch=1.0):
        self.set_volume(pitch)
        self.engine.setProperty('voice', self.current_voice)

        if self.enable_speed_var.get():  # Check if speed checkbox is enabled
            self.set_speed(speed * 150)  # Apply the speed multiplier
        else:
            self.set_speed(150)  # Set speed to default 150

        self.engine.save_to_file(text, 'C:/Python Projects/TTS/temp.wav')
        self.engine.runAndWait()  # Wait for the synthesis to finish
        print("Saved audio to: ", os.path.abspath('C:/Python Projects/TTS/temp.wav'))

        # Now play the saved audio file
        playsound.playsound('C:/Python Projects/TTS/temp.wav')

    def stop_tts(self):
        self.engine.stop()

    def set_voice(self, voice_id):
        self.current_voice = voice_id

    def set_speed(self, speed):
        self.engine.setProperty('rate', speed)
        self.speed_multiplier = speed / 150  # Update the speed multiplier

    def set_volume(self, volume):
        self.engine.setProperty('volume', volume)

class TransparentWindow:
    def __init__(self, tts):
        self.root = tk.Tk()
        self.root.attributes('-alpha', 0.7)
        self.root.geometry('400x300')
        self.root.title('Transparent Window')

        self.always_on_top_var = tk.BooleanVar()
        self.always_on_top_checkbox = tk.Checkbutton(
            self.root,
            text='Always on Top',
            variable=self.always_on_top_var,
            command=self.set_always_on_top
        )
        self.always_on_top_checkbox.pack()

        self.button_window = tk.Toplevel(self.root)
        self.button_window.title('Capture Button')
        self.button_window.geometry('200x200')

        self.button = tk.Button(
            self.button_window,
            text='Capture',
            command=self.capture_screen,
            bg="red"
        )
        self.button.place(relx=0.5, rely=0.5, anchor='center', relwidth=1.0, relheight=0.5, bordermode=OUTSIDE)

        self.transparency = 0.7

        self.tts = tts

        self.button_window.protocol("WM_DELETE_WINDOW", self.on_button_window_closed)

        # Allow dragging of the windows
        self.root.bind('<ButtonPress-1>', self.start_drag)
        self.root.bind('<B1-Motion>', self.drag_window)

        self.button_window.bind('<ButtonPress-1>', self.start_drag2)
        self.button_window.bind('<B1-Motion>', self.drag_window2)

        # Track the root window's size changes
        self.root.bind('<Configure>', self.resize_button)

        # Track the button window's size changes
        self.button_window.bind('<Configure>', self.resize_button2)

        self.speed_slider = Scale(
            self.button_window,
            from_=1.1,
            to=2.0,
            resolution=0.1,
            orient='horizontal',
            label='Speed',
            command=self.update_speed
        )
        self.speed_slider.set(1.1)
        self.speed_slider.pack()

        self.enable_speed_var = tk.BooleanVar()
        self.enable_speed_checkbox = tk.Checkbutton(
            self.button_window,
            text='Enable Speed',
            variable=self.enable_speed_var,
            command=self.toggle_speed_slider
        )
        self.enable_speed_checkbox.pack()

        self.toggle_speed_slider()

    def toggle_speed_slider(self):
        if self.enable_speed_var.get():
            self.speed_slider.config(state='normal')
        else:
            self.speed_slider.config(state='disabled')
            if not self.enable_speed_var.get():
                self.speed_slider.set(1.1)
                self.tts.set_speed(1.1)

    def update_speed(self, speed):
        if self.enable_speed_var.get():
            self.tts.set_speed(float(speed))
        else:
            self.tts.set_speed(float(1.1))
            print('Speed is disabled')



    def start_drag(self, event):
        self.root.x = event.x
        self.root.y = event.y

    def drag_window(self, event):
        deltax = event.x - self.root.x
        deltay = event.y - self.root.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def start_drag2(self, event):
        self.button_window.x = event.x
        self.button_window.y = event.y

    def drag_window2(self, event):
        if event.widget == self.button_window:
            deltax = event.x - self.button_window.x
            deltay = event.y - self.button_window.y
            x = self.button_window.winfo_x() + deltax
            y = self.button_window.winfo_y() + deltay
            self.button_window.geometry(f"+{x}+{y}")

    def set_always_on_top(self):
        self.root.attributes('-topmost', self.always_on_top_var.get())
        self.button_window.attributes('-topmost', self.always_on_top_var.get())

    def on_button_window_closed(self, event=None):
        # Perform any necessary cleanup or actions before terminating
        print("Button window closed")

        # Terminate the script
        self.root.destroy()
        os._exit(0)

    def resize_button(self, event):
        button_size = min(event.width, event.height)  # Size the button to the smaller dimension
        self.button.configure(width=button_size, height=button_size)

    def resize_button2(self, event):
        button_size = min(event.width, event.height)  # Size the button to the smaller dimension
        self.button.configure(width=button_size, height=button_size)

    def capture_screen(self):
        # Disable the capture button to prevent multiple clicks
        self.button.config(state='disabled')

        # Execute the capture process in a separate thread
        capture_thread = Thread(target=self._capture_process)
        capture_thread.start()

    def _capture_process(self):
        # Get the screen resolution
        screen = screeninfo.get_monitors()[0]  # Assumes a single monitor setup
        screen_width, screen_height = screen.width, screen.height
        Image.MAX_IMAGE_PIXELS = None

        # Set initial window visibility flag
        is_visible = False

        # Get the initial opacity value
        initial_opacity = self.root.attributes('-alpha')

        # Define word substitution mapping
        word_mapping = {
            "Thijs": "Thice", #works like 50% of the time -_-
            "thijs": "Thighse",#<-|
            "have": "haave"

            # Add more word substitutions as needed
        }

        while True:
            # Get the root window
            root_window = gw.getWindowsWithTitle(self.root.title())[0]

            # Get the window's handle
            window_handle = root_window._hWnd

            # Get the window's position and dimensions
            rect = win32gui.GetWindowRect(window_handle)
            left, top, right, bottom = rect

            # Set the window opacity to 0
            self.root.attributes('-alpha', 0)

            # Capture the screen region of the root window
            screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
            screenshot_path = "screenshot.png"
            screenshot.save(screenshot_path)

            # Preprocess the image
            #processed_image = self.preprocess_image(screenshot)

            # Save the preprocessed image
            #processed_image_path = "processed_screenshot.png"
            #processed_image.save(processed_image_path)

            # Restore the window's previous opacity
            self.root.attributes('-alpha', initial_opacity)
            self.button.config(state='normal')
            # Add a delay to prevent continuous capturing
            sleep(0.1)


            # Extract text from the preprocessed image
            extracted_text = pytesseract.image_to_string(screenshot) #processed_image
            modified_text = self.modify_text(extracted_text, word_mapping)

            if extracted_text:
                # Show the window if not visible
                if not is_visible:
                    self.root.deiconify()
                    is_visible = True

                # Stop any ongoing TTS synthesis
                self.tts.stop_tts()

                # Start TTS synthesis with the modified extracted text
                self.tts.start_tts(modified_text, speed=float(self.speed_slider.get()))
                self.button.config(state='normal')
            else:
                # Debug message when no text is detected
                print("No text detected in the captured image")
                self.button.config(state='normal')

            # Enable the capture button after the capture process is complete
            self.button.config(state='normal')

            if not button_pressed:
                break


    def modify_text(self, text, word_mapping):
        # Split the text into words
        words = text.split()

        # Iterate over the words and substitute if needed
        modified_words = []
        for word in words:
            modified_word = word_mapping.get(word.lower(), word)
            modified_words.append(modified_word)

        # Join the modified words back into a single string
        modified_text = " ".join(modified_words)

        return modified_text

    def preprocess_image(self, image):
        # Preprocess the image here (e.g., enhance contrast, resize, remove noise, etc.)
        enhanced_image = ImageOps.autocontrast(image)

        return enhanced_image

    def set_background_color(self, color):
        self.root.configure(bg=color)

    def set_transparency(self, transparency):
        self.transparency = transparency
        self.root.attributes('-alpha', self.transparency)

    def run(self):
        self.root.mainloop()


class ButtonsWindow:
    def __init__(self, transparent_window, tts):
        self.transparent_window = transparent_window
        self.tts = tts

        self.root = tk.Toplevel(self.transparent_window.root)
        self.root.geometry('300x400')
        self.root.title('Buttons')

        self.always_on_top_var = tk.BooleanVar()
        self.always_on_top_checkbox = tk.Checkbutton(
            self.root,
            text='Always on Top',
            variable=self.always_on_top_var,
            command=self.set_always_on_top
        )
        self.always_on_top_checkbox.pack()

        self.transparency_label = tk.Label(self.root, text='Transparency')
        self.transparency_label.pack()

        self.transparency_slider = tk.Scale(
            self.root,
            from_=0,
            to=100,
            orient='horizontal',
            command=self.set_transparency
        )
        self.transparency_slider.set(int(self.transparent_window.transparency * 100))
        self.transparency_slider.pack()

        self.color_wheel = ColorWheel(self.root, self.set_color)
        self.color_wheel.pack()

        self.voice_label = tk.Label(self.root, text='TTS Voice')
        self.voice_label.pack()

        self.tts_buttons = TTSButtons(self.root, self.set_tts_voice)
        self.tts_buttons.pack()

    def set_always_on_top(self):
        self.root.attributes('-topmost', self.always_on_top_var.get())

    def set_transparency(self, value):
        transparency = float(value) / 100
        self.transparent_window.set_transparency(transparency)

    def set_color(self, color):
        self.transparent_window.set_background_color(color)

    def set_tts_voice(self, voice_id):
        self.tts.set_voice(voice_id)

    def run(self):
        self.root.mainloop()


class TTSButtons(tk.Frame):
    def __init__(self, parent, set_tts_voice):
        super().__init__(parent)
        self.set_tts_voice = set_tts_voice

        self.create_buttons()

    def create_buttons(self):
        male_button = tk.Button(
            self,
            text='Male',
            command=lambda: self.set_tts_voice(
                'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')
        )
        female_button = tk.Button(
            self,
            text='Female',
            command=lambda: self.set_tts_voice(
                'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')  # TTS_MS_en-US_Helen_11.0
        )

        male_button.pack(side='left', padx=5, pady=5)
        female_button.pack(side='left', padx=5, pady=5)


class ColorWheel(tk.Canvas):
    def __init__(self, parent, callback):
        super().__init__(parent, width=200, height=200)
        self.callback = callback

        self.selected_color = "#000000"

        self.bind("<Button-1>", self.update_color)
        self.bind("<B1-Motion>", self.update_color)

        self.create_color_spectrum()

    def create_color_spectrum(self):
        image = Image.new("RGB", (200, 200))
        draw = ImageDraw.Draw(image)

        for y in range(200):
            for x in range(200):
                hue = math.atan2(y - 100, x - 100) / (2 * math.pi) + 0.5
                saturation = math.hypot(x - 100, y - 100) / 100.0
                r, g, b = colorsys.hsv_to_rgb(hue, saturation, 1)
                color = (int(r * 255), int(g * 255), int(b * 255))
                draw.point((x, y), fill=color)

        self.color_spectrum_image = ImageTk.PhotoImage(image)
        self.create_image(0, 0, image=self.color_spectrum_image, anchor="nw")


if __name__ == '__main__':
    tts = TextToSpeech()
    transparent_window = TransparentWindow(tts)
    buttons_window = ButtonsWindow(transparent_window, tts)
    buttons_window.run()
