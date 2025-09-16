import sounddevice as sd
import soundfile as sf
from scipy.io.wavfile import write

def record_voice(filename='my_voice.wav', duration=5, samplerate=16000) -> str:
    print('Recording Started...')

    voice_recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()
    write(filename, samplerate, voice_recording)
    print(f'Saved voice recording as {filename}')
    return filename

def clone_voice(text: str, reference_audio_path: str, output_dir="cloned_output") -> str:
    return ""

if __name__ == "__main__":
    refrence_path = record_voice()

    text_to_speak = "Hello World! This is your cloned voice using pytorch and yourtts"
