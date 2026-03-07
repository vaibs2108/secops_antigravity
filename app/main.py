import streamlit as st
from dotenv import load_dotenv
import time
import os

from app.data_generator.generator import SecurityDataGenerator
from app.data_generator.rag_generator import RAGDataGenerator
from app.kpi_engine.calculator import KPICalculator
from app.agents.rag_engine import SECopsRAGEngine

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

@st.cache_data(show_spinner=True)
def get_cached_dataset():
    """Generates and caches the main security dataset for the portal."""
    generator = SecurityDataGenerator()
    return generator.generate_all()

@st.cache_data(show_spinner=True)
def get_cached_rag_data():
    """Generates and caches the synthetic KEDB and Ticket data for RAG."""
    kedb = RAGDataGenerator.generate_kedb_entries(50)
    tickets = RAGDataGenerator.generate_tickets(60)
    return kedb, tickets

@st.cache_resource(show_spinner="Initializing Global Vector Engine...")
def get_cached_rag_engine(kedb_df, tickets_df):
    """
    Initializes and caches the FAISS Vector Engine.
    This ensures we only build the vector store once per server instance,
    saving memory and minimizing OpenAI API embedding calls.
    """
    try:
        if not os.getenv("OPENAI_API_KEY"):
            return None
        engine = SECopsRAGEngine()
        engine.ingest_data(kedb_df, tickets_df)
        return engine
    except Exception as e:
        print(f"CRITICAL: RAG Engine failed to initialize: {e}")
        return None

def init_session_state():
    """Initializes the application state, utilizing cached resources where possible."""
    # 1. Main Dashboard Dataset
    if 'dataset' not in st.session_state:
        st.session_state.dataset = get_cached_dataset()
        kpi_engine = KPICalculator(st.session_state.dataset)
        st.session_state.kpis = kpi_engine.get_all_kpis()
    
    # 2. RAG Context Data
    if 'rag_kedb' not in st.session_state:
        kedb, tickets = get_cached_rag_data()
        st.session_state.rag_kedb = kedb
        st.session_state.rag_tickets = tickets
    
    # 3. Global Vector Engine
    if 'rag_engine' not in st.session_state:
        # We use a resource cache so all users share the same FAISS index in memory
        st.session_state.rag_engine = get_cached_rag_engine(
            st.session_state.rag_kedb, 
            st.session_state.rag_tickets
        )

def main():
    st.markdown("""
        <style>
        /* Modern Glassmorphism & Clean Light Theme */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
        
        .stApp {
            background-color: #F8FAFC;
            background-image: radial-gradient(circle at 15% 50%, rgba(30, 58, 138, 0.03), transparent 40%),
                              radial-gradient(circle at 85% 30%, rgba(59, 130, 246, 0.05), transparent 40%);
            color: #0F172A;
            font-family: 'Outfit', -apple-system, sans-serif;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #0F172A !important;
            font-weight: 700;
            letter-spacing: -0.03em;
        }
        
        /* Sidebar styling - Executive Solid White */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            box-shadow: 2px 0 25px rgba(15, 23, 42, 0.05) !important;
            border-right: 1px solid rgba(226, 232, 240, 0.6);
        }
        [data-testid="stSidebar"] .stRadio label {
            padding: 10px 14px;
            border-radius: 8px;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            color: #475569;
        }
        [data-testid="stSidebar"] .stRadio label:hover {
            background-color: rgba(37, 99, 235, 0.08);
            color: #1D4ED8;
            transform: translateX(4px);
        }
        /* Hide native streamlit radio circles */
        [data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {
            display: none !important;
        }
        
        /* Metric Cards - Executive Clean Style */
        [data-testid="metric-container"] {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 20px 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        [data-testid="metric-container"]:hover {
            border-color: #93C5FD;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            transform: translateY(-2px);
        }
        [data-testid="stMetricValue"] {
            color: #1E3A8A !important;
            font-weight: 800;
            font-size: 2.2rem !important;
        }
        [data-testid="stMetricDelta"] {
            font-weight: 600;
        }
        
        /* Custom Buttons - Executive Navy Gradient */
        .stButton > button {
            background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
            color: #FFFFFF !important;
            border: none;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(30, 58, 138, 0.25);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            font-weight: 600;
            letter-spacing: 0.5px;
            padding: 0.6rem 1.2rem;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(30, 58, 138, 0.4);
            color: #FFFFFF;
        }
        
        /* Expander Headers */
        .streamlit-expanderHeader {
            background-color: rgba(248, 250, 252, 0.7);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(226, 232, 240, 0.8);
            border-radius: 8px;
            font-weight: 600;
            color: #1E293B;
        }
        .streamlit-expanderHeader:hover {
            color: #2563EB;
            border-color: rgba(147, 197, 253, 0.5);
            background-color: rgba(241, 245, 249, 0.9);
        }
        
        /* Info Boxes */
        .stAlert {
            background: rgba(239, 246, 255, 0.8) !important;
            backdrop-filter: blur(5px);
            border: 1px solid rgba(191, 219, 254, 0.8) !important;
            border-radius: 8px !important;
            color: #1E3A8A !important;
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
            "💬 SecOps Copilot"
        ]
    )
    
    # Strip emojis for routing logic
    domain = domain_selection.split(" ", 1)[1] if " " in domain_selection else domain_selection
    
    st.sidebar.markdown("---")
    st.sidebar.info("This application synthesizes context and simulates Agent interventions safely.")
    if st.sidebar.button("Regenerate Context Data"):
        st.cache_data.clear()
        st.cache_resource.clear()
        del st.session_state.dataset
        if 'kpis' in st.session_state:
            del st.session_state.kpis
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
    elif "SecOps Copilot" in domain:
        from app.views.chatbot import render_chatbot
        render_chatbot(kpis, dataset)

if __name__ == "__main__":
    main()
