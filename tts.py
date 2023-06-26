import pyttsx3
from pydub import AudioSegment
from pydub.playback import play
import pyaudio
import wave


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
        print("button 1 pressed")
        # Play the modified audio
        play(audio)

    def start_tts2(self, text, speed=1.0, pitch=1.0, save_path='temp.wav'):
        self.engine.setProperty('voice', self.current_voice)
        self.engine.save_to_file(text, save_path)
        self.engine.runAndWait()

        # Load the saved audio file
        audio = AudioSegment.from_file(save_path)

        # Change the playback speed
        audio = audio.speedup(playback_speed=speed)

        # Change the playback pitch
        audio = audio._spawn(audio.raw_data, overrides={'frame_rate': int(audio.frame_rate * pitch)})

        # Save the modified audio
        audio.export(save_path, format='wav')
        print("button 2 pressed")
        # Play the modified audio through the virtual microphone
        play_audio_through_virtual_microphone(save_path)

    def stop_tts(self):
        self.engine.stop()

    def set_voice(self, voice_id):
        self.current_voice = voice_id

    def set_speed(self, speed):
        self.engine.setProperty('rate', speed)

    def set_volume(self, volume):
        self.engine.setProperty('volume', volume)


def play_audio_through_virtual_microphone(audio_path):
    chunk = 1024

    wf = wave.open(audio_path, 'rb')
    p = pyaudio.PyAudio()

    # Get the index of the virtual microphone
    output_device_index = get_virtual_microphone_index()  # Replace with the actual index of the virtual microphone

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    output_device_index=output_device_index)  # Set the output device to the virtual microphone

    data = wf.readframes(chunk)

    while data:
        stream.write(data)
        data = wf.readframes(chunk)

    stream.stop_stream()
    stream.close()

    p.terminate()


def get_virtual_microphone_index():
    return output_device_index  # Output device index obtained from user selection


def list_audio_devices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    devices = []
    for i in range(num_devices):
        device = p.get_device_info_by_host_api_device_index(0, i)
        devices.append((device['index'], device['name']))
    p.terminate()
    return devices


def select_microphone():
    # List available audio devices
    audio_devices = list_audio_devices()
    for i, device in enumerate(audio_devices):
        print(f"Index: {i}, Name: {device[1]}")

    # Prompt the user for input to select the microphone
    while True:
        try:
            selection = int(input("Enter the index of the desired microphone: "))
            if selection < 0 or selection >= len(audio_devices):
                raise ValueError
            break
        except ValueError:
            print("Invalid selection. Please enter a valid index.")

    return audio_devices[selection][0]  # Return the index of the selected microphone


# Get the index of the virtual microphone
output_device_index = select_microphone()  # Replace with the actual index of the virtual microphone
