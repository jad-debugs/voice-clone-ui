import gradio as gr
from core import preprocess_audio, clone_voice
import os
import time

def process(text: str, ref_audio_path: str) -> str:
    if not text.strip():
        return "Error! Enter some text!"
    if not ref_audio_path:
        return "Error! Upload some audio!"

    # save their cleaned audio file
    cleaned_path = f"cleaned_{int(time.time())}"
    preprocess_audio(ref_audio_path, cleaned_path)