import sounddevice as sd
import soundfile as sf
from scipy.io.wavfile import write

def record_voice(filename='my_voice.wav', duration=5, samplerate=16000):
    print('Recording Started...')

    voice_recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()
    write(filename, samplerate, recording)
    print(f'Saved voice recording as {filename}')
    return filename