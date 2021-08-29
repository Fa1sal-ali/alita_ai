# Author: Faisal Ali
# Creation Date: 7th Aug 2021
# Version: 0.0.4
# Revision Date: 15th Aug 2021

# Importing libraries
import pyttsx3 as tts
import speech_recognition as sr
from datetime import datetime
import random
import logging

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
            logger.info("Detecting any user input")
            rcg.pause_threshold = 1
            audio = rcg.listen(source)
        
        try:
            logger.info("Analyzing the user input")
            query = rcg.recognize_google(audio, language="en-IN")
            logger.info(f"User Command: {query}")
        except Exception as error:
            logger.info(error)
            logger.info("AI Response: Unable to Recognize user input")
            self.communicate("Unable to Recognize user input")
            query = 'none'
        return query

class AlitaActions(AlitaSpeechRecog, AlitaTextToSpeech):
    """
    Contains different methods for actions which assistant can perform
    
    Return:
    Voice Output
    """
    def greetings(self):
        super().__init__(voice = self.voice)
        current_hour = datetime.now()
        morning = [ i for i in range(0,12) ]
        if current_hour.hour in morning:
            logger.info("AI Response: Good Morning !!")
            self.communicate("Good Morning !!")
        elif current_hour.hour > 15:
            logger.info("AI Response: Good Evening !!")
            self.communicate("Good Evening !!")
        else:
            logger.info("AI Response: Good Afternoon !!")
            self.communicate("Good Afternoon !!")
        logger.info("AI Response: How can I help you ?")
        self.communicate("How can I help you ?")
    
    def introduction(self):
        super().__init__(voice = self.voice)
        logger.info(f"AI Response: Hi, I'm Alita. Your digital personal assistant.")
        self.communicate("Hi, I'm Alita. Your digital personal assistant.")

    def general_inquiry(self):
        super().__init__(voice = self.voice)
        replies = ["Somewhere between better and best.", "Oh, terrible, thank you so much!", "You go first. Then, we can compare.", "It's a secret.", "I'm doing great, how about you?"]
        response = random.choice(replies)
        logger.info(f"AI Response: {response}")
        self.communicate(response)
    
    def fun_love(self):
        super().__init__(voice = self.voice)
        replies = ["I love ME too!", "Well, who doesn't?", "I get that a lot!", "You are day-dreaming again!", "Are you sure you aren’t sick or something?", "Yeah, thanks. I love myself too.", "Oh really, that's so funny.", "I sure wish the person who created me had given me the ability to understand this human emotion-love"]
        response = random.choice(replies)
        logger.info(f"AI Response: {response}")
        self.communicate(response)

    def cal_info(self, option):
        super().__init__(voice = self.voice)
        x = datetime.now()
        cal_dic = {'hour': x.strftime("%I"), 'minute':x.strftime("%M"), 'time_of_day':x.strftime("%p"), 'day':x.strftime("%A"),'month': x.strftime("%B"), 'year':x.year}
        if option == 'time':
            response = f"It's {cal_dic['hour']}:{cal_dic['minute']} {cal_dic['time_of_day']}"
        elif option == 'day':
            response = f"Today is {cal_dic['day']}."
        elif option == 'month':
            response = f"The month is {cal_dic['month']}."
        elif option == 'year':
            response = f"The year is {cal_dic['year']}."
        logger.info(f"AI Response: {response}")
        self.communicate(response)

if __name__ == "__main__":
    #Setting up logging
    home_dir = "C:/Users/fa1za/Documents/CODE/PYTHON/alita_digitalassistant/"
    log_file = home_dir+"alita_digitalassistant.log"
    logging.basicConfig(filename=log_file,level=logging.INFO, format='%(asctime)s : %(levelname)s -> %(message)s')
    logger = logging.getLogger("Alita Digital Assistant")

    # Displaying logs to the console
    stream = logging.StreamHandler()
    stream.setLevel(logging.INFO)
    streamformat = logging.Formatter('%(asctime)s : %(levelname)s -> %(message)s')
    stream.setFormatter(streamformat)
    logger.addHandler(stream)

    #Setting up assistant
    ai_obj = AlitaActions()
    ai_obj.greetings()
    while True:
        command = ai_obj.recognition().lower()
        try:
            calc = eval(command)
            logger.info(f"AI Response: {command} is {calc}")
            ai_obj.communicate(f"{command} is {calc}")
            continue
        except:
            pass
        if 'hello' in command:
            logger.info(f"AI Response: Hi there.")
            ai_obj.communicate("Hi there.")
            continue
        elif 'your name' in command:
            logger.info(f"AI Response: My name is Alita.")
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
        elif 'time' in command:
            ai_obj.cal_info(option='time')
            continue
        elif 'day' in command:
            ai_obj.cal_info(option='day')
            continue
        elif 'month' in command:
            ai_obj.cal_info(option='month')
            continue
        elif 'year' in command:
            ai_obj.cal_info(option='year')
            continue
        elif 'none' in command:
            continue
        elif '**' in command:
            logger.info("AI Response: Avoid using inappropriate words.")
            ai_obj.communicate("Avoid using inappropriate words.")
            continue
        else:
            logger.info("AI Response: Still learning, not able to answer the query")
            ai_obj.communicate("Still learning, not able to answer the query")
            continue
