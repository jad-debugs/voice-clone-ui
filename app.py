import os
import uuid
import torch
import sounddevice as sd
from scipy.io.wavfile import write
from TTS.api import TTS
import soundfile as sf

def record_voice(filename='my_voice.wav', duration=5, samplerate=16000) -> str:
    print('Recording Started...')

    voice_recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()
    write(filename, samplerate, voice_recording)
    print(f'Saved voice recording as {filename}')
    return filename

def clone_voice(text: str, reference_audio_path: str, output_dir="cloned_outputs") -> str:
    # initilizing model tts
    tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=True)

    # make directory which will save cloned voice
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"cloned_{uuid.uuid4().hex[:8]}.wav")

    cloned_voice = tts.tts_with_vc(
        text = text,
        speaker_wav = reference_audio_path,
        speaker = 'random',
        language="en"
    )

    # saving cloned voice
    sf.write(output_path, cloned_voice, tts.synthesizer.output_sample_rate)
    print('saved cloned voice')
    return output_path

if __name__ == "__main__":
    reference_path = record_voice()

    text_to_speak = "Hello World! This is your cloned voice using pytorch and yourtts"

    output_path = clone_voice(text_to_speak, reference_path)
