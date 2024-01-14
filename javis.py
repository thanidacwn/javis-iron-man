import speech_recognition as sr
import pyttsx3
from decouple import config

OPENAPI_KEY = config("OPENAPI_KEY", cast=str)

from openai import OpenAI

client = OpenAI(api_key=OPENAPI_KEY)


def speak_text(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


r = sr.Recognizer()


def record_text():
    while 1:
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                print("\n I'm listening, Please say something...")
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2)
                print(f'\n You said: {MyText}')

                return MyText
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("Unknown Error Occured")


def send_to_chatgpt(messages, model="gpt-3.5-turbo"):
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5)

    message = resp.choices[0].message.content
    messages.append(resp.choices[0].message)

    return message

messages = [{"role": "system", "content": "Hello, I am Javis. I am here to help you with your daily tasks. How can I help you today?"}, {"role": "user", "content": "Please act like Jarvis from Iron man."}]

while True:
    text = record_text()
    messages.append({"role": "user", "content": text})
    response = send_to_chatgpt(messages)
    print(f"\n Answer: {response}")
    speak_text(response)