AVNI 2.0 — AI Voice Assistant

AVNI 2.0 is a futuristic AI-powered desktop voice assistant built with Python. It can listen to voice commands, process queries using Google Gemini, respond through speech, and display an interactive holographic-style dashboard.

✨ Features
🎙️ Voice Recognition — Understands spoken commands using SpeechRecognition.
🧠 Google Gemini AI — Generates intelligent responses to user queries.
🔊 Text-to-Speech — Responds naturally using pyttsx3.
🖥️ Futuristic Dashboard — Interactive Tkinter interface with neon/holographic visuals.
👤 AI Character — Animated character integrated into the dashboard.
⚡ Real-Time States — IDLE, LISTENING, THINKING, and SPEAKING states.
🌌 Animations & Effects — Particles, holographic rings, waveform, glowing elements, and animated UI.
🔐 Environment Variables — API keys can be stored securely in a .env file.
🛠️ Technologies Used
Python
Tkinter
Google Gemini API
SpeechRecognition
PyAudio
pyttsx3
Python Dotenv
Pillow (PIL)
📁 Project Structure
AVNI-2.0/
│
├── main.py
├── config.py
├── voice.py
├── gemini_brain.py
├── dashboard.py
├── requirements.txt
├── .env
├── cuteCharacter.webp
└── README.md
⚙️ Installation
1. Clone the repository
git clone https://github.com/RoushanKumar8/AVNI-2.0.git
cd AVNI-2.0
2. Create a virtual environment
python -m venv venv
3. Install dependencies

If PowerShell activation is restricted on Windows, you can directly use the virtual-environment Python:

venv\Scripts\python.exe -m pip install -r requirements.txt

Or, after activating the environment:

pip install -r requirements.txt
🔑 Gemini API Setup

Create a .env file in the project root:

GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash

Replace your_api_key_here with your Google Gemini API key.

⚠️ Never upload your .env file or API key to GitHub.

Add this to .gitignore:

.env
venv/
__pycache__/
▶️ Run AVNI

On Windows:

venv\Scripts\python.exe main.py

If your virtual environment is activated:

python main.py
🎤 Wake Phrase

AVNI can be activated using supported wake phrases such as:

Hey Avni

After activation, speak your command and AVNI will process it using the Gemini AI system.

🖥️ Dashboard States

The dashboard visually represents AVNI's current state:

State	Description
IDLE	Waiting for a voice command
LISTENING	Listening to the user's speech
THINKING	Processing the request
SPEAKING	Responding through voice
🎨 Dashboard

The interface is designed with a futuristic HUD/holographic style, featuring:

Neon cyan and purple UI
Animated grid background
Floating particles
Holographic character
Voice waveform
Status indicators
Quick-action panels
Animated rings and platform
🔧 Troubleshooting
ModuleNotFoundError

Install all dependencies again:

venv\Scripts\python.exe -m pip install -r requirements.txt
PowerShell activation error

If you see:

Activate.ps1 cannot be loaded because running scripts is disabled

You don't need to activate the environment. Simply run:

venv\Scripts\python.exe main.py
PyAudio installation issue

If PyAudio fails to install, make sure you're using a compatible Python version and then try:

venv\Scripts\python.exe -m pip install PyAudio
🚀 Future Improvements
🌐 Web search integration
📂 File and application control
🎵 Music control
🌦️ Live weather information
💬 Conversation history
🎭 More animated AI characters
🎨 Customizable dashboard themes
🔔 Desktop notifications
🖱️ Interactive dashboard buttons
🤝 Contributing

Contributions and ideas are welcome!

Fork the repository
Create a new branch
Make your changes
Commit your changes
Push the branch
Open a Pull Request
📜 License

This project is intended for learning, experimentation, and personal use. Add an appropriate open-source license if you plan to distribute it publicly.

🌌 AVNI 2.0

Your voice. Your assistant. Your AI.

Built with ❤️ using Python + Gemini AI.