🛡️ DeepScan AI: Multi-Modal Deepfake Detector
DeepScan AI is a professional-grade forensic tool designed to identify AI-generated or manipulated video and audio content. By leveraging the power of Google's Gemini 1.5 Flash model, the application provides a comprehensive analysis of visual consistency and audio authenticity.

🚀 Features
Visual Forensic Analysis: Detects unnatural skin textures, static expressions, and irregular lighting often found in AI-generated videos.

Audio Deepfake Detection: Analyzes voice tracks for signs of AI cloning, robotic prosody, and synthetic artifacts.

Multi-Modal Verdict: Combines both visual and audio data to provide a final AI Probability Score.

YouTube Integration: Directly analyze videos using a YouTube URL.

Professional PDF Reports: Generate and download detailed forensic reports for documentation.

🛠️ Technology Stack
Framework: Streamlit

AI Engine: Google Gemini API (Generative AI)

Video Processing: yt-dlp, MoviePy

Report Generation: FPDF

Language: Python

📋 Prerequisites
To run this project, you will need:

Python 3.9 or higher.

A Google Gemini API Key (Get it from Google AI Studio).

⚙️ Installation & Setup
Clone the Repository:

Bash
git clone https://github.com/your-username/DeepScan-AI.git
cd DeepScan-AI
Install Dependencies:

Bash
pip install -r requirements.txt
Run the Application:

Bash
streamlit run deepscan_ai.py
📖 How to Use
Launch the app and enter your Gemini API Key in the sidebar.

Choose an input method: Upload a Video or Paste a YouTube Link.

Click "Run Visual Analysis" to start the frame-by-frame check.

Once the visual report is ready, click "Analyze Audio Track" to check for voice cloning.

View the Final Verdict Dashboard and download the PDF Forensic Report.

🛡️ Disclaimer
This tool is intended for educational and research purposes. While it uses advanced AI models for detection, it should be used as a supportive tool alongside human judgment for verifying content authenticity.

👤 Developer
Unni R

[LinkedIn](https://www.linkedin.com/in/unni-r-b09398a7/)

[GitHub](https://github.com/archanaunni-eloor)
