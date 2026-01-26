import streamlit as st
import time
from backend import workflow
import os

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Project Documentation Generator",
    page_icon="📄",
    layout="wide"
)

# -----------------------------
# Custom CSS Styling - Dark Theme
# -----------------------------
st.markdown("""
<style>
    /* Import Modern Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Dark Background with Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 25%, #24243e 50%, #0f0c29 75%, #1a1a2e 100%);
        animation: gradientShift 15s ease infinite;
        background-size: 400% 400%;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Floating Particles Animation */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 15% 20%, rgba(138, 43, 226, 0.12) 0%, transparent 50%),
            radial-gradient(circle at 85% 80%, rgba(75, 0, 130, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(72, 61, 139, 0.06) 0%, transparent 60%),
            radial-gradient(circle at 70% 30%, rgba(123, 104, 238, 0.1) 0%, transparent 40%);
        animation: float 20s ease-in-out infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    /* Main Container */
    .main .block-container {
        max-width: 950px;
        padding: 3rem 2rem;
        position: relative;
        z-index: 1;
    }
    
    /* All text color fix */
    .stApp, .stApp * {
        color: #e0e0e0;
    }
    
    /* Header Title with Dark Glow */
    h1 {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #a78bfa 0%, #c084fc 50%, #e879f9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.03em;
        padding: 1rem 0;
        filter: drop-shadow(0 0 40px rgba(167, 139, 250, 0.5));
        animation: titleGlow 3s ease-in-out infinite;
    }
    
    @keyframes titleGlow {
        0%, 100% { filter: drop-shadow(0 0 40px rgba(167, 139, 250, 0.5)); }
        50% { filter: drop-shadow(0 0 60px rgba(192, 132, 252, 0.7)); }
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #c4b5fd !important;
        margin-bottom: 3rem;
        line-height: 1.7;
        font-weight: 400;
        text-shadow: 0 2px 15px rgba(167, 139, 250, 0.3);
    }
    
    /* Dark Glassmorphism Card */
    .card {
        background: rgba(30, 30, 50, 0.4) !important;
        backdrop-filter: blur(30px) saturate(180%);
        -webkit-backdrop-filter: blur(30px) saturate(180%);
        border-radius: 28px;
        padding: 3rem;
        box-shadow: 
            0 8px 32px 0 rgba(0, 0, 0, 0.6),
            0 0 60px 0 rgba(123, 104, 238, 0.2),
            inset 0 0 0 1px rgba(167, 139, 250, 0.2);
        margin-bottom: 2rem;
        border: 1px solid rgba(167, 139, 250, 0.2);
        animation: cardFloat 6s ease-in-out infinite;
    }
    
    @keyframes cardFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    
    /* Labels with Dark Gradient */
    .label {
        font-size: 1.05rem;
        font-weight: 700;
        background: linear-gradient(135deg, #e0e0e0 0%, #c4b5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.7rem;
        letter-spacing: 0.03em;
        display: block;
        padding: 0.5rem 0;
    }
    
    /* Helper Text */
    .helper {
        font-size: 0.95rem;
        color: #9ca3af !important;
        margin-top: 0.7rem;
        font-style: italic;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
    }
    
    /* Input Fields - Dark Glassmorphism */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(30, 30, 50, 0.6) !important;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(167, 139, 250, 0.3) !important;
        border-radius: 16px !important;
        color: #e0e0e0 !important;
        font-size: 1.05rem !important;
        padding: 0.9rem 1.2rem !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: rgba(167, 139, 250, 0.6) !important;
        box-shadow: 
            0 0 0 4px rgba(167, 139, 250, 0.15),
            0 8px 25px rgba(123, 104, 238, 0.4) !important;
        background: rgba(30, 30, 50, 0.8) !important;
        outline: none !important;
        transform: translateY(-2px);
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: rgba(156, 163, 175, 0.6) !important;
        opacity: 1 !important;
    }
    
    /* Select Boxes - Dark Glassmorphism */
    .stSelectbox > div > div > div {
        background: rgba(30, 30, 50, 0.6) !important;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(167, 139, 250, 0.3) !important;
        border-radius: 16px !important;
        color: #e0e0e0 !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div > div:hover {
        border-color: rgba(167, 139, 250, 0.5) !important;
        background: rgba(30, 30, 50, 0.8) !important;
        transform: translateY(-2px);
    }
    
    .stSelectbox label {
        color: #e0e0e0 !important;
    }
    
    .stSelectbox svg {
        fill: #a78bfa !important;
    }
    
    /* Dropdown menu - Dark Theme */
    div[data-baseweb="popover"] {
        background: rgba(20, 20, 35, 0.98) !important;
        backdrop-filter: blur(20px);
        border-radius: 12px !important;
        border: 1px solid rgba(167, 139, 250, 0.3) !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6);
    }
    
    div[data-baseweb="popover"] li {
        background: transparent !important;
        color: #e0e0e0 !important;
        transition: all 0.2s ease !important;
    }
    
    div[data-baseweb="popover"] li:hover {
        background: rgba(167, 139, 250, 0.2) !important;
        transform: translateX(5px);
    }
    
    /* Radio Buttons - Dark Pills */
    .stRadio > div {
        background: rgba(30, 30, 50, 0.4) !important;
        padding: 0.6rem !important;
        border-radius: 16px !important;
        border: 1px solid rgba(167, 139, 250, 0.2) !important;
    }
    
    .stRadio > label {
        color: #e0e0e0 !important;
        font-weight: 700 !important;
    }
    
    .stRadio div[role="radiogroup"] label {
        background: rgba(30, 30, 50, 0.6) !important;
        color: #e0e0e0 !important;
        padding: 0.7rem 1.5rem !important;
        border-radius: 12px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-weight: 600 !important;
        margin: 0.2rem !important;
        border: 1px solid rgba(167, 139, 250, 0.2) !important;
    }
    
    .stRadio div[role="radiogroup"] label:hover {
        background: rgba(167, 139, 250, 0.2) !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(167, 139, 250, 0.3);
        border-color: rgba(167, 139, 250, 0.4) !important;
    }
    
    .stRadio div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] p {
        color: #e0e0e0 !important;
    }
    
    /* Radio button circle */
    .stRadio input[type="radio"] {
        accent-color: #a78bfa !important;
    }
    
    /* Dark Gradient Button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 50%, #c084fc 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 1.2rem 2.5rem !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.05em !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 
            0 15px 35px rgba(124, 58, 237, 0.4),
            0 5px 15px rgba(0, 0, 0, 0.3),
            0 0 40px rgba(167, 139, 250, 0.3),
            inset 0 0 0 1px rgba(255, 255, 255, 0.1) !important;
        cursor: pointer !important;
        height: auto !important;
        text-transform: uppercase;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 
            0 20px 50px rgba(124, 58, 237, 0.6),
            0 0 60px rgba(167, 139, 250, 0.5),
            inset 0 0 0 1px rgba(255, 255, 255, 0.2) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-2px) scale(1.01) !important;
    }
    
    .stButton > button p {
        color: white !important;
        font-size: 1.15rem !important;
        position: relative;
        z-index: 1;
    }
    
    /* Success Message - Dark Theme */
    .stSuccess {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(22, 163, 74, 0.1) 100%) !important;
        border: 2px solid #22c55e !important;
        border-radius: 16px !important;
        padding: 1.2rem !important;
        box-shadow: 0 8px 25px rgba(34, 197, 94, 0.2);
        animation: successPulse 2s ease-in-out;
    }
    
    @keyframes successPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .stSuccess p, .stSuccess div {
        color: #86efac !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
    }
    
    /* Error Message - Dark Theme */
    .stError {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.1) 100%) !important;
        border: 2px solid #ef4444 !important;
        border-radius: 16px !important;
        padding: 1.2rem !important;
        box-shadow: 0 8px 25px rgba(239, 68, 68, 0.2);
    }
    
    .stError p, .stError div {
        color: #fca5a5 !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
    }
    
    /* Spinner - Dark Theme */
    .stSpinner > div {
        border-top-color: #a78bfa !important;
        border-right-color: #c084fc !important;
    }
    
    .stSpinner > div > div {
        color: #e0e0e0 !important;
        font-weight: 600 !important;
    }
    
    /* Columns */
    [data-testid="column"] {
        padding: 0 0.5rem;
    }
    
    /* Scrollbar - Dark Styled */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 30, 50, 0.3);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%);
        border-radius: 10px;
        border: 2px solid rgba(167, 139, 250, 0.2);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #a78bfa 0%, #c084fc 100%);
    }
    
    /* Glow effect on card hover */
    .card:hover {
        box-shadow: 
            0 8px 32px 0 rgba(0, 0, 0, 0.6),
            0 0 80px 0 rgba(123, 104, 238, 0.3),
            inset 0 0 0 1px rgba(167, 139, 250, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown("<h1>AI Project Documentation Generator</h1>", unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Generate professional project documentation instantly<br>'
    'using AI. Just provide a topic or context.</div>',
    unsafe_allow_html=True
)

# -----------------------------
# Main Card Container
# -----------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

# Input Mode
st.markdown('<div class="label">Choose Input Mode</div>', unsafe_allow_html=True)
input_mode = st.radio(
    "input_mode",
    ["Generate from Topic", "Generate from Context"],
    horizontal=True,
    label_visibility="collapsed"
)
if input_mode=="Generate from Topic":
    final_user="topic"
else:
    final_user="context"

# Project Input
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="label">Project Topic</div>', unsafe_allow_html=True)

if input_mode == "Generate from Topic":
    project_input = st.text_input(
        "project_input",
        placeholder="e.g. AI-based Resume Screening System",
        label_visibility="collapsed"
    )
    st.markdown(
        '<div class="helper">'
        '💡 Enter a brief project name or topic. The AI will expand it into full documentation.'
        '</div>',
        unsafe_allow_html=True
    )
else:
    project_input = st.text_area(
        "project_context",
        placeholder="Describe the project goals, features, tech stack, constraints, etc.",
        height=180,
        label_visibility="collapsed"
    )
    st.markdown(
        '<div class="helper">'
        '💡 Provide detailed context for more accurate and comprehensive documentation.'
        '</div>',
        unsafe_allow_html=True
    )

# Dropdowns
st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="label">Documentation Tone</div>', unsafe_allow_html=True)
    tone = st.selectbox(
        "tone",
        ["Industry Professional", "Technical", "Academic", "Startup"],
        label_visibility="collapsed"
    )

with col2:
    st.markdown('<div class="label">Output Format</div>', unsafe_allow_html=True)
    output_format = st.selectbox(
        "format",
        ["Word Document (.docx)", "PDF Report (.pdf)", "Markdown (.md)"],
        label_visibility="collapsed"
    )

# Generate Button
st.markdown("<br><br>", unsafe_allow_html=True)

if st.button("✨ Generate Documentation", use_container_width=True):
    if project_input:
        with st.spinner("🤖 AI is crafting your documentation..."):
            if final_user=="topic":
                result=workflow.invoke({"topic":project_input,"tone":tone})
                done=True
            else:
                
                result=workflow.invoke({"context":project_input,"tone":tone})
                done=True
        if done:
            st.success("✅ Documentation generated successfully! Ready for download.")

            # Add some spacing
            st.markdown("<br>", unsafe_allow_html=True)

            # Custom styled download button
            with open(result["file_path"], "rb") as f:
                st.markdown("""
                <style>
                /* Download Button Styling */
                .stDownloadButton > button {
                    width: 100%;
                    background: linear-gradient(135deg, #10b981 0%, #059669 50%, #047857 100%) !important;
                    color: white !important;
                    border: none !important;
                    border-radius: 16px !important;
                    padding: 1.3rem 2.5rem !important;
                    font-size: 1.2rem !important;
                    font-weight: 700 !important;
                    letter-spacing: 0.05em !important;
                    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
                    box-shadow: 
                        0 15px 35px rgba(16, 185, 129, 0.4),
                        0 5px 15px rgba(0, 0, 0, 0.3),
                        0 0 40px rgba(52, 211, 153, 0.3),
                        inset 0 0 0 1px rgba(255, 255, 255, 0.1) !important;
                    cursor: pointer !important;
                    height: auto !important;
                    text-transform: uppercase;
                    position: relative;
                    overflow: hidden;
                    margin-top: 1rem !important;
                }
                
                .stDownloadButton > button::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: -100%;
                    width: 100%;
                    height: 100%;
                    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
                    transition: left 0.6s;
                }
                
                .stDownloadButton > button:hover::before {
                    left: 100%;
                }
                
                .stDownloadButton > button:hover {
                    transform: translateY(-4px) scale(1.02) !important;
                    box-shadow: 
                        0 20px 50px rgba(16, 185, 129, 0.6),
                        0 0 60px rgba(52, 211, 153, 0.5),
                        0 0 80px rgba(34, 197, 94, 0.4),
                        inset 0 0 0 1px rgba(255, 255, 255, 0.2) !important;
                }
                
                .stDownloadButton > button:active {
                    transform: translateY(-2px) scale(1.01) !important;
                }
                
                .stDownloadButton > button p {
                    color: white !important;
                    font-size: 1.2rem !important;
                    position: relative;
                    z-index: 1;
                    margin: 0 !important;
                }
                
                /* Download icon animation */
                .stDownloadButton > button:hover {
                    animation: downloadPulse 1.5s ease-in-out infinite;
                }
                
                @keyframes downloadPulse {
                    0%, 100% { 
                        box-shadow: 
                            0 20px 50px rgba(16, 185, 129, 0.6),
                            0 0 60px rgba(52, 211, 153, 0.5);
                    }
                    50% { 
                        box-shadow: 
                            0 20px 50px rgba(16, 185, 129, 0.8),
                            0 0 80px rgba(52, 211, 153, 0.7);
                    }
                }
                </style>
                """, unsafe_allow_html=True)
                
                st.download_button(
                    label="📥 Download Project Documentation (.docx)",
                    data=f,
                    file_name=os.path.basename(result["file_path"]),
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )

            # Optional: Add a helper text below
            st.markdown(
                '<div class="helper" style="text-align: center; margin-top: 1rem;">'
                '💾 Click the button above to save your professionally generated documentation'
                '</div>',
                unsafe_allow_html=True
            )
    else:
        st.error("⚠️ Please enter a project topic or context to continue.")

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    '<div style="text-align: center; color: #c4b5fd; font-size: 1rem; font-weight: 500; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);">'
    '✨ Created by AI • Made with ❤️ using Streamlit ✨'
    '</div>',
    unsafe_allow_html=True
)