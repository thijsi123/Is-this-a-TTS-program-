import tkinter as tk
from PIL import ImageGrab, ImageDraw, ImageTk
import colorsys
import math
import pyttsx3
from threading import Thread
from time import sleep
import pygetwindow as gw
import win32gui
import screeninfo
import os
import screeninfo
import pytesseract
import PIL.Image as Image

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)
        self.voices = self.engine.getProperty('voices')
        self.current_voice = self.voices[0].id

    def start_tts(self, text):
        self.engine.setProperty('voice', self.current_voice)
        self.engine.say(text)
        self.engine.runAndWait()

    def stop_tts(self):
        self.engine.stop()

    def set_voice(self, voice_id):
        self.current_voice = voice_id

    def set_speed(self, speed):
        self.engine.setProperty('rate', speed)

    def set_volume(self, volume):
        self.engine.setProperty('volume', volume)


class TransparentWindow:
    def __init__(self):
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
        self.button_window.geometry('200x150')

        self.button = tk.Button(
            self.button_window,
            text='Capture',
            command=self.capture_screen
        )
        self.button.pack(padx=10, pady=10)

        self.always_on_top_button = tk.Button(
            self.button_window,
            text='Always on Top',
            command=self.set_always_on_top
        )
        self.always_on_top_button.pack(padx=10, pady=5)

        self.transparency = 0.7

        self.tts = TextToSpeech()

    def start_tts(self, text):
        self.tts.start_tts(text)

    def stop_tts(self):
        self.tts.stop_tts()

    def pause_tts(self):
        self.tts.pause_tts()

    def resume_tts(self):
        self.tts.resume_tts()

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
            screenshot.save("screenshot.png")

            # Restore the window's previous opacity
            self.root.attributes('-alpha', initial_opacity)

            # Add a delay to prevent continuous capturing
            sleep(0.1)

            extracted_text = pytesseract.image_to_string(Image.open("screenshot.png"))
            modified_text = " . " + extracted_text  # Prepend "Bread." to the extracted text

            if extracted_text:
                # Show the window if not visible
                if not is_visible:
                    self.root.deiconify()
                    is_visible = True

                # Stop any ongoing TTS synthesis
                self.stop_tts()

                # Start TTS synthesis with the modified extracted text
                print("In start_tts12323")
                self.start_tts(modified_text)

            # Enable the capture button after the capture process is complete
            self.button.config(state='normal')
            if not button_pressed:
                break

        # Hide the window if it was visible during the capture process
        if is_visible:
            self.root.withdraw()

    def set_always_on_top(self):
        self.root.attributes('-topmost', self.always_on_top_var.get())
        self.button_window.attributes('-topmost', self.always_on_top_var.get())

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

        self.root.protocol("WM_DELETE_WINDOW", self.on_buttons_window_closed)
    def on_buttons_window_closed(self):
        # Perform any necessary cleanup or actions before closing the window
        print("Buttons window closed")

        # Terminate the script
        self.root.destroy()
        os._exit(0)

    def set_always_on_top(self):
        self.root.attributes('-topmost', self.always_on_top_var.get())

    def set_transparency(self, value):
        transparency = float(value) / 100
        self.transparent_window.set_transparency(transparency)

    def set_color(self, color):
        self.transparent_window.set_background_color(color)

    def set_tts_voice(self, voice_id):
        self.tts.stop_tts()  # Stop any ongoing TTS synthesis
        self.tts.set_voice(voice_id)
        self.tts.start_tts("Testing voice")  # Test the new voice

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
            command=lambda: self.set_tts_voice('HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')
        )
        female_button = tk.Button(
            self,
            text='Female',
            command=lambda: self.set_tts_voice('HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
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

    def update_color(self, event):
        x, y = event.x, event.y
        hue = math.atan2(y - 100, x - 100) / (2 * math.pi) + 0.5
        saturation = math.hypot(x - 100, y - 100) / 100.0
        self.selected_color = f"#{self.get_hue_rgb(hue, saturation)}"
        self.callback(self.selected_color)

    def get_hue_rgb(self, hue, saturation):
        r, g, b = colorsys.hsv_to_rgb(hue, saturation, 1)
        return f"{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"



if __name__ == '__main__':
    transparent_window = TransparentWindow()
    buttons_window = ButtonsWindow(transparent_window, transparent_window.tts)
    buttons_window.run()

