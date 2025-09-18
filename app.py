import gradio as gr
from core import preprocess_audio, clone_voice
import os
import time

os.makedirs("recordings", exist_ok=True)

recorded_refs = []

def add_recording(new_record):
    if not new_record:
        return recorded_refs, "No recording detected!"
    timestamp = int(time.time())
    path = f"recordings/recorded_{timestamp}.wav"
    os.rename(new_record, path)
    recorded_refs.append(path)
    return recorded_refs, f"Added: {os.path.basename(path)}"

def reset_session():
    recorded_refs.clear()
    return [], "🧹 Cleared all recorded samples."

def process(text: str, ref_audio_paths: list, language:str) -> str:
    if not text.strip():
        return "Error! Enter some text!", None
    if not ref_audio_paths:
        return "Error! Upload some audio!", None

    status = "Preprocessing audio..."

    # save their cleaned audio files
    try:
        cleaned_paths = []
        for path in ref_audio_paths:
            cleaned_path = f"recordings/cleaned_{int(time.time())}.wav"
            preprocess_audio(path, cleaned_path)
            cleaned_paths.append(cleaned_path)

        status = "🧠 Cloning voice using XTTS (this may take ~60s)..."
        output_path = clone_voice(text, cleaned_paths, lang=language)
        return "Voice cloned successfully!", output_path
    except Exception as e:
        return f"Error! {str(e)}", None

with gr.Blocks(title="XTTS Voice Cloner") as demo:
    gr.Markdown("Multi-Sample Voice Cloner with XTTS")
    gr.Markdown("Record multiple voice samples and synthesize a sentence in that voice using PyTorch + XTTS.")

    text_input = gr.Textbox(label="Text to Synthesize", placeholder="Enter sentence...", lines=2)

    with gr.Row():
        audio_input = gr.Audio(label="Record a Sample", type="filepath")
        add_btn = gr.Button("➕ Add Sample")
        clear_btn = gr.Button("🧹 Clear Samples")

    status_box = gr.Textbox(label="Recording Status")
    recordings_list = gr.JSON(label="Recorded Samples")

    add_btn.click(fn=add_recording, inputs=audio_input, outputs=[recordings_list, status_box])
    clear_btn.click(fn=reset_session, outputs=[recordings_list, status_box])

    lang_dropdown = gr.Dropdown(
        choices=["en", "es", "fr", "de", "it", "ar", "zh-cn"],
        value="en",
        label="Language"
    )

    with gr.Row():
        clone_btn = gr.Button("🚀 Clone Voice")
        result_box = gr.Textbox(label="Result Status")
        result_audio = gr.Audio(label="Output")

    clone_btn.click(fn=process, inputs=[text_input, recordings_list, lang_dropdown], outputs=[result_box, result_audio])

if __name__ == "__main__":
    demo.launch(share=True)