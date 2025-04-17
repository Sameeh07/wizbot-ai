import os
from gtts import gTTS
from elevenlabs.client import ElevenLabs
from elevenlabs import save

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")


def text_to_speech_with_gtts(input_text, output_filepath):
    """Convert text to speech using gTTS and save the output file."""
    language = "en"
    tts = gTTS(text=input_text, lang=language, slow=False)
    tts.save(output_filepath)
    return output_filepath


def text_to_speech_with_elevenlabs(input_text, output_filepath):
    """Convert text to speech using ElevenLabs API and save the output file using Nicole (Legacy) voice."""
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=input_text,
        voice="piTKgcLEGmPE4e6mEKli",  # Nicole (Legacy) voice ID
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )
    save(audio, output_filepath)
    return output_filepath