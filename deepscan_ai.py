import streamlit as st
import google.generativeai as genai_legacy
import yt_dlp
import os
import time
from fpdf import FPDF

# Safe Import for MoviePy (Works with v1.x and v2.x)
try:
    from moviepy.editor import VideoFileClip
except ImportError:
    from moviepy import VideoFileClip

# 1. Page Configuration & UI Styling
st.set_page_config(page_title="DeepScan AI", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
    }
    .report-box {
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #007bff;
        background-color: white;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar: Developer Info & API Key
with st.sidebar:
    st.title("🛡️ DeepScan AI")
    st.info("Detecting AI-generated Video and Audio content.")
    
    st.markdown("---")
    st.subheader("Developer Profiles")
    # Replace these with your actual links
    st.markdown("[🔗 LinkedIn](https://www.linkedin.com/in/unni-r-b09398a7/)")
    st.markdown("[💻 GitHub](https://github.com/archanaunni-eloor)")
    
    st.markdown("---")
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    st.warning("Your API key is used only for the current session.")

# 3. Main Application
if api_key:
    genai_legacy.configure(api_key=api_key)
    
    st.title("🛡️ DeepScan AI: Multi-Modal Deepfake Detector")

    # Initialize Session States
    if "visual_report" not in st.session_state: st.session_state.visual_report = None
    if "audio_report" not in st.session_state: st.session_state.audio_report = None
    if "video_ready" not in st.session_state: st.session_state.video_ready = False

    # Input Selection
    option = st.radio("Select Input Method:", ("Upload Video", "YouTube Link (Server Restricted)"))
    video_path = "temp_video.mp4"

    if option == "Upload Video":
        uploaded_file = st.file_uploader("Choose a video...", type=["mp4", "mov", "avi"])
        if uploaded_file:
            with open(video_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.session_state.video_ready = True

    elif option == "YouTube Link (Server Restricted)":
        st.warning("⚠️ **Note:** Due to YouTube's strict anti-bot policies on shared cloud servers, this feature is temporarily disabled in the live demo. Please use the **'Upload Video'** option to test the app.")
        st.info("Direct YouTube analysis works perfectly on Localhost or Private Servers with dedicated IPs.")

    # --- Analysis & Result Section ---
    if st.session_state.video_ready and os.path.exists(video_path):
        st.video(video_path)
        
        if st.button("Run Visual Analysis"):
            try:
                with st.spinner("Analyzing visuals..."):
                    # Using the exact model name that worked yesterday
                    model = genai_legacy.GenerativeModel(model_name='models/gemini-flash-latest')
                    video_file = genai_legacy.upload_file(path=video_path)
                    while video_file.state.name == "PROCESSING":
                        time.sleep(2)
                        video_file = genai_legacy.get_file(video_file.name)
                    
                    prompt = "Analyze this video for AI Deepfake markers. Provide an AI Probability Score (0-100%)."
                    response = model.generate_content([video_file, prompt])
                    st.session_state.visual_report = response.text
            except Exception as e:
                if "429" in str(e):
                    st.error("Daily Quota Exceeded. Please try later.")
                else:
                    st.error(f"Visual Error: {e}")

    # Display Dashboard & PDF Button
    if st.session_state.visual_report:
        st.markdown("---")
        
        # Calculate Verdict Score
        v_score = 0
        try: v_score = int(st.session_state.visual_report.split("Score:")[1].split("%")[0].strip())
        except: v_score = 0
        
        a_score = 0
        if st.session_state.audio_report:
            try: a_score = int(st.session_state.audio_report.split("Score:")[1].split("%")[0].strip())
            except: a_score = 0
            
        final_risk = max(v_score, a_score)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if final_risk > 70: st.error(f"🔴 **Final Verdict: High Risk ({final_risk}% AI Probability)**")
            elif final_risk > 30: st.warning(f"🟡 **Final Verdict: Suspicious ({final_risk}% AI Probability)**")
            else: st.success(f"🟢 **Final Verdict: Low Risk ({final_risk}% AI Probability)**")
        
        with col2:
            # --- പകരമായി ഈ ഭാഗം ഉപയോഗിക്കുക ---
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="DeepScan AI - Report", ln=True, align='C')
            pdf.set_font("Arial", size=10)
            pdf.ln(10)
            
            # വിഷ്വൽ റിപ്പോർട്ടിലെ സ്പെഷ്യൽ ക്യാരക്ടറുകൾ മാറ്റുന്നു
            v_report_safe = st.session_state.visual_report.encode('latin-1', 'ignore').decode('latin-1')
            pdf.multi_cell(0, 5, txt=f"Visual Report:\n{v_report_safe}")
            
            if st.session_state.audio_report:
                # ഓഡിയോ റിപ്പോർട്ടിലെ സ്പെഷ്യൽ ക്യാരക്ടറുകൾ മാറ്റുന്നു
                a_report_safe = st.session_state.audio_report.encode('latin-1', 'ignore').decode('latin-1')
                pdf.ln(5)
                pdf.multi_cell(0, 5, txt=f"Audio Report:\n{a_report_safe}")
            
            # PDF ഔട്ട്പുട്ട് എടുക്കുന്നു
            pdf_out = pdf.output(dest='S').encode('latin-1', 'ignore')
            st.download_button("📥 Download Report", pdf_out, "DeepScan_Report.pdf", "application/pdf")

        # Visual Report Display
        st.subheader("📊 Detailed Visual Report")
        st.markdown(f'<div class="report-box">{st.session_state.visual_report}</div>', unsafe_allow_html=True)

        # Audio Section
        st.markdown("---")
        st.subheader("🎧 Audio Deepfake Analysis")
        if st.session_state.audio_report:
            st.markdown(f'<div class="report-box">{st.session_state.audio_report}</div>', unsafe_allow_html=True)
        else:
            if st.button("Analyze Audio Track"):
                with st.spinner("Processing audio..."):
                    try:
                        clip = VideoFileClip(video_path)
                        if clip.audio is None:
                            st.warning("No audio found.")
                        else:
                            audio_out = "temp_audio.mp3"
                            clip.audio.write_audiofile(audio_out, logger=None)
                            # Fixed model name for audio as well
                            model = genai_legacy.GenerativeModel(model_name='models/gemini-flash-latest')
                            audio_file = genai_legacy.upload_file(path=audio_out)
                            res = model.generate_content([audio_file, "Analyze for AI voice cloning. Provide AI Confidence Score."])
                            st.session_state.audio_report = res.text
                            clip.close()
                            st.rerun()
                    except Exception as ae:
                        # --- Custom Quota Error Handling ---
                        if "429" in str(ae) or "quota" in str(ae).lower():
                            st.error("⚠️ Daily API Limit Reached: You have reached the maximum number of free requests for today. Please try again later or use a different API key.")
                        else:
                            st.error(f"Audio Analysis Error: {ae}")
else:
    st.info("Enter your Gemini API Key in the sidebar to start.")
