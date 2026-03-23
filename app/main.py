import streamlit as st
from dotenv import load_dotenv
import time
import os

from app.data_generator.generator import SecurityDataGenerator
from app.data_generator.rag_generator import RAGDataGenerator
from app.kpi_engine.calculator import KPICalculator
from app.agents.rag_engine import SECopsRAGEngine
from app.utils.workflow_utils import RemediationWorkflow

# Import views
from app.views.dashboard import render_dashboard
from app.views.major_incident import render_major_incident_management
from app.views.provisioning import render_provisioning
from app.views.automation import render_automation
from app.views.asset_visibility import render_asset_visibility
from app.views.compliance import render_compliance
from app.views.detection_response import render_detection_response
from app.views.secops import render_secops
from app.views.login import check_password

load_dotenv(override=True)

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
        
    # 4. Remediation Workflow State
    if 'remediation_workflows' not in st.session_state:
        # Standard domains/phases for tickets
        domains = ['major incident management', 'provisioning', 'automation', 
                   'asset visibility', 'compliance', 'detection & response', 
                   'security operations', 'identified', 'approved', 'implemented', 'verified', 'closed']
        st.session_state.remediation_workflows = {d: [] for d in domains}
        
    if 'approval_queue' not in st.session_state:
        st.session_state.approval_queue = []
        
    if 'workflow_audit_log' not in st.session_state:
        st.session_state.workflow_audit_log = []

def main():
    st.markdown("""
        <style>
        /* ═══════════════════════════════════════════════════════════════
           EXECUTIVE ENTERPRISE SecOps — Premium Light Theme
           ═══════════════════════════════════════════════════════════════ */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
        
        /* ── Global Canvas ── */
        .stApp {
            background-color: #F8FAFC;
            color: #1E293B;
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #0F172A !important;
            font-weight: 700;
            letter-spacing: -0.02em;
        }
        
        /* ── Hide Streamlit chrome ── */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* ── Main Content Area ── */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            max-width: 100% !important;
        }
        [data-testid="stAppViewBlockContainer"] {
            padding-top: 1rem !important;
            padding-bottom: 0.5rem !important;
        }
        div[data-testid="stVerticalBlock"] {
            gap: 0.5rem !important;
        }
        div[data-testid="stVerticalBlock"] > div {
            padding-top: 0px !important;
            padding-bottom: 3px !important;
        }

        /* ── Sidebar — Clean White ── */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E2E8F0 !important;
            box-shadow: 1px 0 8px rgba(15, 23, 42, 0.04) !important;
        }
        [data-testid="stSidebar"] section {
            padding-top: 1rem !important;
        }
        /* Hide native radio circles */
        [data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {
            display: none !important;
        }
        [data-testid="stSidebar"] .stRadio label {
            padding: 8px 14px !important;
            border-radius: 8px;
            font-size: 0.88rem !important;
            color: #475569;
            transition: all 0.2s ease;
        }
        [data-testid="stSidebar"] .stRadio label:hover {
            background-color: #EFF6FF;
            color: #1D4ED8;
        }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            font-size: 0.92rem !important;
        }

        /* ── Metric Cards — Refined ── */
        [data-testid="metric-container"] {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 12px 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            transition: all 0.2s ease;
        }
        [data-testid="metric-container"]:hover {
            border-color: #93C5FD;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.08);
        }
        [data-testid="stMetricValue"] {
            color: #1E3A8A !important;
            font-weight: 700;
            font-size: 1.5rem !important;
        }
        [data-testid="stMetricDelta"] {
            font-weight: 600;
            font-size: 0.78rem !important;
        }

        /* ── Buttons — Subtle Accent ── */
        .stButton > button {
            background: #1E40AF;
            color: #FFFFFF !important;
            border: none;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(30, 64, 175, 0.2);
            transition: all 0.2s ease;
            font-weight: 600;
            letter-spacing: 0.3px;
            padding: 0.55rem 1.2rem;
        }
        .stButton > button:hover {
            background: #1E3A8A;
            box-shadow: 0 4px 14px rgba(30, 58, 138, 0.3);
            color: #FFFFFF !important;
        }

        /* ── Tabs — Clean ── */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            border-bottom: 2px solid #E2E8F0;
        }
        .stTabs [data-baseweb="tab"] {
            height: 36px;
            font-size: 0.88rem !important;
            font-weight: 500;
            border-radius: 6px 6px 0 0;
        }

        /* ── Expanders ── */
        .streamlit-expanderHeader {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            font-weight: 600;
            color: #1E293B;
            padding: 0.6rem 1rem !important;
        }
        .streamlit-expanderHeader:hover {
            color: #1D4ED8;
            border-color: #93C5FD;
            background-color: #F8FAFC;
        }

        /* ── Alert / Info Boxes ── */
        .stAlert {
            background: #F0F7FF !important;
            border: 1px solid #BFDBFE !important;
            border-radius: 8px !important;
            color: #1E3A8A !important;
            padding: 0.5rem 0.75rem !important;
            margin-bottom: 0.5rem !important;
        }

        /* ── Dataframes ── */
        [data-testid="stDataFrame"] {
            border: 1px solid #E2E8F0;
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

    if not check_password():
        st.stop()

    from app.views.login import render_persona
    render_persona()

    # Smooth transition loader for the first login run
    if 'dataset' not in st.session_state:
        loading_ui = st.empty()
        with loading_ui.container():
            st.markdown("""
                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 75vh; text-align: center;">
                    <div style="font-size: 50px; margin-bottom: 20px; animation: pulse 2s infinite;">🔐</div>
                    <h2 style="color: #1E3A8A; font-family: 'Outfit', sans-serif; font-weight: 800;">Command Center Authenticated</h2>
                    <p style="color: #64748B; font-size: 16px;">Synthesizing Enterprise Environment & Booting AI Agents...</p>
                    <style>
                        @keyframes pulse {
                            0% { transform: scale(1); opacity: 1; }
                            50% { transform: scale(1.1); opacity: 0.8; }
                            100% { transform: scale(1); opacity: 1; }
                        }
                        /* Hide sidebar during load to prevent stutter */
                        [data-testid="stSidebar"] { display: none; }
                    </style>
                </div>
            """, unsafe_allow_html=True)
            init_session_state()
        loading_ui.empty()
    else:
        init_session_state()

    
    st.sidebar.title("GenAI Orchestrator Domains")
    
    domain_selection = st.sidebar.radio(
        "Navigation",
        [
            "📊 Executive Dashboard",
            "🚨 Major Incidents (MI)",
            "⚡ Time to Provision",
            "🤖 Automation Index",
            "🔍 Asset Visibility & Coverage",
            "⚖️ Compliance",
            "🛡️ Efficiency in Detection & Response",
            "⚙️ Intelligent IT Security Operations",
            "🕵️ Agents View",
            "📂 Synthetic Data Explorer",
            "💬 SecOps Copilot"
        ]
    )
    
    # Strip emojis for routing logic
    domain = domain_selection.split(" ", 1)[1] if " " in domain_selection else domain_selection
    
    st.sidebar.markdown("---")
    st.sidebar.info("This application synthesizes context and simulates Agent interventions safely.")
    if st.sidebar.button("Regenerate Context Data", width='stretch'):
        st.cache_data.clear()
        st.cache_resource.clear()
        del st.session_state.dataset
        if 'kpis' in st.session_state:
            del st.session_state.kpis
        st.rerun()
        
    if st.sidebar.button("Logout", width='stretch'):
        st.session_state["password_correct"] = False
        st.rerun()
        
    kpis = st.session_state.kpis
    dataset = st.session_state.dataset
    
    # Virtual Routing
    if domain == "Executive Dashboard":
        render_dashboard(kpis, dataset)
    elif domain == "Major Incidents (MI)":
        render_major_incident_management(kpis, dataset)
    elif domain == "Time to Provision":
        render_provisioning(kpis, dataset)
    elif domain == "Automation Index":
        render_automation(kpis, dataset)
    elif domain == "Asset Visibility & Coverage":
        render_asset_visibility(kpis, dataset)
    elif domain == "Compliance":
        render_compliance(kpis, dataset)
    elif domain == "Efficiency in Detection & Response":
        render_detection_response(kpis, dataset)
    elif domain == "Intelligent IT Security Operations":
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

