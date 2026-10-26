import streamlit as st
import requests
from PIL import Image

# Your live tunnel URL from Colab
API_URL = "https://young-ducks-admire.loca.lt/predict"

# 1. Page Config must be first
st.set_page_config(page_title="Rootsgoods Plant Pathology", page_icon="🌱", layout="wide", initial_sidebar_state="collapsed")

# 2. Inject Custom CSS for a Premium UI
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #f8fafc;
    }
    /* Custom Header */
    .hero-text {
        text-align: center;
        color: #166534;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 2.8rem;
        margin-bottom: 0rem;
        padding-bottom: 0rem;
    }
    .hero-sub {
        text-align: center;
        color: #475569;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    /* Style the upload box */
    .stFileUploader>div>div {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    /* Style the button */
    .stButton>button {
        border-radius: 8px;
        height: 3.5em;
        font-size: 1.1em;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Hero Header
st.markdown('<p class="hero-text">🌱 Rootsgoods Diagnostic AI</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">Powered by MiniCPM-V 2.6 & Custom Deep CPU Matrix (95.25% Accuracy)</p>', unsafe_allow_html=True)
st.divider()

# 4. Split Layout
col1, col_gap, col2 = st.columns([1.2, 0.1, 1])

with col1:
    st.markdown("### 📸 1. Leaf Specimen Analysis")
    st.info("Upload a clear, well-lit image of the affected maize crop.")
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        # Use container to give the image a nice border
        with st.container(border=True):
            st.image(image, caption="Target Specimen", use_container_width=True)

with col2:
    st.markdown("### 🔬 2. Diagnostic Report")
    
    if uploaded_file is None:
        st.warning("👈 Awaiting image upload to begin analysis...")
    else:
        if st.button("🚀 Run Deep Matrix Analysis", type="primary", use_container_width=True):
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
                        
                        # Premium Results Container
                        with st.container(border=True):
                            st.markdown("#### Top Pathologies Detected")
                            
                            for i, (disease, prob) in enumerate(predictions.items()):
                                clean_name = disease.replace("_", " ").title()
                                percentage = prob * 100
                                
                                # Use columns for a clean metric layout
                                m_col1, m_col2 = st.columns([3, 1])
                                with m_col1:
                                    st.markdown(f"**{i+1}. {clean_name}**")
                                with m_col2:
                                    st.markdown(f"`{percentage:.2f}%`")
                                    
                                st.progress(float(prob))
                                
                        # Actionable Next Steps
                        top_disease = list(predictions.keys())[0].replace("_", " ").title()
                        with st.expander(f"📝 Recommended Protocol for {top_disease}"):
                            st.write(f"**Immediate Actions:**")
                            st.write("- Isolate the affected crop sector if possible.")
                            st.write("- Log the geographic coordinates of this specimen in the Rootsgoods database.")
                            st.write("- Consult the agronomy team for targeted chemical or biological treatments specific to this diagnosis.")
                            
                    else:
                        st.error(f"Backend Error: {response.status_code}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("⚠️ Could not connect to the backend. Ensure LocalTunnel is running in Colab and you've entered the IP password in the browser.")
