# Author: Faisal Ali
# Creation Date: 7th Aug 2021
# Version: 0.0.2
# Revision Date: 15th Aug 2021

# Importing libraries
import pyttsx3 as tts
import speech_recognition as sr
import datetime
import random

class AlitaTextToSpeech:
    def __init__(self, speed = 190, voice = "Female"):

        """
        A constructor used to initialize Text To Speech

        Parameters:
        speed (int): Set the rate at which word are spoken, default is 190.
        voice (string): Set a Male or a Female voice, default is Female.
        
        Returns:
        None
        """

        # Initiate the engine
        self.engine = tts.init() 

        # Configure the speed
        self.speed = speed
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', self.speed)

        # Configure the voice
        self.voice = voice
        voices = self.engine.getProperty('voices')
        if self.voice.lower() == 'male':
            self.sound = voices[0].id
        else:
            self.sound = voices[1].id
        self.engine.setProperty('voice', self.sound)

    def communicate(self, content):
        """
        Takes the content and returns a voice output for the same.

        Parameters:
        content (string): Information/Message.
        
        Return:
        Voice Output
        """
        self.content = content
        self.engine.say(self.content)
        self.engine.runAndWait()

class AlitaSpeechRecog(AlitaTextToSpeech):
    """
    Taked the voice input from the microphone and returns the recognized words
    
    Return:
    query(string): Recognized voice
    """

    def recognition(self):
        super().__init__(voice = self.voice)
        rcg = sr.Recognizer()
        with sr.Microphone() as source:
            print("Detecting any user input")
            rcg.pause_threshold = 1
            audio = rcg.listen(source)
        
        try:
            print("Analyzing the user input")
            query = rcg.recognize_google(audio, language="en-IN")
            print(f"User Command: {query}")
        except Exception as error:
            print(error)
            print("AI Response: Unable to Recognize user input")
            self.communicate("Unable to Recognize user input")
            query = 'none'
        return query

class AlitaActions(AlitaSpeechRecog, AlitaTextToSpeech):
    
    def greetings(self):
        super().__init__(voice = self.voice)
        current_hour = datetime.datetime.now()
        morning = [ i for i in range(0,12) ]
        if current_hour.hour in morning:
            print("AI Response: Good Morning !!")
            self.communicate("Good Morning !!")
        elif current_hour.hour > 15:
            print("AI Response: Good Evening !!")
            self.communicate("Good Evening !!")
        else:
            print("AI Response: Good Afternoon !!")
            self.communicate("Good Afternoon !!")
        print("AI Response: How can I help you ?")
        self.communicate("How can I help you ?")
    
    def introduction(self):
        super().__init__(voice = self.voice)
        print(f"AI Response: Hi, I'm Alita. Your digital personal assistant.")
        self.communicate("Hi, I'm Alita. Your digital personal assistant.")

    def general_inquiry(self):
        super().__init__(voice = self.voice)
        replies = ["Somewhere between better and best.", "Oh, terrible, thank you so much!", "You go first. Then, we can compare.", "It's a secret.", "I'm doing great, how about you?"]
        response = random.choice(replies)
        print(f"AI Response: {response}")
        self.communicate(response)
    
    def fun_love(self):
        super().__init__(voice = self.voice)
        replies = ["I love ME too!", "Well, who doesn't?", "I get that a lot!", "You are day-dreaming again!", "Are you sure you aren’t sick or something?", "Yeah, thanks. I love myself too.", "Oh really, that's so funny.", "I sure wish the person who created me had given me the ability to understand this human emotion-love"]
        response = random.choice(replies)
        print(f"AI Response: {response}")
        self.communicate(response)

if __name__ == "__main__":
    ai_obj = AlitaActions()
    ai_obj.greetings()
    while True:
        command = ai_obj.recognition().lower()
        try:
            calc = eval(command)
            print(f"AI Response: {command} is {calc}")
            ai_obj.communicate(f"{command} is {calc}")
            continue
        except:
            pass
        if 'hi' in command or 'hello' in command:
            print(f"AI Response: Hi there.")
            ai_obj.communicate("Hi there.")
            continue
        if 'your name' in command:
            print(f"AI Response: My name is Alita.")
            ai_obj.communicate("My name is Alita.")
            continue
        elif 'introduce yourself' in command or 'who are you' in command or 'about yourself' in command:
            ai_obj.introduction()
            continue
        elif 'how are you' in command or 'about you' in command or 'you doing' in command:
            ai_obj.general_inquiry()
            continue
        elif 'i love you' in command:
            ai_obj.fun_love()
            continue
        elif 'none' in command:
            continue
        elif '**' in command:
            print("AI Response: Avoid using inappropriate words.")
            ai_obj.communicate("Avoid using inappropriate words.")
            continue
        else:
            print("AI Response: Still learning, not able to answer the query")
            ai_obj.communicate("Still learning, not able to answer the query")
            continue
