import openai
from tkinter import *
from tkinter import filedialog, Tk, Button, Label, StringVar, PhotoImage, messagebox
import base64
import requests
from moviepy.editor import VideoFileClip
import cv2
import pygame

your_api_key = 'YOUR_API_KEY' #has to have gpt4-vision-preview

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def image_request(image_path, api_key):
  base64_image = encode_image(image_path)

  prompt = 'Based on this image, you are to evaluate my outfit considering the harmony and contrast of colors, the proportions and fit of the clothing in relation to my body type, and how well the outfit complements the my body shape. Make it short without introduction'
  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {your_api_key}"
  }

  payload = {
      "model": "gpt-4-vision-preview",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": prompt
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              }
            }
          ]
        }
      ],
      "max_tokens": 1500
  }

  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
  return response

def extract_message(json_data):
  res = json_data.json()
  return res['choices'][0]['message']['content']


def analyze(image_path, feedback_text):
  res = image_request(image_path, your_api_key)
  extracted = extract_message(res)
  messagebox.showinfo("YOU ARE A CERTIFIED SLAY QUEEN (or king)", extracted)

def upload_image(feedback_text):
  image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png")])
  feedback_text.set(f"Image uploaded: {image_path}")
  return image_path


def update_frame(index, label, window, delay):
  try:
      # Load the next frame of the GIF
      frame = PhotoImage(file='mattel_please_dont_sue_me.gif', format=f"gif -index {index}")
      label.config(image=frame)
      # Keep a reference to the image to prevent garbage collection
      label.image = frame

      # Attempt to load the next frame to determine if it exists
      try:
          PhotoImage(file='mattel_please_dont_sue_me.gif', format=f"gif -index {index+1}")
          window.after(delay, update_frame, index+1, label, window, delay)  # Proceed to next frame after 100ms
      except:
          window.after(delay, update_frame, 0, label, window, delay)  # If next frame doesn't exist, restart from frame 0
  except Exception as e:
      print(e)

def main():
  window = Tk()
  window.title("Are you a slay queen (or king)")

  pygame.mixer.init()
  pygame.mixer.music.load('chipi_chipi_chapa_chapa_dubi_dubi_daba_daba.mp3')
  pygame.mixer.music.play(-1)

  feedback_text = StringVar(window)
  analyze_button = Button(window, text="Analyze your outfit", command=lambda: analyze(upload_image(feedback_text), feedback_text))
  analyze_button.pack()

  feedback_label = Label(window, textvariable=feedback_text)
  feedback_label.pack()

  # Initialize the first frame of the GIF
  frame = PhotoImage(file='mattel_please_dont_sue_me.gif')
  label = Label(window, image=frame)
  label.pack()

  # Start animating the GIF
  update_frame(0, label, window, 500)

  window.mainloop()

if __name__ == "__main__":
  main()
