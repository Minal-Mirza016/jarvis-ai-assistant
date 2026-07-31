import os
try:
    from dotenv import load_dotenv
    # Try loading .env, then config_example.env if .env does not exist
    if os.path.exists('.env'):
        load_dotenv('.env')
    elif os.path.exists('config_example.env'):
        load_dotenv('config_example.env')
except ImportError:
    pass  # dotenv is optional, but recommended for local development
import subprocess
import sys
import webbrowser
import json

# import query  # This module doesn't exist, removing it
import requests
import cv2  # type: ignore
import psutil
import pyautogui
import pyjokes
import pyttsx3
import pywhatkit as kit
import speech_recognition as sr
import wikipedia
from requests import get
import datetime
import time
import pyaudio
import instaloader
import threading
import pyautogui
import psutil
import pyperclip
import smtplib
import requests
import sympy as sp
from forex_python.converter import CurrencyRates
from PyDictionary import PyDictionary



# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Text-to-speech function
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:  # Adjust microphone index if needed
        print('listening...')
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=8)  # Keeps the current timeout values
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please say that again.")
            return "none"

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query

    except sr.UnknownValueError:
        speak("I didn't understand what you said. Please try again.")
        return "none"

    except sr.RequestError as e:
        speak("There was an error connecting to the speech recognition service.")
        return "none"


# Greeting function
def wish():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")
    if hour >= 0 and hour <= 12:
        speak(f"Good Morning!, its {tt}")
    elif hour > 12 and hour <= 18:
        speak(f"Good Afternoon!, its {tt}")
    else:
        speak(f"Good Evening!, its {tt}")
    speak("I am Jarvis, sir. Please tell me how may I help you.")
    # List all available features/services
    features = [
        "Open and close applications like Notepad, Calculator, Chrome, Command Prompt, Camera, etc.",
        "Search on Google, Wikipedia, YouTube, Facebook, StackOverflow.",
        "Play music from your music folders.",
        "Send WhatsApp messages.",
        "Play songs on YouTube.",
        "Pause music.",
        "Tell you a joke.",
        "Provide system information (CPU, battery).",
        "Shut down, restart, or sleep your system.",
        "Switch between windows.",
        "Get weather information for any city.",
        "Chat with AI (Gemini).",
        "Get the latest news headlines.",
        "Control system volume.",
        "Show battery status.",
        "Read clipboard contents.",
        "Get dictionary meanings.",
        "Add and show tasks in a to-do list.",
        "Save voice notes.",
        "Translate text to other languages.",
        "Solve math expressions.",
        "Find your location using IP address.",
        "Check Instagram profiles and download profile pictures.",
        "Take screenshots.",
        "And more! Just ask."
    ]
    speak("Here are some things I can do for you:")
    for feat in features:
        speak(feat)

# to get the latest news 
def news():
    try:
        # Get API key from environment variable or use a default
        api_key = os.getenv('NEWS_API_KEY', '199f6a4d399642c1939348be692a95ec')
        main_url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'

        # Fetch news data
        response = requests.get(main_url)
        if response.status_code != 200:
            speak(f"Failed to fetch news. HTTP status code: {response.status_code}")
            return

        # Parse JSON response
        main_page = response.json()
        articles = main_page.get("articles", [])

        if not articles:
            speak("No news articles found at the moment.")
            return

        # Read top 5 news articles
        speak("Here are the top 5 news headlines for today:")
        for i, article in enumerate(articles[:5]):  # Fetch the first 5 headlines
            title = article.get("title", "No Title Available")
            description = article.get("description", "No Description Available")
            speak(f"News {i + 1}: {title}")
            speak(f"Description: {description}")
    except requests.exceptions.RequestException as e:
        speak(f"An error occurred while fetching the news: {e}")
    except Exception as e:
        speak(f"An unexpected error occurred: {e}")


# Get system information
def system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    battery = psutil.sensors_battery().percent
    speak(f"CPU is at {cpu_usage} percent and battery is at {battery} percent.")


# Tell a joke
def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)


# Shutdown or restart the system
def system_control(action):
    if action == "shutdown":
        speak("Shutting down the system.")
        os.system("shutdown /s /t 1")
    elif action == "restart":
        speak("Restarting the system.")
        os.system("shutdown /r /t 1")


# Open applications
def open_application(app_name):
    try:
        if app_name == "notepad":
            os.startfile("C:\\Windows\\system32\\notepad.exe")
        elif app_name == "calculator":
            subprocess.Popen("calc.exe")
        else:
            speak("Application not found.")
    except Exception as e:
        speak("Unable to open the application.")

# Global variable for camera
cap = None

def open_camera():
    global cap  # Ensure 'cap' is globally accessible
    cap = cv2.VideoCapture(0)
    try:
        while cap.isOpened():
            ret, img = cap.read()
            if not ret:
                speak("Failed to capture video from the camera.")
                break
            cv2.imshow("Webcam", img)
            if cv2.waitKey(50) & 0xFF == 27:  # Exit loop when 'Esc' key is pressed
                break
        cap.release()
        cv2.destroyAllWindows()
    except Exception as e:
        speak(f"An error occurred while using the camera: {e}")
        cap.release()
        cv2.destroyAllWindows()


# chat with gemini 
def chat_with_ai(prompt):
    gemini_api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyDpJHgxEaluV29lrIE_ll4tmYamNOO01NY')
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=' + gemini_api_key
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()
            reply = result['candidates'][0]['content']['parts'][0]['text']
            speak(reply)
        else:
            speak(f"Gemini API error: {response.status_code} {response.text}")
    except Exception as e:
        speak(f"Failed to connect to Gemini API: {e}")


# to get the weather of a city 
def get_weather(city):
    alt_api_key = os.getenv('ALTERNATIVE_WEATHER_API_KEY')
    if alt_api_key and alt_api_key != '94309001167b447f974193340250609':
        # Use WeatherAPI.com
        url = f"http://api.weatherapi.com/v1/current.json?key={alt_api_key}&q={city}&aqi=no"
        try:
            response = requests.get(url)
            data = response.json()
            if 'current' in data:
                weather = data['current']['condition']['text']
                temp = data['current']['temp_c']
                humidity = data['current']['humidity']
                wind_speed = data['current']['wind_kph']
                weather_report = (f"The weather in {city} is currently {weather} "
                                  f"with a temperature of {temp}°C, humidity of {humidity}%, "
                                  f"and wind speed of {wind_speed} km/h.")
                speak(weather_report)
            elif 'error' in data:
                speak(f"WeatherAPI error: {data['error'].get('message', 'Unknown error')}")
            else:
                speak("Sorry, I couldn't find the weather details for that city. Please try again.")
        except Exception as e:
            speak(f"An error occurred while fetching the weather: {e}")
    else:
        # Fallback to OpenWeatherMap
        api_key = os.getenv('WEATHER_API_KEY', "ea4de27bbbaacd4edebd913f7067a6ab")
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
        try:
            response = requests.get(complete_url)
            data = response.json()
            if data["cod"] != "404":
                weather = data["weather"][0]["description"]
                temp = data["main"]["temp"]
                humidity = data["main"]["humidity"]
                wind_speed = data["wind"]["speed"]
                weather_report = (f"The weather in {city} is currently {weather} "
                                  f"with a temperature of {temp}°C, humidity of {humidity}%, "
                                  f"and wind speed of {wind_speed} meters per second.")
                speak(weather_report)
            else:
                speak("Sorry, I couldn't find the weather details for that city. Please try again.")
        except requests.exceptions.RequestException as e:
            speak(f"An error occurred while fetching the weather: {e}")



# to change the volume 
def change_volume(command):
    if "up" in command:
        pyautogui.press("volumeup")
        speak("Volume increased")
    elif "down" in command:
        pyautogui.press("volumedown")
        speak("Volume decreased")
    elif "mute" in command:
        pyautogui.press("volumemute")
        speak("Volume muted")



# to check the battery status 
def battery_status():
    battery = psutil.sensors_battery()
    percent = battery.percent
    speak(f"Battery is at {percent} percent")
    if battery.power_plugged:
        speak("Your laptop is charging")
    elif percent < 20:
        speak("Warning, battery is low. Please plug in the charger")


# to read the clipboard contents 
def read_clipboard():
    text = pyperclip.paste()
    if text:
        speak("Your clipboard contains: " + text)
    else:
        speak("Clipboard is empty")


# to get the meaning of a word 
dictionary = PyDictionary()

def get_meaning(word):
    meaning = dictionary.meaning(word)
    if meaning:
        for key, value in meaning.items():
            speak(f"{key} meaning of {word} is {value[0]}")
            break
    else:
        speak("Sorry, I could not find the meaning")


# to add a task to a list 
def add_task(task):
    with open("todo.txt", "a") as f:
        f.write(task + "\n")
    speak("Task added to your to do list")


# to show the tasks in the list
def show_tasks():
    try:
        with open("todo.txt", "r") as f:
            tasks = f.readlines()
            if tasks:
                speak("Your tasks are")
                for task in tasks:
                    speak(task.strip())
            else:
                speak("Your to do list is empty")
    except FileNotFoundError:
        speak("You don't have a to do list yet")


# to save note 
def save_note():
    speak("What should I write?")
    note = take_command()  # Fixed function name
    with open("voice_notes.txt", "a") as f:
        f.write(note + "\n")
    speak("Your note has been saved")



# to translate the text 
from googletrans import Translator

translator = Translator()

def translate_text(text, dest_lang="es"):
    try:
        translated = translator.translate(text, dest=dest_lang)
        speak(f"Translation: {translated.text}")
    except Exception as e:
        speak(f"Translation failed: {e}")



# to solve the math expression 
def solve_math(expression):
    try:
        expr = sp.sympify(expression)
        result = sp.simplify(expr)
        speak(f"The result is {result}")
    except Exception as e:
        speak(f"Math error: {e}")


# Main function
if __name__ == '__main__':
    wish()
    while True:
            try:
                query = take_command().lower()

                # Skip processing if nothing was recognized
                if query == "none":
                    continue

                # Exit/close/goodbye/quit triggers (only if the query is exactly an exit command)
                exit_commands = [
                    "exit",
                    "close",
                    "goodbye",
                    "quit",
                    "you can sleep",
                    "ok goodbye",
                    "okay goodbye",
                    "bye"
                ]
                if query.strip() in exit_commands:
                    speak('Thanks for using me sir, have a good day')
                    break

                # ...existing code for all other commands...
            except Exception as e:
                print("[FATAL ERROR] Unhandled exception in main loop:", e)
                import traceback
                traceback.print_exc()
                speak(f"A fatal error occurred: {e}")
                
            # to open notepad 
            if "open notepad" in query:
                open_application("notepad")

             #to close notepad
            elif "close notepad" in query:
                speak("Okay sir, closing Notepad")
                os.system("taskkill /f /im notepad.exe")
    

            # to open calculator 
            elif "open calculator" in query:
                open_application("calculator")

            # to close calculator 
            elif "close calculator" in query:
                speak("Okay sir, closing Calculator...")
                for process in psutil.process_iter():
                    try:
                        if "calculator" in process.name().lower():
                            process.terminate()
                            speak("Calculator has been closed.")
                            break
                    except Exception as e:
                        speak(f"An error occurred: {e}")


            # to open chrome
            elif "open chrome" in query:
                speak("Opening Google Chrome...")
                apath = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Include the full path to chrome.exe
                os.startfile(apath)

            # to close chrome     
            elif "close chrome" in query:
                speak("Okay sir, closing Google Chrome...")
                os.system("taskkill /f /im chrome.exe")



            # to open command prompt
            elif "open command prompt" in query:
                speak("Opening Command Prompt...")
                os.system("start cmd")

            # to close command prompt     
            elif "close command prompt" in query:
                speak("Okay sir, closing Command Prompt")
                os.system("taskkill /f /im cmd.exe")


            # to open camera 
            elif "open camera" in query:
                speak("Opening the camera...")
                camera_thread = threading.Thread(target=open_camera)  # Run camera in a separate thread
                camera_thread.start()  # Start the thread

            # to close camera 
            elif "close camera" in query:
                try:
                    speak("Okay sir, closing the camera...")
                    # Release the camera and close any OpenCV windows
                    if cap is not None:
                        cap.release()
                    cv2.destroyAllWindows()
                except NameError:
                    speak("The camera is not currently open.")
                except Exception as e:
                    speak(f"An error occurred while closing the camera: {e}")


            # to get the ip address 
            elif "ip address" in query:
                speak("Fetching your IP address...")
                ip = get('https://api.ipify.org').text
                speak(f"Your IP address is {ip}")


            # to search on wikipedia 
            elif "wikipedia" in query:
                speak("Searching Wikipedia...")
                query = query.replace("wikipedia", "").strip()
                if not query:
                    speak("Please specify what you'd like to search on Wikipedia.")
                else:
                    try:
                        results = wikipedia.summary(query, sentences=2, auto_suggest=True, redirect=True)
                        speak(f"According to Wikipedia, {results}")
                    except wikipedia.DisambiguationError as e:
                        speak(f"Multiple results found for {query}. Please be more specific.")
                    except wikipedia.PageError:
                        speak(f"Sorry, I couldn't find any page on Wikipedia related to {query}.")
                    except Exception as e:
                        speak(f"An error occurred while searching Wikipedia: {e}")


            # open Youtube 
            elif "open youtube" in query:
                speak("Opening YouTube...")
                webbrowser.open("https://www.youtube.com")


            # open Facebook
            elif "open facebook" in query:
                speak("Opening Facebook...")
                webbrowser.open("https://www.facebook.com")


            # open stackoverflow
            elif "open stackoverflow" in query:
                speak("Opening stackoverflow...")
                webbrowser.open("https://www.stackoverflow.com")


            # open and search on google 
            elif "open google" in query:
                speak("What should I search on Google?")
                cm = take_command().lower()
                if cm and cm != "none":
                    search_url = f"https://www.google.com/search?q={cm.replace(' ', '+')}"
                    webbrowser.open(search_url)
                else:
                    speak("I didn't catch your search query. Opening Google home page.")
                    webbrowser.open("https://www.google.com")


            # play music 
            elif "play music" in query:
                # Try multiple common music directories
                music_dirs = [
                    r"C:\Users\warda\Music",
                    r"C:\Users\User\Music", 
                    r"C:\Users\User\Downloads\Music",
                    r"C:\Music"
                ]
                music_found = False
                for music_dir in music_dirs:
                    if os.path.exists(music_dir):
                        try:
                            songs = os.listdir(music_dir)
                            for song in songs:
                                if song.endswith(".mp3"):
                                    os.startfile(os.path.join(music_dir, song))
                                    music_found = True
                                    break
                            if music_found:
                                break
                        except Exception:
                            continue
                if not music_found:
                    speak("No music directory found. Please check your music folder path.")

            # pause music 
            elif "pause music" in query:
                speak("Pausing the music...")
                pyautogui.press("playpause")  # Simulates the media "play/pause" key


            # send whatsapp message 
            elif "send whatsapp message" in query:
                speak("Sending a WhatsApp message...")
                try:
                    phone_number = os.getenv('WHATSAPP_PHONE', "++92 308 9691318")
                    message = "This is a test message from Jarvis. Yes you are a bitch"
                    kit.sendwhatmsg_instantly(phone_number, message)
                    speak("The message has been sent")
                except Exception as e:
                    speak(f"Failed to send WhatsApp message: {e}")


            # play song on youtube 
            elif "play song on youtube" in query:
                speak("Which song should I play on YouTube?")
                song = take_command()
                if song and song != "none":
                    url = f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}"
                    webbrowser.open(url)
                    speak(f"Searching YouTube for {song}")
                else:
                    speak("Sorry, I didn't catch the song name.")

            # search on youtube 
            elif "search on youtube" in query or "search youtube" in query:
                speak("What should I search on YouTube?")
                yt_query = take_command()
                if yt_query and yt_query != "none":
                    url = f"https://www.youtube.com/results?search_query={yt_query.replace(' ', '+')}"
                    webbrowser.open(url)
                    speak(f"Here are the YouTube search results for {yt_query}")
                else:
                    speak("Sorry, I didn't catch the search query.")


            #to find a joke
            elif "tell me a joke" in query:
                joke = pyjokes.get_joke()
                speak(joke)



            #system information
            elif "system info" in query:
                system_info()

            #to shut down the system
            elif "shut down the system" in query:
                os.system('shutdown /s /t S')

            #to restart the system
            elif "restart the system" in query:
                os.system('shutdown /r /t S')

            #to sleep the system
            elif "sleep the system" in query:
                os.system("rundll32.exe powrprof.dll,SetSuspendState Sleep")

            #to switch the window
            elif "switch the window" in query:
                speak("Switching the window...")
                try:
                    # Hold down the Alt key
                    pyautogui.keyDown("alt")
                    time.sleep(0.2)  # Short delay to ensure the Alt key is registered

                    # Press the Tab key to switch windows
                    pyautogui.press("tab")
                    time.sleep(0.2)  # Short delay to stabilize the switch

                    # Release the Alt key
                    pyautogui.keyUp("alt")
                    speak("Window switched successfully.")
                except Exception as e:
                    speak(f"An error occurred while switching the window: {e}")


            # to know thw weather of a city 
            elif "weather" in query:
                speak("Which city do you want the weather for?")
                city = take_command()
                if city and city != "none":
                    get_weather(city)
                else:
                    speak("Sorry, I didn't catch the city name.")



            #to chat with Gemini    
            elif "chat with me" in query:
                speak("Sure! What would you like to talk about?")
                user_input = take_command()
                if user_input and user_input != "none":
                    chat_with_ai(user_input)
                else:
                    speak("Sorry, I didn't catch that.")



            # to know the news
            elif "news" in query:
                speak('Please wait sir, fetching the latest news')
                news()
                speak("Here are the latest headlines")



            # volume control
            elif "volume" in query:
                change_volume(query)
                speak("I have adjusted the volume")

            # to show battery status
            elif "battery" in query:
                speak('Checking your battery status sir')
                battery_status()
                speak("That is your current battery level")

            # clipboard reader
            elif "clipboard" in query:
                speak("Reading the clipboard contents for you")
                read_clipboard()



            # dictionary meaning
            elif "meaning of" in query:
                word = query.replace("meaning of", "").strip()
                get_meaning(word)
                speak(f"I have found the meaning of {word}")



            # to-do list
            elif "add task" in query:
                task = query.replace("add task", "").strip()
                add_task(task)
                speak(f"I have added the task: {task}")

            # to show tasks
            elif "show tasks" in query:
                speak("Here are your tasks sir")
                show_tasks()

            # save notes
            elif "note" in query or "remember this" in query:
                save_note()
                speak("Your note has been saved successfully")



            #google translate
            elif "translate" in query:
                speak("What should I translate?")
                text = take_command()
                if not text or text == "none":
                    speak("Sorry, I didn't catch what to translate.")
                else:
                    speak("Which language?")
                    lang = take_command().lower()
                    if not lang or lang == "none":
                        speak("Sorry, I didn't catch the language.")
                    else:
                        translate_text(text, lang)



            #math solver
            elif "solve" in query:
                speak("Tell me the expression")
                expr = take_command()
                if expr and expr != "none":
                    solve_math(expr)
                else:
                    speak("Sorry, I didn't catch the expression.")



            #to find my location using IP address
            elif "where i am" in query or "where we are" in query:
                speak("Wait sir, let me check...")
                try:
                    # Get the public IP address
                    ipAdd = requests.get('https://api.ipify.org').text
                    print(f"Public IP Address: {ipAdd}")

                    # Fetch location details using GeoJS
                    url = f'https://get.geojs.io/v1/ip/geo/{ipAdd}.json'
                    geo_requests = requests.get(url)
                    geo_data = geo_requests.json()

                    # Extract city and country from the response
                    city = geo_data.get('city', 'Unknown city')
                    country = geo_data.get('country', 'Unknown country')

                    speak(f"Sir, I am not sure, but I think we are in {city} city of {country} country.")
                except requests.exceptions.RequestException as e:
                    speak("Sorry sir, there seems to be a network issue.")
                    print(f"Network error: {e}")
                except Exception as e:
                    speak("Sorry sir, I couldn't determine your location due to an error.")
                    print(f"Error: {e}")



            # To check a instagram profile
            elif "instagram profile" in query or "profile on instagram" in query:
                try:
                    speak("Please say the Instagram username.")
                    name = take_command().replace(' ', '').strip()
                    if not name or name == "none":
                        speak("Sorry, I didn't catch the username.")
                    else:
                        profile_url = f'https://www.instagram.com/{name}'
                        webbrowser.open(profile_url)
                        speak(f"Here is the profile of the user {name}.")
                        time.sleep(5)
                        max_attempts = 3
                        for attempt in range(max_attempts):
                            speak("Would you like to download the profile picture of this account? Please say yes or no.")
                            confirm = take_command().lower()
                            if any(word in confirm for word in ["yes", "yeah", "yup", "sure", "ok", "okay"]):
                                try:
                                    import instaloader
                                    loader = instaloader.Instaloader()
                                    loader.download_profile(name, profile_pic_only=True)
                                    speak("The profile picture has been saved in the current folder.")
                                except Exception as e:
                                    speak(f"Failed to download profile picture: {e}")
                                break
                            elif any(word in confirm for word in ["no", "nope", "nah"]):
                                speak("Alright, I will not download the profile picture.")
                                break
                            elif attempt < max_attempts - 1:
                                speak("I didn't understand what you said. Please try again.")
                            else:
                                speak("Sorry, I couldn't understand your response. Skipping download.")
                                break
                except Exception as e:
                    speak(f"An error occurred: {e}")



            # To take screenshot
            elif "take screenshot" in query or "take a screenshot" in query:
                speak("sir, please tell me the name for this screenshot file")
                name = take_command().lower()
                if not name or name == "none":
                    speak("Sorry, I didn't catch the file name for the screenshot.")
                else:
                    speak("please sir hold the screen for few seconds, I am taking screenshot")
                    time.sleep(3)
                    img = pyautogui.screenshot()
                    img.save(f"{name}.png")
                    speak(f"I am done sir, the screenshot is saved in our main folder. now I am ready for more.")
