import streamlit as st
import streamlit.components.v1 as components
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
    page_title="Autonomous Security Tools Operations",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────────────────────────────────────
# FORCE SIDEBAR EXPANDED - Runs after login (inside main() after check_password)
# ──────────────────────────────────────────────────────────────────────────────
def force_sidebar_expanded():
    """Inject JavaScript to force sidebar expansion."""
    components.html(
        """
        <script>
        (function() {
            console.log("Sidebar expand script running");
            function expandSidebar() {
                // Try all possible selectors for the collapse/expand button
                const selectors = [
                    '[data-testid="collapsedControl"]',
                    '[data-testid="stSidebarCollapsedControl"]',
                    'button[kind="sidebarCollapse"]',
                    '.st-emotion-cache-1wmy9hl',  // common class for collapse button
                    'button[aria-label="Collapse sidebar"]',
                    'button[aria-label="Expand sidebar"]'
                ];
                let btn = null;
                for (let sel of selectors) {
                    btn = window.parent.document.querySelector(sel);
                    if (btn) break;
                }
                if (btn) {
                    console.log("Found expand/collapse button, clicking...");
                    btn.click();
                    return true;
                }
                // If button not found, check if sidebar is already visible
                const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
                if (sidebar) {
                    const style = window.getComputedStyle(sidebar);
                    const isVisible = style.display !== 'none' && style.width !== '0px' && style.visibility !== 'hidden';
                    if (!isVisible) {
                        console.log("Sidebar hidden but button not found, trying to force via CSS");
                        sidebar.style.display = 'block';
                        sidebar.style.width = '80px';
                        sidebar.style.minWidth = '80px';
                        return true;
                    }
                }
                return false;
            }
            // Run multiple times to catch Streamlit's hydration
            setTimeout(expandSidebar, 200);
            setTimeout(expandSidebar, 500);
            setTimeout(expandSidebar, 1000);
            // Also watch for DOM changes
            const observer = new MutationObserver(function(mutations) {
                expandSidebar();
            });
            observer.observe(window.parent.document.body, { childList: true, subtree: true });
        })();
        </script>
        """,
        height=0,
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
        st.session_state.rag_engine = get_cached_rag_engine(
            st.session_state.rag_kedb, 
            st.session_state.rag_tickets
        )
        
    # 4. Remediation Workflow State
    if 'remediation_workflows' not in st.session_state:
        domains = ['major incident management', 'provisioning', 'automation', 
                   'asset visibility', 'compliance', 'detection & response', 
                   'security operations', 'identified', 'approved', 'implemented', 'verified', 'closed']
        st.session_state.remediation_workflows = {d: [] for d in domains}
        
    if 'approval_queue' not in st.session_state:
        st.session_state.approval_queue = []
        
    if 'workflow_audit_log' not in st.session_state:
        st.session_state.workflow_audit_log = []

def main():
    # ═══════════════════════════════════════════════════════════════
    # GLOBAL CSS — Premium Dark Theme, Horizontal Layout
    # CRITICAL: Force sidebar to be visible and fixed width
    # ═══════════════════════════════════════════════════════════════
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        /* ── Global Canvas ── */
        .stApp {
            background-color: #020617;
            color: #F8FAFC;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #FFFFFF !important;
            font-weight: 700;
            letter-spacing: -0.02em;
            font-family: 'Inter', sans-serif !important;
        }
        
        /* ── Hide Streamlit chrome (menu, footer, header) ── */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* ── FORCE SIDEBAR VISIBLE & FIXED WIDTH ── */
        [data-testid="stSidebar"] {
            width: 80px !important;
            min-width: 80px !important;
            max-width: 80px !important;
            background-color: #0B1120 !important;
            border-right: 1px solid #1E293B;
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
            transition: none !important;
            transform: none !important;
            margin-left: 0 !important;
            left: 0 !important;
            position: relative !important;
        }

        /* Completely hide all collapse/expand buttons */
        button[kind="sidebarCollapse"],
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapsedControl"],
        [aria-label="Collapse sidebar"],
        [aria-label="Expand sidebar"] {
            display: none !important;
            visibility: hidden !important;
            width: 0 !important;
            height: 0 !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }

        /* Sidebar action buttons – icon only, full width */
        [data-testid="stSidebar"] button {
            width: 100%;
            justify-content: center;
            background: transparent !important;
            border: none !important;
            font-size: 24px;
            padding: 10px 0;
            color: #94A3B8 !important;
            box-shadow: none !important;
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            background: #1E293B !important;
            color: #3B82F6 !important;
        }

        /* Ensure sidebar content is visible */
        [data-testid="stSidebarContent"] {
            padding-top: 1rem;
            display: block !important;
            visibility: visible !important;
        }

        /* ── Main Content Area — tighter spacing ── */
        .block-container {
            padding-top: 0.5rem !important;
            padding-bottom: 0.5rem !important;
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
            max-width: 100% !important;
        }
        [data-testid="stAppViewBlockContainer"] {
            padding-top: 0.5rem !important;
            padding-bottom: 0.5rem !important;
        }
        div[data-testid="stVerticalBlock"] {
            gap: 0.4rem !important;
        }
        div[data-testid="stVerticalBlock"] > div {
            padding-top: 0px !important;
            padding-bottom: 2px !important;
        }

        /* ── Horizontal Nav Tabs — Clean, Sticky ── */
        .stTabs [data-baseweb="tab-list"] {
            background: #020617;
            border-bottom: 2px solid #1E293B;
            padding: 0 8px;
            gap: 0;
            border-radius: 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        }
        .stTabs [data-baseweb="tab"] {
            height: auto;
            padding: 10px 18px;
            font-size: 0.82rem !important;
            font-weight: 600;
            border-radius: 0;
            border-bottom: 3px solid transparent;
            color: #94A3B8;
            transition: all 0.2s ease;
            white-space: nowrap;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: #3B82F6;
            background: #1E293B;
        }
        .stTabs [aria-selected="true"] {
            border-bottom-color: #3B82F6 !important;
            color: #3B82F6 !important;
            background: #0F172A !important;
        }
        /* Hide the default tab highlight bar */
        .stTabs [data-baseweb="tab-highlight"] {
            display: none !important;
        }
        .stTabs [data-baseweb="tab-border"] {
            display: none !important;
        }

        /* ── Metric Cards — Refined ── */
        [data-testid="metric-container"] {
            background: #0B1120;
            border: 1px solid #1E293B;
            border-radius: 10px;
            padding: 12px 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            transition: all 0.2s ease;
        }
        [data-testid="metric-container"]:hover {
            border-color: #3B82F6;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
        }
        [data-testid="stMetricValue"] {
            color: #FFFFFF !important;
            font-weight: 700;
            font-size: 1.4rem !important;
        }
        [data-testid="stMetricDelta"] {
            font-weight: 600;
            font-size: 0.75rem !important;
        }

        /* ── Buttons — Subtle Accent ── */
        .stButton > button {
            background: #3B82F6;
            color: #FFFFFF !important;
            border: none;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(59, 130, 246, 0.2);
            transition: all 0.2s ease;
            font-weight: 600;
            letter-spacing: 0.3px;
            padding: 0.5rem 1.1rem;
            font-size: 0.85rem;
        }
        .stButton > button:hover {
            background: #2563EB;
            box-shadow: 0 4px 14px rgba(59, 130, 246, 0.3);
            color: #FFFFFF !important;
        }

        /* ── Expanders — Clean ── */
        .streamlit-expanderHeader {
            background-color: #0B1120;
            border: 1px solid #1E293B;
            border-radius: 10px;
            font-weight: 600;
            color: #F8FAFC;
            padding: 0.5rem 0.8rem !important;
            font-size: 0.88rem;
        }
        .streamlit-expanderHeader:hover {
            color: #3B82F6;
            border-color: #3B82F6;
        }

        /* ── Alert / Info Boxes ── */
        .stAlert {
            background: #0F172A !important;
            border: 1px solid #1E3A8A !important;
            border-radius: 8px !important;
            color: #93C5FD !important;
            padding: 0.4rem 0.7rem !important;
            margin-bottom: 0.4rem !important;
            font-size: 0.85rem !important;
        }

        /* ── Dataframes ── */
        [data-testid="stDataFrame"] {
            border: 1px solid #1E293B;
            border-radius: 8px;
        }

        /* ── Demo Tile Cards ── */
        .demo-tile {
            background: #0B1120;
            border: 1px solid #1E293B;
            border-radius: 12px;
            padding: 16px 18px;
            transition: all 0.25s ease;
            box-shadow: 0 1px 3px rgba(0,0,0,0.15);
            height: 100%;
        }
        .demo-tile:hover {
            border-color: #3B82F6;
            box-shadow: 0 6px 20px rgba(59,130,246,0.12);
            transform: translateY(-2px);
        }
        .demo-tile h5 {
            margin: 0 0 6px 0 !important;
            font-size: 0.88rem !important;
            color: #F8FAFC !important;
            font-weight: 700 !important;
        }
        .demo-tile p {
            margin: 0;
            font-size: 0.78rem;
            color: #94A3B8;
            line-height: 1.45;
        }
        .demo-tile .agent-badge {
            display: inline-block;
            background: #1E293B;
            color: #93C5FD;
            font-size: 0.68rem;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 12px;
            margin-top: 8px;
            border: 1px solid #3B82F6;
        }

        /* ── KPI Card Tiles ── */
        .kpi-card {
            background: #0B1120;
            border: 1px solid #1E293B;
            border-radius: 12px;
            padding: 14px 16px;
            margin-bottom: 20px;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            transition: all 0.2s ease;
        }
        .kpi-card:hover {
            border-color: #3B82F6;
            box-shadow: 0 4px 12px rgba(59,130,246,0.15);
        }
        .kpi-card .kpi-value {
            font-size: 1.5rem;
            font-weight: 800;
            color: #FFFFFF;
            margin: 4px 0;
        }
        .kpi-card .kpi-label {
            font-size: 0.72rem;
            font-weight: 600;
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .kpi-card .kpi-sub {
            font-size: 0.7rem;
            color: #64748B;
            margin-top: 2px;
        }
        </style>
    """, unsafe_allow_html=True)

    if not check_password():
        st.stop()

    # Force sidebar expanded after login (critical)
    force_sidebar_expanded()

    # Smooth transition loader for the first login run
    if 'dataset' not in st.session_state:
        loading_ui = st.empty()
        with loading_ui.container():
            st.markdown("""
                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 75vh; text-align: center;">
                    <div style="font-size: 50px; margin-bottom: 20px; animation: pulse 2s infinite;">🔐</div>
                    <h2 style="color: #1E3A8A; font-family: 'Inter', sans-serif; font-weight: 800;">Command Center Authenticated</h2>
                    <p style="color: #64748B; font-size: 16px;">Synthesizing Enterprise Environment & Booting AI Agents...</p>
                    <style>
                        @keyframes pulse {
                            0% { transform: scale(1); opacity: 1; }
                            50% { transform: scale(1.1); opacity: 0.8; }
                            100% { transform: scale(1); opacity: 1; }
                        }
                    </style>
                </div>
            """, unsafe_allow_html=True)
            init_session_state()
        loading_ui.empty()
    else:
        init_session_state()

    # ═══════════════════════════════════════════════════════════════
    # TOP NAVIGATION BAR
    # ═══════════════════════════════════════════════════════════════
    username = os.getenv("ADMIN_USERNAME", "admin").capitalize()
    initials = username[:2].upper()
    
    st.markdown(f"""
        <div style="background: #0F172A; padding: 8px 12px 8px 60px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1E293B; margin: -8px -24px 8px -24px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 1.4rem;">🛡️</span>
                <div>
                    <span style="font-family: 'Inter', sans-serif; font-size: 1.05rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.5px;">Autonomous Security Tools Operations</span>
                    <span style="font-family: 'Inter', sans-serif; font-size: 0.75rem; color: #94A3B8; margin-left: 8px;">Command Center</span>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 16px;">
                <div style="display: flex; flex-direction: column; align-items: flex-end;">
                    <span style="font-family: 'Inter', sans-serif; font-size: 12px; font-weight: 700; color: #FFFFFF; line-height: 1.2;">{username}</span>
                    <span style="font-family: 'Inter', sans-serif; font-size: 10px; font-weight: 500; color: #94A3B8; line-height: 1.2;">SecOps Administrator</span>
                </div>
                <div style="width: 32px; height: 32px; border-radius: 50%; background: #3B82F6; color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; font-family: 'Inter', sans-serif; font-size: 13px;">
                    {initials}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Utility buttons row & Global View State
    if 'active_view' not in st.session_state:
        st.session_state.active_view = 'main'
        
    with st.sidebar:
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        if st.button("📊", help="Main Dashboards", use_container_width=True):
            st.session_state.active_view = 'main'
            st.rerun()
        if st.button("📂", help="Data Explorer", use_container_width=True):
            st.session_state.active_view = 'data'
            st.rerun()
        if st.button("🕵️", help="Agents & Tools", use_container_width=True):
            st.session_state.active_view = 'agents'
            st.rerun()
        if st.button("🤖", help="SecOps Copilot", use_container_width=True):
            st.session_state.active_view = 'copilot'
            st.rerun()
            
        st.markdown("<div style='height: 40vh;'></div>", unsafe_allow_html=True)
        
        if st.button("🔄", help="Regenerate Context", use_container_width=True):
            st.cache_data.clear()
            st.cache_resource.clear()
            for k in ['dataset', 'kpis', 'rag_kedb', 'rag_tickets', 'rag_engine']:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()
        if st.button("🚪", help="Logout", use_container_width=True):
            st.session_state["password_correct"] = False
            st.rerun()

    kpis = st.session_state.kpis
    dataset = st.session_state.dataset

    # ═══════════════════════════════════════════════════════════════
    # HORIZONTAL DOMAIN TABS — NorthStar Labels
    # ═══════════════════════════════════════════════════════════════
    if st.session_state.active_view == 'main':
        if 'active_domain_tab' not in st.session_state:
            st.session_state.active_domain_tab = "📊 Dashboard"
            
        domain_tabs = [
            "📊 Dashboard", "🎯 Zero MI", "⚡ Zero Touch", "🤖 Zero Toil", 
            "🔍 Zero Visibility Gap", "⚖️ Zero Non-Compliance", "🛡️ Zero False Positive", "⚙️ Intelligent Ops"
        ]
        
        # UI Styling to make buttons act like seamless tabs
        st.markdown("""
            <style>
            div[data-testid="stHorizontalBlock"] button {
                padding: 4px 0px;
                font-size: 11.5px !important;
                border: none !important;
                background: #0F172A;
                color: #94A3B8;
                border-radius: 8px 8px 0 0 !important;
                border-bottom: 2px solid transparent !important;
                box-shadow: none !important;
                transition: all 0.2s ease;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            div[data-testid="stHorizontalBlock"] button:hover {
                color: #FFFFFF;
                background: #1E293B;
                border-bottom: 2px solid #3B82F6 !important;
            }
            div[data-testid="stHorizontalBlock"] button[kind="primary"] {
                color: #FFFFFF !important;
                background: transparent !important;
                border-bottom: 2px solid #3B82F6 !important;
                font-weight: bold;
            }
            </style>
        """, unsafe_allow_html=True)
        
        # Allocate dynamic widths based on character length to prevent text wrap
        col_weights = [1.0, 0.85, 1.1, 1.0, 1.6, 1.6, 1.5, 1.35]
        cols = st.columns(col_weights, gap="small")
        for idx, tab_name in enumerate(domain_tabs):
            with cols[idx]:
                if st.button(
                    tab_name, 
                    use_container_width=True, 
                    type="primary" if st.session_state.active_domain_tab == tab_name else "secondary"
                ):
                    st.session_state.active_domain_tab = tab_name
                    st.rerun()
                    
        st.markdown("<div style='height: 1px; background: #1E293B; margin-top: -16px; margin-bottom: 24px;'></div>", unsafe_allow_html=True)
        
        tab = st.session_state.active_domain_tab
        if tab == "📊 Dashboard": render_dashboard(kpis, dataset)
        elif tab == "🎯 Zero MI": render_major_incident_management(kpis, dataset)
        elif tab == "⚡ Zero Touch": render_provisioning(kpis, dataset)
        elif tab == "🤖 Zero Toil": render_automation(kpis, dataset)
        elif tab == "🔍 Zero Visibility Gap": render_asset_visibility(kpis, dataset)
        elif tab == "⚖️ Zero Non-Compliance": render_compliance(kpis, dataset)
        elif tab == "🛡️ Zero False Positive": render_detection_response(kpis, dataset)
        elif tab == "⚙️ Intelligent Ops": render_secops(kpis, dataset)
    elif st.session_state.active_view == 'data':
        from app.views.data_explorer import render_data_explorer
        render_data_explorer(dataset)
        
    elif st.session_state.active_view == 'agents':
        from app.views.agent_console import render_agent_console
        render_agent_console(kpis, dataset)
        
    elif st.session_state.active_view == 'copilot':
        from app.views.chatbot import render_chatbot
        render_chatbot(kpis, dataset)

if __name__ == "__main__":
    main()