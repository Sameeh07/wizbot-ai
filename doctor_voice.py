# import os
# from gtts import gTTS
# from elevenlabs.client import ElevenLabs
# from elevenlabs import save

# ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")


# def text_to_speech_with_gtts(input_text, output_filepath):
#     """Convert text to speech using gTTS and save the output file."""
#     language = "en"
#     tts = gTTS(text=input_text, lang=language, slow=False)
#     tts.save(output_filepath)
#     return output_filepath


# def text_to_speech_with_elevenlabs(input_text, output_filepath):
#     """Convert text to speech using ElevenLabs API and save the output file using Nicole (Legacy) voice."""
#     client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
#     audio = client.generate(
#         text=input_text,
#         voice="Aria",  
#         output_format="mp3_22050_32",
#         model="eleven_turbo_v2"
#     )
#     save(audio, output_filepath)
#     return output_filepath




    # doctor_voice.py

import os
from gtts import gTTS
from elevenlabs.client import ElevenLabs
from elevenlabs import save
from elevenlabs.core.api_error import ApiError

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

def text_to_speech_with_gtts(input_text, output_filepath):
    """Convert text to speech using gTTS and save the output file."""
    language = "en"
    tts = gTTS(text=input_text, lang=language, slow=False)
    tts.save(output_filepath)
    return output_filepath


def text_to_speech_with_elevenlabs(input_text, output_filepath):
    """Convert text to speech using ElevenLabs API and save the output file, with fallback to gTTS if unauthorized."""
    # Attempt ElevenLabs TTS
    try:
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        audio = client.generate(
            text=input_text,
            voice="Aria",  # Nicole (Legacy) voice ID
            output_format="mp3_22050_32",
            model="eleven_turbo_v2"
        )
        save(audio, output_filepath)
        return output_filepath
    except ApiError as e:
        # Fallback to gTTS if ElevenLabs fails (e.g., free tier disabled)
        print(f"ElevenLabs API error ({e.status_code}): {e.body}. Falling back to gTTS.")
        return text_to_speech_with_gtts(input_text, output_filepath)
    except Exception as e:
        # General fallback
        print(f"Error in ElevenLabs TTS: {e}. Falling back to gTTS.")
        return text_to_speech_with_gtts(input_text, output_filepath)
