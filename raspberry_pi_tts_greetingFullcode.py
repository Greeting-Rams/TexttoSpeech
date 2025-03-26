
import sys
import random
import time
import pygame
from google.cloud import texttospeech

# Initialize the Text-to-Speech client
client = texttospeech.TextToSpeechClient()

def synthesize_speech(text, output_file="output.mp3"):
    """Synthesizes speech from the input text and saves it to an MP3 file."""
    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.1,
        pitch=1.0
    )

    response = client.synthesize_speech(
        input=input_text,
        voice=voice,
        audio_config=audio_config
    )

    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to "{output_file}"')

def play_audio(file_path="output.mp3"):
    """Plays the audio file using pygame (best for Raspberry Pi)."""
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    print(f'Finished playing "{file_path}"')

def detect_clothing_color():
    """Simulates the detection of clothing color."""
    colors = ["red", "blue", "green", "yellow", "black", "white"]
    print("Simulating color detection...")
    detected_color = random.choice(colors)
    print(f"Detected clothing color: {detected_color}")
    return detected_color

def generate_greeting(clothing_color):
    greetings = [
        f"Hello! Welcome to our building. I see you're wearing {clothing_color}. It looks great on you!",
        f"Hi there! I love your {clothing_color} outfit. Welcome to our store!",
        f"Welcome! Your {clothing_color} clothing is so stylish. Enjoy your visit!",
        f"Hello! That {clothing_color} outfit is fantastic. Welcome to our mall!",
        f"Hi! Your {clothing_color} clothing is stunning. Let us know if you need any help."
    ]
    return random.choice(greetings)

def generate_farewell():
    farewells = [
        "Goodbye! Thank you for visiting us. Have a great day!",
        "See you later! We hope to see you again soon.",
        "Thank you for shopping with us. Goodbye!",
        "Have a wonderful day! Goodbye!",
        "Goodbye! Take care and come back soon."
    ]
    return random.choice(farewells)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 script.py <mode>")
        print("Mode '1' for greeting, '2' for farewell")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "1":
        clothing_color = detect_clothing_color()
        greeting = generate_greeting(clothing_color)
        print("Generating greeting...")
        synthesize_speech(greeting)
        play_audio()
    elif mode == "2":
        farewell = generate_farewell()
        print("Generating farewell...")
        synthesize_speech(farewell)
        play_audio()
    else:
        print("Invalid mode. Use '1' for greeting or '2' for farewell.")

if __name__ == "__main__":
    main()
