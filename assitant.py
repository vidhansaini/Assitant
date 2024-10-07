import os
import subprocess
import speech_recognition as sr
import pyttsx3
import ctypes
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

# Initialize speech recognition and text-to-speech
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to speak out responses
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen for a command
def listen():
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjusts for background noise
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"Command received: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        print("Could not understand the audio")
        return ""
    except sr.RequestError as e:
        speak("Could not request results. Check your internet connection.")
        print(f"RequestError: {e}")
        return ""

# Function to open files/folders/applications
def open_application(path):
    try:
        os.startfile(path)  # Windows
        speak(f"Opening {path}")
    except Exception as e:
        speak("Sorry, I can't open that.")
        print(e)

# Function to control volume
def set_volume(level):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        
        # Get range and scale the volume properly
        current_volume = volume.GetMasterVolumeLevelScalar()
        new_volume = min(max(current_volume + level, 0.0), 1.0)  # Valid range 0 to 1
        
        volume.SetMasterVolumeLevelScalar(new_volume, None)
        speak(f"Volume set to {int(new_volume * 100)}%")
    except Exception as e:
        speak("Sorry, I couldn't adjust the volume.")
        print(f"Volume error: {e}")


# Function to control brightness
def change_brightness(level):
    try:
        displays = sbc.list_monitors()  # Check available monitors
        if not displays:
            speak("No monitors detected.")
            return
        
        current_brightness = sbc.get_brightness(display=displays[0])[0]
        new_brightness = min(max(current_brightness + level, 0), 100)
        
        sbc.set_brightness(new_brightness, display=displays[0])
        speak(f"Brightness set to {new_brightness}%")
    except Exception as e:
        speak("Sorry, I couldn't adjust the brightness.")
        print(f"Brightness error: {e}")

#Function for keyboard
def open_on_screen_keyboard():
    try:
        os.system("start osk")  # Windows
        speak("Opening on-screen keyboard.")
    except Exception as e:
        speak("Sorry, I can't open the on-screen keyboard.")
        print(f"Keyboard error: {e}")

#Function to get news
def get_news(country, category):
    try:
        # Ensure getnews.py exists and works
        if not os.path.exists('getnews.py'):
            speak("The news fetching script is missing.")
            return
        
        # Assuming getnews.py handles country and category as arguments
        subprocess.run(['python', 'getnews.py', country, category], check=True)
        speak(f"Fetching {category} news from {country}.")
    except Exception as e:
        speak("Sorry, I couldn't fetch the news.")
        print(f"News error: {e}")

# Core function to handle commands
def handle_command(command):
    if 'open' in command:
        if 'notepad' in command:
            open_application("notepad.exe")
        elif 'chrome' in command:
            open_application("C:/Program Files/Google/Chrome/Application/chrome.exe")
        elif 'ghostoftsushima' in command:
            open_application("C:\Games\Ghost of Tsushima DIRECTOR'S CUT\GhostOfTsushima.exe")
        else:
            speak("Sorry, I don't know how to open that.")
    
    elif 'volume' in command:
        if 'up' in command:
            set_volume(0.1)  # Increase volume by 10%
        elif 'down' in command:
            set_volume(-0.1)  # Decrease volume by 10%
    
    elif 'brightness' in command:
        if 'up' in command:
            change_brightness(10)  # Increase brightness by 10%
        elif 'down' in command:
            change_brightness(-10)  # Decrease brightness by 10%
    
    elif 'news' in command:
        try:
            # Example command: "dexter news india sports"
            words = command.split()
            if len(words) >= 3:
                country = words[1]   # Extract country (second word)
                category = ' '.join(words[2:])  # Extract everything after the country as category
                get_news(country, category)
            else:
                speak("Please specify both a country and a category for the news.")
        except Exception as e:
            speak("Sorry, I couldn't process the news request.")
            print(f"Command error: {e}")
    
    elif 'keyboard' in command:
        open_on_screen_keyboard()
    
    else:
        speak("Sorry, I don't understand that command.")

# Main function to run Dexter
def run_dexter():
    speak("Hello, I am Dexter. How can I assist you?")
    while True:
        command = listen()  # Listen for command
        if command and 'dexter' in command:  # Ensure hotword is in command
            command = command.replace('dexter', '').strip()
            print(f"Processing command: {command}")
            
            if 'exit' in command or 'quit' in command:
                speak("Goodbye!")
                break
            else:
                handle_command(command)
        else:
            print(f"No valid hotword 'Dexter' detected in: {command}")


# Run Dexter
if __name__ == "__main__":
    run_dexter()
