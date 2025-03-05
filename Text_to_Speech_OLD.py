import sys
import random
from google.cloud import texttospeech
from playsound import playsound

def synthesize_speech(mode, output_file, clothing_description=None):
    # Initialize the client
    client = texttospeech.TextToSpeechClient()

    # Prepare the SSML input based on mode
    if mode == "1":
        ssml_text = """
        <speak>
          Hello! How are you <emphasis level="strong">today</emphasis>? 
          I hope you're doing <prosody pitch="+10%">well</prosody>.
        </speak>
        """
    elif mode == "2":
        ssml_text = """
        <speak>
          Good bye! It was <emphasis level="strong">nice</emphasis> meeting you. 
          Have a <emphasis level="strong">great</emphasis> day!
        </speak>
        """
    elif mode == "3" and clothing_description:
        compliments = [
            f"Wow, that {clothing_description} looks absolutely stunning on you!",
            f"I love the combination of colors in your {clothing_description}. It's so stylish!",
            f"Your {clothing_description} makes you look fantastic. What great taste!",
            f"The {clothing_description} is perfect for today. You look amazing!",
            f"That {clothing_description} really brings out your personality. Fantastic choice!"
        ]
        compliment = random.choice(compliments)
        ssml_text = f"""
        <speak>
          {compliment}
        </speak>
        """
    else:
        print("Invalid mode. Use '1' for hello, '2' for goodbye, or '3' for clothing comments.")
        return

    # Set up the input for text-to-speech synthesis
    input_text = texttospeech.SynthesisInput(ssml=ssml_text)

    # Configure the voice settings
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",  # Wavenet voice for more natural sound
    )

    # Configure the audio output settings
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.1,  # Adjust the speaking rate for a more natural sound
        pitch=1.0,          # Adjust the pitch if needed
    )

    # Perform the Text-to-Speech request
    response = client.synthesize_speech(
        input=input_text,
        voice=voice,
        audio_config=audio_config
    )

    # Write the output to an MP3 file
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to "{output_file}"')

def play_audio(file_path):
    # Play the audio file
    playsound(file_path)
    print(f'Playing audio file "{file_path}"')

# Check for command-line arguments
if len(sys.argv) < 2:
    print("Usage: python script.py <mode> [clothing_description]")
    print("Mode '1' for hello, '2' for goodbye, '3' for clothing comments")
else:
    mode = sys.argv[1]
    if mode == "3":
        if len(sys.argv) < 3:
            print("Please provide a clothing description for mode 3.")
        else:
            clothing_description = sys.argv[2]
            synthesize_speech(mode, "output.mp3", clothing_description)
            play_audio("output.mp3")
    else:
        synthesize_speech(mode, "output.mp3")
        play_audio("output.mp3")

