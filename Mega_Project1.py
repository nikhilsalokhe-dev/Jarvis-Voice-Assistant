import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from google import genai
from gtts import gTTS
import pygame
import os
import time

recognizer = sr.Recognizer()  # Helps in recognizing speech
engine = pyttsx3.init()  # pyttsx gets initialised
newsapi = "bebad34df02f4c5ca72f299ff14ce533"


def speak_old(text):
    engine.say(text)
    engine.runAndWait()


def speak(text):
    tts = gTTS(text)
    tts.save("temp.mp3")

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the mp3 file
    pygame.mixer.music.load("temp.mp3")

    # Play the mp3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")


api_key = "YOUR GEMINI API KEY"


def aiProcess(command):
    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=command,
        )
        return response.text

    except genai.errors.ClientError as e:
        if "429" in str(e):
            print("⚠️ Rate limit reached! Free tier allows 20 requests/min.")
            return "Sir, I am hitting the free tier request limit. Please wait a minute before asking again."
        else:
            speak(f"API Error: {e}")
            return "Sorry, I encountered an API error."
    except Exception as e:
        speak(f"General Error: {e}")
        return "I am unable to process that request right now."


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")

    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")

    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")

    elif "play" in c.lower():
        song_found = False

        # Loop through your music dictionary keys from musicLibrary
        for song_name in musicLibrary.music.keys():
            # Check if the song name (e.g., "apna bana le") is anywhere in your command
            if song_name in c.lower():
                link = musicLibrary.music[song_name]
                print(f"Matching song found: Opening {song_name}...")
                webbrowser.open(link)
                song_found = True
                break  # Stop checking once we find a match

        if not song_found:
            speak("Sorry, I couldn't find that song in your music library.")

    elif "news" in c.lower():
        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}"
        )
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()

            # Extract the articles
            articles = data.get("articles", [])

            # Print the headlines
            for article in articles:
                speak(article["title"])

    else:
        # Let openAI handle the request
        output = aiProcess(c)
        speak(output)


if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        # Listen for the wake word Jarvis

        # obtain audio from the microphone
        r = sr.Recognizer()

        # recognize speech using Sphinx
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source)
            word = r.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Yes")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)
                    time.sleep(2)

        except Exception as e:
            print("Error; {0}".format(e))
