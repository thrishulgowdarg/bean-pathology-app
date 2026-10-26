import streamlit as st
import requests
from PIL import Image

# Your live tunnel URL from Colab
API_URL = "https://young-ducks-admire.loca.lt/predict"

st.set_page_config(page_title="Rootsgoods Plant Pathology", page_icon="🌱", layout="wide")

# Inject Custom Enterprise CSS
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .main-header {
        text-align: center; color: #166534; font-family: sans-serif;
        font-weight: 800; font-size: 2.5rem; margin-bottom: 0; padding-bottom: 0;
    }
    .sub-header {
        text-align: center; color: #475569; font-size: 1.1rem; margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #166534; color: white; border-radius: 8px;
        height: 3em; font-size: 1.1em; font-weight: bold; border: none;
    }
    .stButton>button:hover {
        background-color: #14532d; border: none; color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🌱 Rootsgoods Diagnostic AI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Powered by MiniCPM-V 2.6 & Custom Deep CPU Matrix (95.25% Accuracy)</p>', unsafe_allow_html=True)
st.divider()

col1, gap, col2 = st.columns([1, 0.1, 1])

with col1:
    st.markdown("<h3 style='color: #1e293b;'>📸 1. Leaf Specimen Analysis</h3>", unsafe_allow_html=True)
    st.info("Upload a clear, well-lit image of the affected maize crop.")
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        with st.container(border=True):
            st.image(image, caption="Target Specimen", use_container_width=True)

with col2:
    st.markdown("<h3 style='color: #1e293b;'>🔬 2. Diagnostic Report</h3>", unsafe_allow_html=True)
    
    if uploaded_file is None:
        st.warning("👈 Awaiting image upload to begin analysis...")
    else:
        if st.button("🚀 Run Deep Matrix Analysis", use_container_width=True):
            with st.spinner("Extracting 13,056-dim features & running deep CPU probe..."):
                uploaded_file.seek(0)
                files = {"file": (uploaded_file.name, uploaded_file, "image/jpeg")}
                
                try:
                    response = requests.post(API_URL, files=files)
                    if response.status_code == 200:
                        data = response.json()
                        predictions = data.get("predictions", {})
                        latency = data.get("latency_ms", 0)
                        
                        st.success(f"⚡ Inference completed in **{latency} ms** on CPU edge-backend")
                        st.markdown("<h4 style='color: #1e293b; margin-top: 15px;'>Top Pathologies Detected:</h4>", unsafe_allow_html=True)
                        
                        # Custom HTML Progress Cards (Fixes invisible text issue)
                        for i, (disease, prob) in enumerate(predictions.items()):
                            clean_name = disease.replace("_", " ").title()
                            percentage = prob * 100
                            
                            html_bar = f"""
                            <div style="background-color: white; padding: 14px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                                    <span style="font-weight: 700; color: #334155; font-size: 16px;">{i+1}. {clean_name}</span>
                                    <span style="font-weight: 800; color: #166534; font-size: 16px;">{percentage:.1f}%</span>
                                </div>
                                <div style="width: 100%; background-color: #f1f5f9; border-radius: 4px; height: 10px;">
                                    <div style="width: {percentage}%; background-color: #22c55e; height: 10px; border-radius: 4px;"></div>
                                </div>
                            </div>
                            """
                            st.markdown(html_bar, unsafe_allow_html=True)
                            
                        # Actionable Dropdown
                        top_disease = list(predictions.keys())[0].replace("_", " ").title()
                        with st.expander(f"📝 Recommended Protocol for {top_disease}"):
                            st.write("**Immediate Actions:**")
                            st.write("- Isolate the affected crop sector if possible.")
                            st.write("- Log the geographic coordinates of this specimen in the Rootsgoods database.")
                            st.write("- Consult the agronomy team for targeted chemical or biological treatments.")
                    else:
                        st.error(f"Backend Error: {response.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error("⚠️ Could not connect to the backend. Ensure LocalTunnel is running and the IP password was entered.")
