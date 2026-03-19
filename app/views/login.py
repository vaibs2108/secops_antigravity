import streamlit as st
import os

def check_password():
    """Returns `True` if the user had the correct password."""
    
    # Secure defaults from .env
    admin_user = os.getenv("ADMIN_USERNAME", "admin")
    admin_pass = os.getenv("ADMIN_PASSWORD", "admin")

    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    # ---- LOGIN UI ----
    st.markdown("""
        <style>
        /* Hide the sidebar and top header to make it a true landing page */
        [data-testid="collapsedControl"] { display: none; }
        [data-testid="stSidebar"] { display: none; }
        [data-testid="stHeader"] { display: none; }
        
        /* Inject the Tech/AI Security Background into the main app container */
        .stApp {
            background: linear-gradient(rgba(15, 23, 42, 0.75), rgba(15, 23, 42, 0.95)), 
                        url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
        
        /* Push the content down just right to center it visually */
        [data-testid="stAppViewBlockContainer"] {
            padding-top: 10vh !important;
            max-width: 100% !important;
        }

        /* Style the st.form to be the actual glassmorphic login card */
        [data-testid="stForm"] {
            background-color: rgba(255, 255, 255, 0.97) !important;
            backdrop-filter: blur(20px) !important;
            padding: 45px 40px !important;
            border-radius: 16px !important;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255,255,255,0.1) inset !important;
            border: none !important;
            width: 440px !important;
            max-width: 90vw !important;
            margin: 0 auto !important; /* Center the form horizontally */
        }
        
        /* Typography overrides inside the form */
        .login-icon {
            font-size: 64px;
            margin-bottom: 5px;
            text-align: center;
            text-shadow: 0 4px 12px rgba(30,58,138,0.2);
        }
        .login-title {
            color: #1E3A8A;
            font-weight: 800;
            font-size: 26px;
            margin-bottom: 8px;
            font-family: 'Outfit', sans-serif;
            letter-spacing: -0.5px;
            text-align: center;
        }
        .login-subtitle {
            color: #64748B;
            font-size: 14px;
            margin-bottom: 30px;
            font-family: 'Outfit', sans-serif;
            text-align: center;
        }
        
        /* Input styling */
        [data-testid="stTextInput"] label {
            color: #1E293B !important;
            font-weight: 600;
            font-size: 14px;
        }
        
        .stButton>button {
            border-radius: 8px;
            font-weight: 600;
            letter-spacing: 0.5px;
            padding: 0.6rem 1.2rem;
            margin-top: 15px;
            background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
            color: #FFFFFF !important;
            border: none;
            width: 100%;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(30, 58, 138, 0.25);
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(30, 58, 138, 0.4);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # We use Streamlit columns to constrain the width safely on any screen size.
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        with st.form("login_form", clear_on_submit=False):
            # Injecting the title directly INSIDE the form box so it's a unified component
            st.markdown("""
                <div>
                    <div class="login-icon">🛡️</div>
                    <div class="login-title">Autonomous Security Operations</div>
                    <div class="login-subtitle">Executive Command Center Authentication</div>
                </div>
            """, unsafe_allow_html=True)
            
            username = st.text_input("Username", placeholder="admin")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            
            submit = st.form_submit_button("Secure Login", width='stretch')
            
            if submit:
                if username == admin_user and password == admin_pass:
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("🔒 Access Denied: Invalid credentials.")
                    
    return False

def render_persona():
    import os
    username = os.getenv("ADMIN_USERNAME", "admin").capitalize()
    initials = username[:2].upper()
    
    st.markdown(f"""
        <div style="position: fixed; top: 12px; right: 80px; z-index: 999999; display: flex; align-items: center; gap: 10px; background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(8px); padding: 6px 16px; border-radius: 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); border: 1px solid rgba(226, 232, 240, 0.8);">
            <div style="display: flex; flex-direction: column; align-items: flex-end;">
                <span style="font-family: 'Outfit', sans-serif; font-size: 13px; font-weight: 700; color: #1E293B; line-height: 1.2;">{username}</span>
                <span style="font-family: 'Outfit', sans-serif; font-size: 10px; font-weight: 500; color: #64748B; line-height: 1.2;">SecOps Administrator</span>
            </div>
            <div style="width: 34px; height: 34px; border-radius: 50%; background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; font-family: 'Outfit', sans-serif; font-size: 14px; box-shadow: inset 0 2px 4px rgba(255,255,255,0.3);">
                {initials}
            </div>
        </div>
    """, unsafe_allow_html=True)

