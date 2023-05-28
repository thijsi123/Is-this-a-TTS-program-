import pyttsx3
from pydub import AudioSegment
from pydub.playback import play

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 1500)
        self.engine.setProperty('volume', 1.0)
        self.voices = self.engine.getProperty('voices')
        self.current_voice = self.voices[0].id

    def start_tts(self, text, speed=1.0, pitch=1.0):
        self.engine.setProperty('voice', self.current_voice)
        self.engine.save_to_file(text, 'temp.wav')
        self.engine.runAndWait()

        # Load the saved audio file
        audio = AudioSegment.from_file('temp.wav')

        # Change the playback speed
        audio = audio.speedup(playback_speed=speed)

        # Change the playback pitch
        audio = audio._spawn(audio.raw_data, overrides={'frame_rate': int(audio.frame_rate * pitch)})

        # Play the modified audio
        play(audio)

    def stop_tts(self):
        self.engine.stop()

    def set_voice(self, voice_id):
        self.current_voice = voice_id

    def set_speed(self, speed):
        self.engine.setProperty('rate', speed)

    def set_volume(self, volume):
        self.engine.setProperty('volume', volume)


engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    print(voice.id, voice.name)