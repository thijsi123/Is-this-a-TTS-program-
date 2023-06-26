# main.py
from transparent_window import TransparentWindow, load_model
from tts import TextToSpeech
from buttons_window import ButtonsWindow
from threading import Thread

if __name__ == '__main__':
    # Create a thread for loading the model
    model_thread = Thread(target=load_model)
    model_thread.start()

    model_thread.join()  # Wait for the model loading thread to finish
    tts = TextToSpeech()
    transparent_window = TransparentWindow(tts)
    buttons_window = ButtonsWindow(transparent_window, tts)
    buttons_window.run()
