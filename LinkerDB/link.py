import streamlit as st
import dropbox
import pandas as pd
import os
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import time

import streamlit as st
import streamlit.components.v1 as components



st.set_page_config(   
                page_title="DB-LinX App",
                page_icon="📥",
                layout="wide",
                initial_sidebar_state="expanded")


# --- 🚫 Block Chrome browsers ---
components.html("""
<script>
(function() {
    let ua = navigator.userAgent;
    // Detect Chrome but exclude Edge (Edg) and Opera (OPR)
    if (ua.includes("Chrome") && !ua.includes("Edg") && !ua.includes("OPR")) {
        document.body.style.backgroundColor = "white";
        document.body.innerHTML = `
            <div style="
                display:flex;
                justify-content:center;
                align-items:center;
                height:100vh;
                font-family:Arial, sans-serif;
                color:#d00;
                font-size:24px;
                font-weight:bold;
            ">
                🚫 Please choose another browser
            </div>
        `;
    }
})();
</script>
""", height=0)



# 📘 Sidebar Instructions
with st.sidebar:
    st.header("📖 How to Use")
    st.markdown("""
    1. Paste your **Dropbox API Key** 🔐  
    2. Enter the **Main Folder Path** 📂  
    3. Select file types to extract (optional) 🧠  
    4. Click **Generate Links** 🚀  
    5. Download your CSV 📥  
    """)
    st.markdown("---")
    st.info("Need help? Visit [Dropbox API Docs](https://www.dropbox.com/developers/documentation)")

# 🏷️ Title and Branding
st.markdown("""
    <h1 style='text-align: center; color: #FF4B4B;'>📦 Dropbox Link Xtractor</h1>
    <h4 style='text-align: center;'>Powered by <span style='color: red;'>Mr.X</span></h4>
    <hr style='border: 1px solid #ddd;'>
""", unsafe_allow_html=True)

#-----------------------------------------------------------------------

ACCESS_TOKEN = st.text_area("🔐 Feed your :red[**Dropbox**] API Key Here !:", placeholder="Paste your Dropbox API token here...")
FOLDER_PATH = st.text_input("📂 Enter your :red[**Dropbox**] Folder path Here !:", placeholder="/MainFolder")

# 🧃 File Type Filter


btn = st.button("🚀 Generate Dropbox Links")

try:
    from secure_logic import traverse_folder
    SECURE_LOGIC_AVAILABLE = True
except ImportError:
    SECURE_LOGIC_AVAILABLE = False

if btn:
    if not ACCESS_TOKEN or not FOLDER_PATH:
        st.warning("⚠️ Please provide both the API key and folder path.")
    elif not SECURE_LOGIC_AVAILABLE:
        st.error("🚫 Secure logic module not found. This app is running in public mode.")
        st.info("🔐 To enable Dropbox link extraction, add your private module locally.")
    else:
        with st.spinner("🔄 Extracting links..."):
            progress = st.progress(0)
            try:
                dbx = dropbox.Dropbox(ACCESS_TOKEN)
                main_folder_name = FOLDER_PATH.strip('/').split('/')[-1]

                for i in range(1, 6):
                    time.sleep(0.3)
                    progress.progress(i * 20)

                all_links = traverse_folder(dbx, FOLDER_PATH, main_folder_name)

                if all_links:
                    df = pd.DataFrame(all_links)
                    csv_content = df.to_csv(index=False).encode('utf-8')

                    st.success(f"✅ {len(df)} links generated successfully!")
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv_content,
                        file_name="dropbox_links.csv",
                        mime="text/csv",
                        type="primary"
                    )
                else:
                    st.warning("⚠️ No matching files found. Please check your folder path and filters.")
                    st.info("💡 Arey, yaar Use Common Sense, Simple sa kaam 😁😅!")

            except dropbox.exceptions.AuthError:
                st.error("❌ Invalid access token.")
                st.info("💡 Arey, yaar Use Common Sense, Simple sa kaam 😁😅!")
            except Exception as e:
                st.error(f"❌ Unexpected error: {e}")
                st.info("💡 Arey, yaar Use Common Sense, Simple sa kaam 😁😅!")




