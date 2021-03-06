import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import smtplib
import sys
import subprocess


engine = pyttsx3.init('sapi5')      # we can use the inbuilt voices from the windows with this
voices=engine.getProperty('voices')
# print(voices[0].id)
engine.setProperty('voice',voices[0].id)     # to set the voice which we want to use

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >=0 and hour <12:
        speak("Good Morning Mr. Sood")

    elif hour >=12 and hour <18:
        speak("Good Afternoon Mr. Sood")

    else :
        speak("Good Evening Mr. Sood") 

    speak("I am Jerry , How May I Assist You ?")

def takeCommand():

    r = sr.Recognizer()         #helps to recognize audio
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1            # seconds of non-speaking audio before a phrase is considered complete
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio , language='en-in')            # attempt to recognize any speech in the audio
        print("User said: ", query)
    except Exception :
        # print(e)
        print("Can you repeat please...")
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('mymail@gmail.com', 'password')
    server.sendmail('myemail@gmail.com', to, content)
    server.close()

def Note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":","-") + "-note.txt"            #gives the name to the file
    with open(file_name , "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe",file_name])

if __name__=="__main__":        # main method
    wishMe()
    while True:
        query = takeCommand().lower()

        # logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")

        elif 'play music' in query:
            music_dir = 'E:\\movies\\SONGS'         #giving the path of songs file in the system
            songs = os.listdir(music_dir)           #list all the files in the music_dir
            print(songs)    
            os.startfile(os.path.join(music_dir, random.choice(songs)))         #opens the file and plays the random song

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "D:\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'email to' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "destinationEmail@gmail.com"    
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry not able to send this Email!")

        elif 'take notes' in query:
            speak("What would you like me to write down ,sir?")
            text = takeCommand().lower()            # attempt to recognize any speech in the audio
            Note(text)
            speak("I have made a note of that!")

        elif 'turn off' in query:
            sys.exit()

        