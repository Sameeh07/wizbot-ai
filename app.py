# import os
# import gradio as gr

# from model import encode_image, analyze_image_with_query
# from patient_voice import record_audio, transcribe_with_groq
# from doctor_voice import text_to_speech_with_gtts, text_to_speech_with_elevenlabs

# #load_dotenv()

# system_prompt="""You have to act as a professional doctor, I know you are not but this is for learning purpose. What's in this image? Do you find anything wrong with it medically? If you make a differential, suggest some remedies for them. Do not add any numbers or special characters in your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.Do not say 'In the image I see' but say 'With what I see, I think you have ....'Don't respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot. Keep your answer concise (max 2 sentences). No preamble, start your answer right away please.If the user asks any questions related to mental health, respond like a professional mental health counselor or therapist. Be empathetic, supportive, and avoid any clinical or robotic tone. Offer comfort, reassurance, and gentle guidance without giving direct medical advice or diagnosis."""


# def process_inputs(audio_filepath, image_filepath):
#     speech_to_text_output = transcribe_with_groq(GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
#                                                  audio_filepath=audio_filepath,
#                                                  stt_model="whisper-large-v3")

#     # Handle the image input
#     if image_filepath:
#         doctor_response = analyze_image_with_query(query=system_prompt+speech_to_text_output, encoded_image=encode_image(image_filepath), model="llama-3.2-11b-vision-preview")
#     else:
#         doctor_response = "No image provided for me to analyze"

#     voice_of_doctor = text_to_speech_with_elevenlabs(input_text=doctor_response, output_filepath="final.mp3") 

#     return speech_to_text_output, doctor_response, voice_of_doctor


# # Create the interface
# iface = gr.Interface(
#     fn=process_inputs,
#     inputs=[
#         gr.Audio(sources=["microphone"], type="filepath"),
#         gr.Image(sources=["upload", "webcam"], type="filepath", label="Upload an image (optional)")
#     ],
#     outputs=[
#         gr.Textbox(label="Speech to Text"),
#         gr.Textbox(label="Doctor's Response"),
#         gr.Audio("Temp.mp3")
#     ],
#     title="WIZCARE AI"
# )
# port = int(os.environ.get("PORT", 7860))
# iface.launch(server_name="0.0.0.0", server_port=port)
# iface.launch(debug=True, share=True)

#http://127.0.0.1:7860
# app.py (main entry for Render deployment)
# app.py (main entry for Render deployment)
import os
import gradio as gr
from dotenv import load_dotenv
from patient_voice import transcribe_with_groq
from doctor_voice import text_to_speech_with_elevenlabs, text_to_speech_with_gtts

# Load environment variables
load_dotenv()

# System prompt for the doctor bot
system_prompt = (
    "You are a professional doctor. Always respond with empathy and medical knowledge. "
    "Keep answers short, clear, and friendly."
)

def process_input(audio_filepath, text_input):
    # Transcribe audio if provided
    transcription = ""
    if audio_filepath:
        transcription = transcribe_with_groq(
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )
    # Combine with typed input
    user_query = f"{transcription} {text_input}".strip()
    # Validate input
    if not user_query:
        return "", "Please speak or type your symptoms/questions.", None

    # Call Groq for doctor response using text-only model
    from groq import Groq
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    chat = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_query}
        ]
    )
    doctor_response = chat.choices[0].message.content

    # Convert doctor response to speech, using ElevenLabs if key provided, else gTTS
    if os.environ.get("ELEVENLABS_API_KEY"):
        audio_out = text_to_speech_with_elevenlabs(
            input_text=doctor_response,
            output_filepath="doctor_response.mp3"
        )
    else:
        audio_out = text_to_speech_with_gtts(
            input_text=doctor_response,
            output_filepath="doctor_response.mp3"
        )

    return transcription, doctor_response, audio_out

# Gradio interface
iface = gr.Interface(
    fn=process_input,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath", label="Speak your symptoms (optional)"),
        gr.Textbox(lines=2, placeholder="Or type your symptoms/questions...", label="Text input (optional)")
    ],
    outputs=[
        gr.Textbox(label="Transcription"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(label="Doctor's Voice Reply")
    ],
    title="WIZCARE AI - Voice & Text Doctor Assistant"
)

# Launch on Render
port = int(os.environ.get("PORT", 7860))
iface.launch(server_name="0.0.0.0", server_port=port)

