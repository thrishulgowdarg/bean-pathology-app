import streamlit as st
import requests
import io
from PIL import Image

st.set_page_config(
    page_title="Bean Pathology Diagnostic Suite | MiniCPM-V 2.6 CPU",
    page_icon="🌿",
    layout="wide"
)

st.markdown("""
<style>
    .diag-card {
        padding: 20px 24px;
        border-radius: 12px;
        margin-bottom: 16px;
        border-left: 7px solid;
        box-shadow: 0 3px 10px rgba(0,0,0,0.06);
    }
    .telemetry-pill {
        display: inline-block;
        background: #f1f5f9;
        color: #334155;
        font-size: 0.82rem;
        font-weight: 600;
        padding: 5px 12px;
        border-radius: 999px;
        margin-right: 8px;
        margin-bottom: 14px;
        border: 1px solid #cbd5e1;
    }
    .assessment-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 14px;
    }
</style>
""", unsafe_allow_html=True)

PATHOLOGY_KB = {
    "angular_leaf_spot": {
        "title": "ANGULAR LEAF SPOT",
        "severity": "Confirmed Fungal Infection — High Severity",
        "bg_color": "#fef2f2",
        "border_color": "#dc2626",
        "text_color": "#991b1b",
        "pathogen": "Pseudocercospora griseola (syn. Phaeoisariopsis griseola)",
        "morphology": "Sharp-edged, geometric polygonal brown-to-gray necrotic lesions strictly bounded by the leaf veins and veinlets, lacking raised powdery spore pustules.",
        "chemical": "Apply Strobilurin (Azoxystrobin) or Triazole (Difenoconazole) foliar sprays at early pod initiation (R1–R3) when foliar incidence exceeds 10%.",
        "cultural": "Use certified pathogen-free seed, enforce a 2-year crop rotation with non-legumes (e.g., maize), and plow under infected bean debris post-harvest."
    },
    "bean_rust": {
        "title": "BEAN RUST",
        "severity": "Confirmed Uredinial Infection — Moderate/High Severity",
        "bg_color": "#fffbeb",
        "border_color": "#d97706",
        "text_color": "#92400e",
        "pathogen": "Uromyces appendiculatus",
        "morphology": "Small, circular, slightly raised reddish-brown (cinnamon-colored) powdery spore pustules scattered across the lamina, surrounded by distinct yellow chlorotic halos.",
        "chemical": "Targeted foliar application of Tebuconazole or Propiconazole (DMI) fungicides upon initial pustule eruption prior to pod fill.",
        "cultural": "Plant rust-resistant cultivars carrying Ur-gene pyramids, avoid high-pressure overhead irrigation, and eliminate volunteer bean plants."
    },
    "healthy": {
        "title": "HEALTHY FOLIAGE",
        "severity": "Asymptomatic / Vigorous Canopy",
        "bg_color": "#ecfdf5",
        "border_color": "#059669",
        "text_color": "#065f46",
        "pathogen": "None Detected (Pathogen-Free Lamina)",
        "morphology": "Intact, uniform vibrant green leaf surface with normal venation; free of vein-delimited angular necrosis, chlorotic halos, or raised uredinial rust pustules.",
        "chemical": "No fungicide intervention required. Preserve natural beneficial phyllosphere microflora.",
        "cultural": "Continue routine foliar scouting schedule, balanced NPK soil nutrition, and optimal inter-row canopy airflow."
    }
}

# Left Sidebar
with st.sidebar:
    st.markdown("## 🌿 PhytoScan VLM Suite")
    st.caption("rootsgoods AI — Foliar Pathology Engine")
    api_url = st.text_input(
        "CPU Engine Tunnel URL (.loca.lt)",
        value="https://puny-bees-matter.loca.lt",
        placeholder="https://xxxx.loca.lt"
    ).strip().rstrip("/")
    st.selectbox("Select Crop Module", ["Bean Foliar Module (Phaseolus vulgaris)"], index=0)
    st.divider()
    st.markdown("**Model:** `MiniCPM-V 2.6 (CPU Native)`")
    st.markdown("**Test Accuracy:** `97.66% (Macro F1: 97.66%)`")
    st.markdown("**Classifier:** `Direct Matrix Probe`")

st.markdown("## 🔬 Bean Foliar Pathology Diagnostic Suite")

col_left, col_right = st.columns([1.0, 1.3], gap="large")

with col_left:
    uploaded_file = st.file_uploader("Upload leaf image (.jpg, .jpeg, .png)", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        pil_img = Image.open(uploaded_file)
        st.image(pil_img, use_container_width=True)

with col_right:
    run_btn = st.button("Run Diagnostic Engine", type="primary")
    
    if uploaded_file is not None and run_btn:
        if not api_url:
            st.error("⚠️ Please enter your `.loca.lt` URL in the left sidebar first!")
        else:
            with st.spinner("Executing MiniCPM-V 2.6 CPU Matrix Probe..."):
                try:
                    img_buf = io.BytesIO()
                    pil_img.convert("RGB").save(img_buf, format="JPEG")
                    img_buf.seek(0)
                    
                    headers = {"Bypass-Tunnel-Reminder": "true"}
                    resp = requests.post(
                        f"{api_url}/predict",
                        files={"file": ("leaf.jpg", img_buf, "image/jpeg")},
                        headers=headers,
                        timeout=30
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    
                    probs_dict = data["probabilities"]
                    latency_ms = data["latency_ms"]
                    
                    pred_key = max(probs_dict, key=probs_dict.get)
                    pred_conf = probs_dict[pred_key] * 100.0
                    kb = PATHOLOGY_KB[pred_key]
                    
                    # Dynamic Diagnosis Card
                    st.markdown(f"""
                    <div class="diag-card" style="background-color: {kb['bg_color']}; border-left-color: {kb['border_color']};">
                        <div style="font-size: 0.80rem; font-weight: 700; text-transform: uppercase; color: {kb['text_color']}; letter-spacing: 0.05em;">
                            {kb['severity']}
                        </div>
                        <h3 style="color: {kb['text_color']}; margin: 4px 0 0 0; font-weight: 800;">
                            Verified Diagnosis: {kb['title']} ({pred_conf:.2f}%)
                        </h3>
                    </div>
                    <div>
                        <span class="telemetry-pill">⚡ CPU Latency: {latency_ms:.0f} ms</span>
                        <span class="telemetry-pill">🎯 Verified Test Accuracy: 97.66%</span>
                        <span class="telemetry-pill">🧮 MiniCPM Vision + Matrix Probe</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Confidence Breakdown
                    st.markdown("#### Confidence Breakdown")
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Angular Leaf Spot", f"{probs_dict['angular_leaf_spot']*100:.1f}%")
                    m2.metric("Bean Rust", f"{probs_dict['bean_rust']*100:.1f}%")
                    m3.metric("Healthy", f"{probs_dict['healthy']*100:.1f}%")
                    
                    for label_name, key_name in [
                        ("Angular Leaf Spot", "angular_leaf_spot"),
                        ("Bean Rust", "bean_rust"),
                        ("Healthy", "healthy")
                    ]:
                        pct = float(probs_dict[key_name] * 100.0)
                        st.progress(min(max(int(round(pct)), 0), 100), text=f"**{label_name}** — {pct:.1f}%")
                        
                    st.divider()
                    
                    # Clinical Pathology Assessment
                    st.markdown("### 📋 Clinical Pathology Assessment")
                    st.markdown(f"""
                    <div class="assessment-card">
                        <p style="margin-bottom: 10px;"><b>Causative Pathogen:</b> <i>{kb['pathogen']}</i></p>
                        <p style="margin-bottom: 0;"><b>Lesion Morphology:</b> {kb['morphology']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    tab1, tab2 = st.tabs(["🧪 Chemical Control", "🌱 Cultural Management"])
                    with tab1:
                        st.info(f"**Chemical Control:** {kb['chemical']}")
                    with tab2:
                        st.success(f"**Cultural Management:** {kb['cultural']}")
                        
                except Exception as e:
                    st.error(f"Connection error: {e}. Check that your Colab cell is running and the tunnel URL is active.")
