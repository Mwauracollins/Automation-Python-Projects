import os
import subprocess

import openai
import speech_recognition as sr
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get("API_KEY")
openai.api_key = API_KEY
model = "gpt-3.5-turbo-0613"
recognizer = sr.Recognizer()


def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.WaitTimeoutError:
            print("No speech detected")
        except sr.UnknownValueError:
            print("Sorry could not understand you")


def run_conversation():
    try:
        user_command = recognize_speech()
        messages = [
            {
                "role": "user",
                "content": user_command
            }
        ]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
        return response
    except Exception as e:
        print("An error occurred:", str(e))


def voice_reply(response_text):
    tts = gTTS(text=response_text, lang="en")
    tts.save("response.mp3")

    vlc_path = r'C:\Program Files (x86)\VideoLAN\VLC\vlc.exe'
    subprocess.Popen([vlc_path, "response.mp3"])


if __name__ == "__main__":
    response = run_conversation()
    if response:
        voice_reply(response['choices'][0]['messages']['content'])
