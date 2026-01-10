import streamlit as st
import time
from symbol_mapper import SymbolMapper
from pda_validator import PDAValidator

# page config
st.set_page_config(
    page_title="JobSafe Validator",
    page_icon="⚖️",
    layout="centered"
)

# styling
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

# header
st.title("⚖️ JobSafe")
st.caption("A Structural Integrity Verifier for Employment Contracts using Pushdown Automata")
st.markdown("---")

# init backend
try:
    mapper = SymbolMapper()
    pda = PDAValidator()
except Exception as e:
    st.error(f"System Error: Could not load backend modules. {e}")
    st.stop()

# sidebar
with st.sidebar:
    st.header("ℹ️ How it Works")
    st.markdown("""
    This system uses a **Pushdown Automata (PDA)** to validate contract structure.
    
    **Valid Sequence:**
    1. Header (H)
    2. Role (R)
    3. Duration (D)
    4. Scope/Duties (S)
    5. Compensation (C)
    6. Benefits (B)
    7. Confidentiality (F)
    8. Termination (T)
    9. Signatures (X)
    """)
    st.info("Dependencies Enforced:\n\n• Role ↔ Scope\n• Pay ↔ Benefits")

# main UI
uploaded_file = st.file_uploader("📂 Drag and drop your Contract (.txt)", type="txt")

if uploaded_file is not None:
   
    raw_text = uploaded_file.read().decode("utf-8")
    
    with st.expander("📄 View Original Contract Text", expanded=False):
        st.text(raw_text)

  
    st.subheader("1️⃣ Structural Analysis")
    
    lines = raw_text.strip().split('\n')
    token_stream = []
    
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    with st.container(border=True):
        st.markdown("**Token Generation Log:**")
        log_container = st.container()
        log_container.markdown("---")
        
        for i, line in enumerate(lines):
            
            progress = (i + 1) / len(lines)
            progress_bar.progress(progress)
            
            symbol = mapper.get_symbol(line)
            if symbol:
                token_stream.append(symbol)
               
                color = "blue"
                if symbol in ['R', 'C']: color = "orange" 
                if symbol in ['S', 'B']: color = "green"  
                
                log_container.markdown(f":{color}[Found **{symbol}**] | *{line.strip()[:50]}...*")
                time.sleep(0.05) 
    
    status_text.success("Analysis Complete!")
    st.info(f"**Generated Token Stream:** `{token_stream}`")

   
    st.divider()
    st.subheader("2️⃣ Validation Results")
    
    with st.spinner("Running Pushdown Automata Logic..."):
        time.sleep(1) 
        is_valid, log = pda.validate(token_stream)

    if is_valid:
        st.success("## ✅ CONTRACT ACCEPTED")
        st.markdown("The contract follows a valid structural sequence and all dependencies are resolved.")
        st.balloons()
    else:
        st.error("## ❌ CONTRACT REJECTED")
        st.markdown("The contract structure is invalid.")
        
       
        error_msg = "Unknown Error"
        for entry in log:
            if "REJECT" in entry:
                error_msg = entry
        
        st.warning(f"**Reason for Rejection:**\n\n`{error_msg}`")
        
        with st.expander("🔍 View Full Debug Log"):
            for entry in log:
                st.code(entry, language="text")
