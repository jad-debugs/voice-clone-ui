import gradio as gr
from core import preprocess_audio, clone_voice
import os
import time

os.makedirs("recordings", exist_ok=True)

def process(text: str, ref_audio_paths: list, language:str) -> str:
    if not text.strip():
        return "Error! Enter some text!"
    if not ref_audio_paths:
        return "Error! Upload some audio!"

    status = "Preprocessing audio..."

    # save their cleaned audio files
    cleaned_paths = []
    for path in ref_audio_paths:
        cleaned_path = f"recordings/cleaned_{int(time.time())}.wav"
        preprocess_audio(path, cleaned_path)
        cleaned_paths.append(cleaned_path)


    try:
        status = "Cloning voice using XTTS (this may take up to 60s)..."
        output_path = clone_voice(text, cleaned_path, lang=language)
        return "Voice cloned !", output_path
    except Exception as e:
        return f"Error! {str(e)}", None

demo = gr.Interface(
    fn=process,
    inputs=[
        gr.Textbox(
            label="Text", 
            placeholder="Enter text to synthesize...", 
            lines=2
        ),
        gr.Radio(
            choices=["Upload", "Record"],
            value="Upload",
            label="Input Mode"
        ),
        gr.File(
            file_types=[".wav", ".mp3", ".m4a"],
            label="Upload Reference Audio Samples (Multiple Supported)",
            file_count="multiple",
            visible=True,
            elem_id="upload_input"
        ),
        gr.Audio(
            label="Record Reference Audio (15s+ recommended)",
            type="filepath",
            visible=False,
            elem_id="record_input"
        ),
        gr.Dropdown(
            label="Language",
            choices=["en", "es", "fr", "de", "it", "ar", "zh-cn"],
            value="en",
            interactive=True,
            info="Select the language of the voice you're cloning."
        )
    ],
    outputs=[
        gr.Textbox(label="Status"),
        gr.Audio(label="Cloned Voice Output")
    ],
    title="Voice Cloner",
    description=("Clone any voice using [XTTS](https://github.com/coqui-ai/TTS) powered by PyTorch!\n"
        "➤ Upload or record a sample of the voice (at least 15 seconds recommended).\n"
        "➤ Type the message you want it to say.\n"
        "➤ Hit **Clone Voice** and wait ~30s for magic to happen!"
    ),
)

if __name__ == "__main__":
    demo.launch(share=True)