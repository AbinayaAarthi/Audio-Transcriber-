# app.py

import gradio as gr
import openai
import os

# Set your OpenAI key (ideally from environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Core function to transcribe and detect tone
def transcribe_and_analyze(audio):
    try:
        # Transcription using Whisper API
        transcript = openai.Audio.transcribe("whisper-1", audio)["text"]

        # Very simple tone detection logic (you can expand this)
        if any(word in transcript.lower() for word in ["okay", "confident", "sure"]):
            sentiment = "Calm/Confident"
        elif any(word in transcript.lower() for word in ["uh", "um", "maybe", "not sure"]):
            sentiment = "Nervous/Uncertain"
        else:
            sentiment = "Neutral"

        return transcript, sentiment
    except Exception as e:
        return str(e), "Error"

# Gradio Interface
interface = gr.Interface(
    fn=transcribe_and_analyze,
    inputs=gr.Audio(source="microphone", type="filepath", label="Speak or Upload Audio"),
    outputs=[
        gr.Textbox(label="Transcription"),
        gr.Textbox(label="Estimated Sentiment"),
    ],
    title="🎤 Audio Transcriber with Sentiment Analysis",
    description="Record your voice to transcribe speech and estimate tone for applications like loan pre-screening or emotion recognition.",
    theme="default"
)

# Launch
if __name__ == "__main__":
    interface.launch()
