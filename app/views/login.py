import streamlit as st
import os

def check_password():
    """Returns `True` if the user had the correct password."""
    
    # Secure defaults from .env
    admin_user = os.getenv("ADMIN_USERNAME", "admin")
    admin_pass = os.getenv("ADMIN_PASSWORD", "admin")

    import base64
    def get_base64_bin_file(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()

    bin_str = get_base64_bin_file(os.path.join(os.path.dirname(__file__), '..', 'assets', 'login_bg.png'))
    
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    # ── LOGIN UI — Light Frosted Theme ──
    st.markdown(f"""
        <style>
        /* Hide sidebar and header for clean landing page */
        [data-testid="collapsedControl"] {{ display: none; }}
        [data-testid="stSidebar"] {{ display: none; }}
        [data-testid="stHeader"] {{ display: none; }}
        
        /* Light frosted background — NO dark overlay */
        [data-testid="stAppViewContainer"] {{
            background: linear-gradient(135deg, rgba(248, 250, 252, 0.92), rgba(239, 246, 255, 0.88)), 
                        url("data:image/png;base64,{bin_str}") !important;
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
            overflow: hidden !important;
        }}
        
        [data-testid="stHeader"] {{ background: transparent !important; }}
        
        /* Center content */
        [data-testid="stAppViewBlockContainer"] {{
            padding-top: 0 !important;
            height: 100vh !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            max-width: 100% !important;
        }}

        /* Glassmorphic login card — bright white */
        [data-testid="stForm"] {{
            background-color: rgba(255, 255, 255, 0.97) !important;
            backdrop-filter: blur(20px) !important;
            padding: 40px 35px !important;
            border-radius: 16px !important;
            box-shadow: 0 20px 60px -15px rgba(30, 58, 138, 0.12), 0 0 0 1px rgba(226, 232, 240, 0.6) inset !important;
            border: 1px solid #E2E8F0 !important;
            width: 420px !important;
            max-width: 90vw !important;
            margin: auto !important;
        }}
        
        /* Typography */
        .login-icon {{
            font-size: 48px;
            margin-bottom: 4px;
            text-align: center;
        }}
        .login-title {{
            color: #1E3A8A;
            font-weight: 800;
            font-size: 22px;
            margin-bottom: 4px;
            font-family: 'Outfit', sans-serif;
            letter-spacing: -0.5px;
            text-align: center;
        }}
        .login-subtitle {{
            color: #64748B;
            font-size: 13px;
            margin-bottom: 28px;
            font-family: 'Outfit', sans-serif;
            text-align: center;
        }}
        
        /* Input styling */
        [data-testid="stTextInput"] label {{
            color: #1E293B !important;
            font-weight: 600;
            font-size: 13px;
        }}
        
        .stButton>button {{
            border-radius: 8px;
            font-weight: 600;
            letter-spacing: 0.3px;
            padding: 0.55rem 1rem;
            margin-top: 12px;
            background: #1E40AF;
            color: #FFFFFF !important;
            border: none;
            width: 100%;
            transition: all 0.2s ease;
            box-shadow: 0 2px 8px rgba(30, 64, 175, 0.2);
        }}
        .stButton>button:hover {{
            background: #1E3A8A;
            box-shadow: 0 4px 16px rgba(30, 58, 138, 0.3);
        }}
        </style>
    """, unsafe_allow_html=True)
    
    # Center the login box
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        with st.form("login_form", clear_on_submit=False):
            st.markdown("""
                <div>
                    <div class="login-icon">🛡️</div>
                    <div class="login-title">Autonomous SecOps</div>
                    <div class="login-subtitle">Executive Command Center Authentication</div>
                </div>
            """, unsafe_allow_html=True)
            
            username = st.text_input("Username", placeholder="admin")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            
            submit = st.form_submit_button("Secure Login", use_container_width=True)
            
            if submit:
                if username == admin_user and password == admin_pass:
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("🔒 Access Denied")
                    
    return False

def render_persona():
    """Persona display is now handled by the horizontal top navbar in main.py."""
    pass

