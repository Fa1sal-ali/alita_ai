# Author: Faisal Ali
# Creation Date: 7th Aug 2021
# Version: 0.0.2
# Revision Date: 15th Aug 2021

# Importing libraries
import pyttsx3 as tts
import speech_recognition as sr

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

if __name__ == "__main__":
    ai_obj = AlitaSpeechRecog()
    command = ai_obj.recognition().lower()
    print(command)
