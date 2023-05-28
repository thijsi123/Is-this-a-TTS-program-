import tkinter as tk
import pyttsx3

class TTSButtons(tk.Frame):
    def __init__(self, parent, tts):
        super().__init__(parent)

        self.parent = parent
        self.tts = tts

        self.create_buttons()
        self.create_sliders()

    def create_buttons(self):
        voices = self.tts.engine.getProperty('voices')  # Get the list of voices

        female_voice = None
        male_voice = None

        for voice in voices:
            if voice.gender == pyttsx3.voice.VoiceGender.FEMALE:
                female_voice = voice
            elif voice.gender == pyttsx3.voice.VoiceGender.MALE:
                male_voice = voice

        if female_voice:
            female_button = tk.Button(self, text="Female", command=lambda: self.set_tts_voice(female_voice.id))
            female_button.pack(side='left', padx=5, pady=5)

        if male_voice:
            male_button = tk.Button(self, text="Male", command=lambda: self.set_tts_voice(male_voice.id))
            male_button.pack(side='left', padx=5, pady=5)

    def set_tts_voice(self, voice):
        self.tts.set_voice(voice)

    def create_sliders(self):
        pitch_label = tk.Label(self, text="Pitch")
        pitch_label.pack()

        pitch_slider = tk.Scale(self, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, command=self.set_pitch)
        pitch_slider.pack()

        speed_label = tk.Label(self, text="Speed")
        speed_label.pack()

        speed_slider = tk.Scale(self, from_=0, to=200, orient=tk.HORIZONTAL, command=self.set_speed)
        speed_slider.pack()

    def set_pitch(self, value):
        pitch = float(value)
        self.tts.set_pitch(pitch)

    def set_speed(self, value):
        speed = float(value)  # Convert speed to a float
        self.tts.set_speed(speed)
