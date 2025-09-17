import os
import uuid
import sounddevice as sd
from scipy.io.wavfile import write

import torch
from TTS.config.shared_configs import BaseDatasetConfig
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig
from TTS.tts.models.xtts import XttsArgs

torch.serialization.add_safe_globals({
    BaseDatasetConfig,
    XttsConfig,
    XttsAudioConfig,
    XttsArgs
})

from TTS.api import TTS
import soundfile as sf
import librosa

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False)

# tts.to(device)

# Allowlist required classes
os.environ["COQUI_TOS_AGREED"] = "1"



def preprocess_audio(input_path, output_path):
    y, sr = librosa.load(input_path, sr=22050)
    y, _ = librosa.effects.trim(y, top_db=20)  # trim silence
    y = librosa.util.normalize(y)              # normalize
    sf.write(output_path, y, sr)

def record_voice(filename='my_voice.wav', duration=5, samplerate=22050) -> str:
    print('Recording Started...')

    voice_recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()
    write(filename, samplerate, voice_recording)
    print(f'Saved voice recording as {filename}')
    return filename

def clone_voice(text: str, reference_audio_path: str, output_dir="cloned_outputs") -> str:
    # initilizing model tts
    from TTS.api import TTS  # Re-import to force reload (optional but safe)

    # Re-initialize TTS model (ensures clean session)
    tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False)
    tts.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
    # make directory which will save cloned voice
    os.makedirs(output_dir, exist_ok=True)

    # f"cloned_{uuid.uuid4().hex[:8]}.wav" 
    output_path = os.path.join(output_dir, "cloned_voice.wav")

    tts.tts_to_file(
        text = text,
        speaker_wav = reference_audio_path,
        language='en',
        file_path=output_path,
    )

    # saving cloned voice
    #sf.write(output_path, cloned_voice, tts.synthesizer.output_sample_rate)
    print('saved cloned voice')
    return output_path

if __name__ == "__main__":
    reference_path = record_voice(duration=10)

    cleaned_reference_path = "cleaned_reference.wav"
    preprocess_audio(reference_path, cleaned_reference_path)

    text_to_speak = "Hey, this is Jad—I'm just testing out this voice clone project to see how real it sounds."

    output_path = clone_voice(text_to_speak, cleaned_reference_path)
