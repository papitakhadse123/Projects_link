import google.generativeai as genai
import datetime
import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr



API_KEY = "AIzaSyB9O8mum0XK0N10F96PYKBOSn_cUWIoOBQ"


genai.configure(api_key=API_KEY)


model = genai.GenerativeModel("gemini-2.0-pro-exp")
chat = model.start_chat()


recognizer = sr.Recognizer()
import mysql.connector



def process_message():
    user_message = user_input.get().strip()
    user_input.delete(0, tk.END)

    if not user_message:
        return
    
    display_message(f"You: {user_message}", "blue")
    
    user_message_lower = user_message.lower()
    if "date" in user_message_lower or "today's date" in user_message_lower:
        response_text = f"Today's date is {datetime.datetime.now().strftime('%A, %B %d, %Y')}."
    elif "time" in user_message_lower or "what is the time now" in user_message_lower:
        response_text = f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}"
    else:
        response = chat.send_message(user_message)
        response_text = response.text.strip()
    
    display_message(f"Chatbot: {response_text}", "green")

def display_message(message, color):
    chat_display.configure(state=tk.NORMAL)
    chat_display.insert(tk.END, message + "\n", (color,))
    chat_display.configure(state=tk.DISABLED)
    chat_display.yview(tk.END)

def voice_input():
    with sr.Microphone() as source:
        status_label.config(text="Listening...", fg="orange")
        root.update()
        try:
            audio = recognizer.listen(source, timeout=5)
            user_message = recognizer.recognize_google(audio)
            user_input.insert(0, user_message)
            status_label.config(text="Voice input received!", fg="green")
            process_message()
        except sr.UnknownValueError:
            status_label.config(text="Sorry, could not understand.", fg="red")
        except sr.RequestError:
            status_label.config(text="Speech service unavailable!", fg="red")


root = tk.Tk()
root.title("Chatbot - ChatGPT Style with Voice Input")
root.geometry("600x700")

chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=25, state=tk.DISABLED)
chat_display.tag_configure("blue", foreground="blue")
chat_display.tag_configure("green", foreground="green")
chat_display.pack(pady=10, padx=10)

status_label = tk.Label(root, text="", fg="black", font=("Arial", 12))
status_label.pack()

input_frame = tk.Frame(root)
input_frame.pack(pady=10)

user_input = tk.Entry(input_frame, width=50, font=("Arial", 14))
user_input.pack(side=tk.LEFT, padx=5)
user_input.bind("<Return>", lambda event: process_message())

send_button = tk.Button(input_frame, text="Send", command=process_message, font=("Arial", 14), bg="#007bff", fg="white")
send_button.pack(side=tk.LEFT, padx=5)

voice_button = tk.Button(input_frame, text="🎤 Speak", command=voice_input, font=("Arial", 14), bg="#ff5733", fg="white")
voice_button.pack(side=tk.LEFT)

root.mainloop()
