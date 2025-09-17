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
    cleaned_path = f"cleaned_{int(time.time())}.wav"
    preprocess_audio(ref_audio_path, cleaned_path)

    try:
        output_path = clone_voice(text, cleaned_path)
        return "Voice cloned !!!", output_path
    except Exception as e:
        return f"Error! {str(e)}", None

demo = gr.Interface(
    fn=process,
    inputs=[
        gr.Textbox(label="Text", placeholder="Enter text to synthesize...", lines=2),
        gr.Audio(label="Reference Audio", type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Status"),
        gr.Audio(label="Cloned Voice Output")
    ],
    title="XTTS Voice Cloner",
    description="Clone any voice using XTTS! Upload or record a reference sample and enter text."
)

# add notes for whats going in since model will take long on gpu
# tell user to record for at least 15 seconds
# add folder for saved recordings
# make ui look nicer

if __name__ == "__main__":
    demo.launch()