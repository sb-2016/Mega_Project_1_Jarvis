import os
import speech_recognition as sr
import webbrowser as wb
import pyttsx3 as tts
import music
import requests
import google.generativeai as genai
from gtts import gTTS
import pygame

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
ttsx = tts.init()
url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey=3fa18e979d3e4286b1f1481ac7da6298"
def talk_old(words):
    ttsx.say(words)
    ttsx.runAndWait()
def talk(words):
    tts = gTTS(words)
    tts.save('temp.mp3')
    # Initialize Pygame Mixer
    pygame.mixer.init()

    # Load your MP3 file
    mp3_file = "temp.mp3"  # Replace with the actual path to your MP3 file
    pygame.mixer.music.load(mp3_file)

    # Start playback
    pygame.mixer.music.play()

    # Wait for playback to finish
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()

    # Clean up
    os.remove('temp.mp3')

def aiprocess(command):
    API_KEY = "GOOGLE_API_KEY"

    genai.configure(api_key="GOOGLE_API_KEY")

    model = genai.GenerativeModel('gemini-1.5-flash')

    response = model.generate_content(command)
    return (response.text)

def processcommand(c):
    command = c.lower()
    if "open google" in command:
        talk("Opening Google")
        wb.open("https://www.google.com")
    elif "open youtube" in command:
        talk("Opening YouTube")
        wb.open("https://www.youtube.com")
    elif "open facebook" in command:
        talk("Opening Facebook")
        wb.open("https://www.facebook.com")
    elif "open linkedin" in command:
        talk("Opening LinkedIn")
        wb.open("https://www.linkedin.com")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = music.music[song]
        wb.open(link)
        talk(f"Playing {song}")

    elif c.lower().startswith("news"):
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            for article in articles:
                title = article.get('title', 'No title available')
                talk(title)
        else:
            talk("Error fetching headlines. Please check your API key and try again.")
    else:
         # Let openai handle the command
        response = aiprocess(command)
        talk(response)


if __name__ == "__main__":
    talk("Initializing Jarvis....")
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Listening for Jarvis...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=1)
            command = recognizer.recognize_google(audio)
            if command.lower() == "jarvis":
                talk("Yes, how can I help you?")
                print("Yes, how can I help you?")
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source)
                    print("Listening for command...")
                    audio = recognizer.listen(source, timeout=2, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    processcommand(command)
            print("You said: " + command)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"Error; {e}")
