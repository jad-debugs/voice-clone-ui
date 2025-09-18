<img width="1276" height="795" alt="image" src="https://github.com/user-attachments/assets/6ea5dcf5-1d56-47c4-94d6-64db43088802" />

# 🎤 XTTS Voice Cloner (Gradio + PyTorch)

Clone any voice using multiple reference samples and synthesize speech with [XTTS](https://github.com/coqui-ai/TTS), all through an intuitive Gradio UI built on top of PyTorch.

## 🚀 Features

- 🎙️ Record and use **multiple reference samples** for better voice cloning  
- 🧼 Automatic audio preprocessing (cleaning, normalizing)  
- 🧠 Real-time voice synthesis using Coqui's XTTS model  
- 🌍 Supports **multi-lingual** text-to-speech (e.g. English, French, Arabic, Chinese)  
- ⚙️ Built with **PyTorch** + **Gradio**

## 📦 Requirements

- Python 3.9 or 3.10  
- `ffmpeg` installed on your system  
- A working GPU (for best performance)

## 🛠 Setup Instructions

### 📁 Clone the repository

```bash
git clone https://github.com/yourusername/xtts-voice-cloner.git
cd xtts-voice-cloner
```
### Virtual Environment
``` bash
python3 -m venv voice-env
source voice-env/bin/activate        # On Windows: .\voice-env\Scripts\activate
```

### Install Dependencies and Run
``` bash
pip install -r requirements.txt
python app.py
```
Once it launches, you'll see a link like this, open either:

Running on local URL: http://127.0.0.1:7860  
Running on public URL: https://your-session.gradio.live
