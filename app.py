import streamlit as st
import time
from symbol_mapper import SymbolMapper
from pda_validator import PDAValidator
from pypdf import PdfReader  # <--- NEW IMPORT

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="JobSafe Validator",
    page_icon="⚖️",
    layout="centered"
)

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stStatusWidget {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("⚖️ JobSafe")
st.caption("A Structural Integrity Verifier for Employment Contracts using Pushdown Automata")
st.markdown("---")

# --- INITIALIZE BACKEND ---
try:
    mapper = SymbolMapper()
    pda = PDAValidator()
except Exception as e:
    st.error(f"System Error: Could not load backend modules. {e}")
    st.stop()

# --- SIDEBAR INFO ---
# In your app.py sidebar code:
with st.sidebar:
    st.header("ℹ️ How it Works")
    st.markdown("""
    This system uses a **Pushdown Automata (PDA)** to validate contract structure.
    
    **Strict Sequence Enforced:**
    1. Header (H)
    2. Role (R)
    3. Duration (D)
    4. Scope/Duties (S)  <-- Make sure this is #4
    5. Compensation (C)  <-- Make sure this is #5
    6. Benefits (B)
    7. Confidentiality (F)
    8. Termination (T)
    9. Signatures (X)
    """)

# --- HELPER FUNCTION FOR PDF ---
def extract_text_from_pdf(uploaded_file):
    try:
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return None

# --- MAIN INTERFACE ---
# UPDATE: Changed type to include "pdf"
uploaded_file = st.file_uploader("📂 Drag and drop your Contract (TXT or PDF)", type=["txt", "pdf"])

if uploaded_file is not None:
    # 1. READ FILE (Logic updated for PDF)
    raw_text = ""
    
    if uploaded_file.type == "application/pdf":
        with st.spinner("Extracting text from PDF..."):
            raw_text = extract_text_from_pdf(uploaded_file)
            if not raw_text:
                st.error("Error: Could not read this PDF. It might be an image scan.")
                st.stop()
    else:
        # It's a TXT file
        raw_text = uploaded_file.read().decode("utf-8")
    
    with st.expander("📄 View Extracted Text", expanded=False):
        st.text(raw_text)

    # 2. ANALYZE (Symbol Mapper)
    st.subheader("1️⃣ Structural Analysis")
    
    lines = raw_text.strip().split('\n')
    token_stream = []
    
    # Progress Bar Animation
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    with st.container(border=True):
        st.markdown("**Token Generation Log:**")
        log_container = st.container()
        log_container.markdown("---")
        
        for i, line in enumerate(lines):
            # Update progress
            progress = (i + 1) / len(lines)
            progress_bar.progress(progress)
            
            symbol = mapper.get_symbol(line)
            if symbol:
                token_stream.append(symbol)
                # specific coloring for symbols
                color = "blue"
                if symbol in ['R', 'C']: color = "orange" # Dependency openers
                if symbol in ['S', 'B']: color = "green"  # Dependency closers
                
                log_container.markdown(f":{color}[Found **{symbol}**] | *{line.strip()[:50]}...*")
                time.sleep(0.05) # Artificial delay for effect
    
    status_text.success("Analysis Complete!")
    st.info(f"**Generated Token Stream:** `{token_stream}`")

    # 3. VALIDATE (PDA)
    st.divider()
    st.subheader("2️⃣ Validation Results")
    
    with st.spinner("Running Pushdown Automata Logic..."):
        time.sleep(1) # Artificial delay for effect
        is_valid, log = pda.validate(token_stream)

    if is_valid:
        st.success("## ✅ CONTRACT ACCEPTED")
        st.markdown("The contract follows a valid structural sequence and all dependencies are resolved.")
        st.balloons()
    else:
        st.error("## ❌ CONTRACT REJECTED")
        st.markdown("The contract structure is invalid.")
        
        # Isolate the specific error from the log
        error_msg = "Unknown Error"
        for entry in log:
            if "REJECT" in entry:
                error_msg = entry
        
        st.warning(f"**Reason for Rejection:**\n\n`{error_msg}`")
        
        with st.expander("🔍 View Full Debug Log"):
            for entry in log:
                st.code(entry, language="text")