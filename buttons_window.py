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




class TransparentWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-alpha', 0.7)
        self.root.geometry('400x300')
        self.root.title('Transparent Window')

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
        #Failed to add peterg voice
        peterg_button = tk.Button(
            self,
            text='Peterg',
            command=lambda: self.set_tts_voice('G:\AI\RVC-beta\RVC-beta-v2-0618\weights\peterg.pth')
        )

        male_button.pack(side='left', padx=5, pady=5)
        female_button.pack(side='left', padx=5, pady=5)
        #peterg_button.pack(side='left', padx=5, pady=5)



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

