# main.py
from tts import TextToSpeech
from transparent_window import TransparentWindow
from buttons_window import ButtonsWindow

if __name__ == '__main__':
    tts = TextToSpeech()
    transparent_window = TransparentWindow(tts)
    buttons_window = ButtonsWindow(transparent_window, tts)
    buttons_window.run()
