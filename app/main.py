import streamlit as st
from dotenv import load_dotenv
import time

from app.data_generator.generator import SecurityDataGenerator
from app.kpi_engine.calculator import KPICalculator

# Import views
from app.views.dashboard import render_dashboard
from app.views.major_incident import render_major_incident_management
from app.views.provisioning import render_provisioning
from app.views.automation import render_automation
from app.views.asset_visibility import render_asset_visibility
from app.views.compliance import render_compliance
from app.views.detection_response import render_detection_response
from app.views.secops import render_secops

load_dotenv()

st.set_page_config(
    page_title="GenAI SecOps Demo",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

def init_session_state():
    if 'dataset' not in st.session_state:
        with st.spinner("Generating enterprise-scale synthetic security data..."):
            generator = SecurityDataGenerator()
            dataset = generator.generate_all()
            st.session_state.dataset = dataset
            
            # Initialize KPI Engine
            kpi_engine = KPICalculator(dataset)
            st.session_state.kpis = kpi_engine.get_all_kpis()
            
            st.success("✅ Synthetic environment initialized successfully.")
            time.sleep(1)
            st.rerun()

def main():
    st.markdown("""
        <style>
        /* Modern Glassmorphism & Cyber Premium Theme */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
        
        .stApp {
            background-color: #050b14;
            background-image: radial-gradient(circle at 15% 50%, rgba(0, 255, 204, 0.05), transparent 40%),
                              radial-gradient(circle at 85% 30%, rgba(0, 153, 255, 0.08), transparent 40%);
            color: #e2e8f0;
            font-family: 'Outfit', -apple-system, sans-serif;
        }
        
        h1, h2, h3 {
            color: #ffffff;
            font-weight: 600;
            letter-spacing: -0.02em;
        }
        
        /* Sidebar styling - Glass effect */
        [data-testid="stSidebar"] {
            background-color: rgba(9, 14, 23, 0.85) !important;
            backdrop-filter: blur(12px);
            border-right: 1px solid rgba(0, 255, 204, 0.15);
        }
        [data-testid="stSidebar"] .stRadio label {
            padding: 10px 14px;
            border-radius: 8px;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            color: #94a3b8;
        }
        [data-testid="stSidebar"] .stRadio label:hover {
            background-color: rgba(0, 255, 204, 0.1);
            color: #00ffcc;
            transform: translateX(4px);
        }
        /* Hide native streamlit radio circles */
        [data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {
            display: none !important;
        }
        
        /* Metric Cards - Neon & Glass */
        [data-testid="metric-container"] {
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 15px 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }
        [data-testid="metric-container"]:hover {
            border-color: rgba(0, 255, 204, 0.5);
            box-shadow: 0 0 25px rgba(0, 255, 204, 0.15);
            transform: translateY(-3px);
            background: rgba(15, 23, 42, 0.8);
        }
        [data-testid="stMetricValue"] {
            color: #00ffcc !important;
            font-weight: 700;
        }
        [data-testid="stMetricDelta"] {
            font-weight: 600;
        }
        
        /* Custom Buttons - Cyber Gradient */
        .stButton > button {
            background: linear-gradient(135deg, #0052cc 0%, #00ffcc 100%);
            color: #050b14;
            border: none;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0, 255, 204, 0.3);
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            font-weight: 700;
            letter-spacing: 0.5px;
            padding: 0.5rem 1rem;
        }
        .stButton > button:hover {
            transform: scale(1.03) translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 255, 204, 0.5);
            color: #050b14;
        }
        
        /* Expander Headers */
        .streamlit-expanderHeader {
            background-color: rgba(15, 23, 42, 0.7);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 8px;
            font-weight: 600;
            color: #e2e8f0;
        }
        .streamlit-expanderHeader:hover {
            color: #00ffcc;
            border-color: rgba(0, 255, 204, 0.4);
            background-color: rgba(15, 23, 42, 0.9);
        }
        
        /* Info Boxes */
        .stAlert {
            background: rgba(0, 153, 255, 0.1) !important;
            backdrop-filter: blur(5px);
            border: 1px solid rgba(0, 153, 255, 0.3) !important;
            border-radius: 8px !important;
            color: #e2e8f0 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    init_session_state()
    
    st.sidebar.title("GenAI Orchestrator Domains")
    
    domain_selection = st.sidebar.radio(
        "Navigation",
        [
            "📊 Executive Dashboard",
            "🚨 Major Incident Management",
            "⚡ Provisioning",
            "🤖 Automation",
            "🔍 Asset Visibility",
            "⚖️ Compliance",
            "🛡️ Detection & Response",
            "⚙️ Security Operations",
            "🕵️ Agents View",
            "📂 Synthetic Data Explorer",
            "💬 Platform Copilot (Chat)"
        ]
    )
    
    # Strip emojis for routing logic
    domain = domain_selection.split(" ", 1)[1] if " " in domain_selection else domain_selection
    
    st.sidebar.markdown("---")
    st.sidebar.info("This application synthesizes context and simulates Agent interventions safely.")
    if st.sidebar.button("Regenerate Context Data"):
        del st.session_state.dataset
        st.rerun()
        
    kpis = st.session_state.kpis
    dataset = st.session_state.dataset
    
    # Virtual Routing
    if domain == "Executive Dashboard":
        render_dashboard(kpis, dataset)
    elif domain == "Major Incident Management":
        render_major_incident_management(kpis, dataset)
    elif domain == "Provisioning":
        render_provisioning(kpis, dataset)
    elif domain == "Automation":
        render_automation(kpis, dataset)
    elif domain == "Asset Visibility":
        render_asset_visibility(kpis, dataset)
    elif domain == "Compliance":
        render_compliance(kpis, dataset)
    elif domain == "Detection & Response":
        render_detection_response(kpis, dataset)
    elif domain == "Security Operations":
        render_secops(kpis, dataset)
    elif domain == "Agents View":
        from app.views.agent_console import render_agent_console
        render_agent_console(kpis, dataset)
    elif domain == "Synthetic Data Explorer":
        from app.views.data_explorer import render_data_explorer
        render_data_explorer(dataset)
    elif "Platform Copilot" in domain:
        from app.views.chatbot import render_chatbot
        render_chatbot(kpis, dataset)

if __name__ == "__main__":
    main()
