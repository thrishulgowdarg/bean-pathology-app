import streamlit as st
import requests
from PIL import Image

# Your live tunnel URL from Colab
API_URL = "https://young-ducks-admire.loca.lt/predict"

# 1. Changed layout from "centered" to "wide"
st.set_page_config(page_title="Rootsgoods Plant Pathology", page_icon="🌱", layout="wide")

st.title("🌱 Rootsgoods 12-Class Maize Diagnostic AI")
st.markdown("**Powered by MiniCPM-V 2.6 & Custom Deep CPU Probe (95.25% Accuracy)**")

uploaded_file = st.file_uploader("Upload a maize leaf image for diagnosis...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 2. Create two side-by-side columns
    col1, col2 = st.columns([1, 1]) 
    
    with col1:
        image = Image.open(uploaded_file)
        # use_container_width prevents the image from blowing up too large
        st.image(image, caption="Uploaded Leaf", use_container_width=True)
        
    with col2:
        # Make the button span the width of the right column
        if st.button("Run Diagnostic Scan", type="primary", use_container_width=True):
            with st.spinner("Extracting features and running deep matrix engine..."):
                uploaded_file.seek(0)
                files = {"file": (uploaded_file.name, uploaded_file, "image/jpeg")}
                
                try:
                    response = requests.post(API_URL, files=files)
                    
                    if response.status_code == 200:
                        data = response.json()
                        predictions = data.get("predictions", {})
                        latency = data.get("latency_ms", 0)
                        
                        st.success(f"⚡ Inference completed in {latency} ms on CPU backend")
                        
                        st.subheader("Top 3 Predictions")
                        for disease, prob in predictions.items():
                            st.metric(label=disease.replace("_", " ").title(), value=f"{prob * 100:.1f}%")
                            st.progress(float(prob))
                    else:
                        st.error(f"Backend Error: {response.status_code}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("⚠️ Could not connect to the backend. If you just clicked the Tunnel URL, make sure you entered the Tunnel Password (IP address) in your browser first to bypass the warning screen.")
