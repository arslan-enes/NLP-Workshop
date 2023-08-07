from bardapi import Bard
import requests

#__Secure-1PSID
token = "get-your-__Secure-1PSID-from-bard.google.com"
bard = Bard(token=token)

# bard get answer
bard.get_answer('How to say "Hello" in German?')

# bard ask_about_image
image = open('chatbot/Flag_of_Turkey.png', 'rb').read()
bard.ask_about_image('What is in the image?', image)['content']

# session example
session = requests.Session()
session.headers = {
            "Host": "bard.google.com",
            "X-Same-Domain": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "https://bard.google.com",
            "Referer": "https://bard.google.com/",
        }
session.cookies.set("__Secure-1PSID", token)

bard = Bard(token=token, session=session, timeout=30)
bard.get_answer('Hi! My name is Enes.')['content']
bard.get_answer("What is my name?")['content']


# TTS
audio = bard.speech('Hello, I am Bard! How can I help you today?')

with open("audio.mp3", 'wb') as mp3_file:
    mp3_file.write(audio)

