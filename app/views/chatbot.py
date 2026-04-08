import streamlit as st
import pandas as pd
from app.agents.manager import AgentManager
import os

def render_rag_workflow():
    """Renders a premium, executive-level visual depiction of the RAG data flow."""
    st.markdown("""
        <style>
        .rag-pipeline {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #FFFFFF;
            padding: 30px;
            border-radius: 16px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 10px 25px rgba(30, 58, 138, 0.05);
            margin-bottom: 30px;
        }
        .pipeline-node {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            flex: 1;
        }
        .node-icon {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            margin-bottom: 12px;
            border: 1px solid #BFDBFE;
            transition: all 0.3s ease;
        }
        .node-icon.active {
            background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
            color: white;
            box-shadow: 0 8px 15px rgba(30, 58, 138, 0.2);
            border: none;
        }
        .node-label {
            font-size: 0.85rem;
            font-weight: 700;
            color: #1E293B;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .node-subtext {
            font-size: 0.75rem;
            color: #64748B;
            margin-top: 4px;
        }
        .pipeline-arrow {
            font-size: 24px;
            color: #CBD5E1;
            padding: 0 10px;
            margin-bottom: 30px;
            animation: pulse-arrow 2s infinite;
        }
        @keyframes pulse-arrow {
            0% { transform: translateX(0); opacity: 0.4; }
            50% { transform: translateX(5px); opacity: 1; }
            100% { transform: translateX(0); opacity: 0.4; }
        }
        </style>
        
        <div class="rag-pipeline">
            <div class="pipeline-node">
                <div class="node-icon">📚</div>
                <div class="node-label">KEDB</div>
                <div class="node-subtext">50 Fixes</div>
            </div>
            <div class="pipeline-arrow">➔</div>
            <div class="pipeline-node">
                <div class="node-icon">🎫</div>
                <div class="node-label">ITIL Tickets</div>
                <div class="node-subtext">60 CR/SR/INC</div>
            </div>
            <div class="pipeline-arrow">➔</div>
            <div class="pipeline-node">
                <div class="node-icon active">🧠</div>
                <div class="node-label">FAISS Core</div>
                <div class="node-subtext">Vector Store</div>
            </div>
            <div class="pipeline-arrow">➔</div>
            <div class="pipeline-node">
                <div class="node-icon">🔍</div>
                <div class="node-label">Semantic</div>
                <div class="node-subtext">Retrieval</div>
            </div>
            <div class="pipeline-arrow">➔</div>
            <div class="pipeline-node">
                <div class="node-icon active" style="background: linear-gradient(135deg, #059669 0%, #10B981 100%);">🤖</div>
                <div class="node-label">SecOps AI</div>
                <div class="node-subtext">Copilot</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_chatbot(kpis: dict, dataset: dict):
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; background: #E0E7FF; padding: 5px 15px; border-radius: 8px; margin-bottom: 5px; border-left: 5px solid #1E3A8A;">
            <h4 style="margin: 0; color: #1E3A8A; font-size: 1rem;">🛡️ SecOps Copilot</h4>
            <p style="margin: 0; font-size: 0.82rem; color: #1E40AF;"><b>Objective:</b> AI-powered RAG assistant for enterprise security analysis.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Render the premium workflow visualization
    render_rag_workflow()
    
    # Create Tabs for a cleaner Layout
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Copilot Chat", "📚 KEDB Database", "🎫 SecOps Tickets", "🕸️ Knowledge Graph"])
    
    kedb_df = st.session_state.get('rag_kedb', pd.DataFrame())
    tickets_df = st.session_state.get('rag_tickets', pd.DataFrame())
    
    with tab1:
        st.markdown("### 🤖 Security Analyst Copilot")
        st.caption("Ask questions about securing the enterprise. The Copilot will automatically query the FAISS memory banks (KEDB & Tickets) in real-time to augment its answers.")
        
        # Reference questions for new production-realistic datasets
        st.markdown("""
        <div style="margin-bottom: 12px;">
            <span style="font-size: 0.78rem; color: #64748B; font-weight: 600;">💡 Try asking:</span>
            <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: 5px;">
                <span style="background: #EFF6FF; color: #1E40AF; padding: 4px 10px; border-radius: 16px; font-size: 0.75rem; border: 1px solid #BFDBFE; cursor: pointer;">🔍 Show CrowdStrike EDR events flagged as malicious</span>
                <span style="background: #FEF3C7; color: #92400E; padding: 4px 10px; border-radius: 16px; font-size: 0.75rem; border: 1px solid #FDE68A; cursor: pointer;">⚖️ Which firewall rules are drifting from CIS baseline?</span>
                <span style="background: #FEE2E2; color: #991B1B; padding: 4px 10px; border-radius: 16px; font-size: 0.75rem; border: 1px solid #FECACA; cursor: pointer;">🛡️ Any DLP incidents with credit card data leaks?</span>
                <span style="background: #ECFDF5; color: #065F46; padding: 4px 10px; border-radius: 16px; font-size: 0.75rem; border: 1px solid #A7F3D0; cursor: pointer;">📋 Show access log anomalies with 401/403 errors</span>
                <span style="background: #F5F3FF; color: #5B21B6; padding: 4px 10px; border-radius: 16px; font-size: 0.75rem; border: 1px solid #DDD6FE; cursor: pointer;">🔥 Which firewalls have critical config drift?</span>
                <span style="background: #FFF7ED; color: #9A3412; padding: 4px 10px; border-radius: 16px; font-size: 0.75rem; border: 1px solid #FED7AA; cursor: pointer;">📊 What is the DLP policy coverage for PCI-DSS?</span>
                <span style="background: #FCE7F3; color: #9D174D; padding: 4px 10px; border-radius: 16px; font-size: 0.75rem; border: 1px solid #FBCFE8; cursor: pointer;">🔁 Which assets have recurring incidents and what's the root cause?</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize chat history
        if "copilot_messages" not in st.session_state:
            st.session_state.copilot_messages = [
                {
                    "role": "assistant", 
                    "content": "Hello! I am your SecOps Copilot. I have analyzed the active Known Error Database, current Incident Tickets, and enterprise telemetry including CrowdStrike EDR, firewall logs, DLP incidents, and access logs. How can I assist with your investigation today?"
                }
            ]

        # Display chat messages
        for msg in st.session_state.copilot_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # React to user input
        if prompt := st.chat_input("E.g., Show me CrowdStrike EDR events with RansomwareActivity on Windows hosts"):
            
            st.chat_message("user").markdown(prompt)
            st.session_state.copilot_messages.append({"role": "user", "content": prompt})

            if not os.getenv("OPENAI_API_KEY"):
                response = "Error: OPENAI_API_KEY is required to contact the FAISS embeddings and LLM."
                with st.chat_message("assistant"):
                    st.markdown(response)
                st.session_state.copilot_messages.append({"role": "assistant", "content": response})
                return

            with st.chat_message("assistant"):
                with st.spinner("Searching FAISS Index..."):
                    
                    # Retrieve context from RAG Engine
                    rag_engine = st.session_state.get("rag_engine")
                    if rag_engine:
                        retrieved_context = rag_engine.retrieve_context(prompt, top_k=4)
                    else:
                        retrieved_context = "ERROR: Vector Engine Offline."
                    
                    with st.expander("🔍 View Retrieved Knowledge Base Context", expanded=False):
                        st.text(retrieved_context)

                    manager = AgentManager()
                    platform_context = manager._build_context(kpis)
                    
                    dataset = st.session_state.get('dataset', {})
                    synthetic_samples_str = "3. SYNTHETIC TELEMETRY & OBSERVABILITY DB (Live Data Snippets):\n"
                    for d_key, d_df in dataset.items():
                         if isinstance(d_df, pd.DataFrame) and not d_df.empty:
                              synthetic_samples_str += f"[{d_key.upper()} - 5 rows sample]:\n" + d_df.head(5).to_csv(index=False) + "\n"
                    
                    # Merge Platform Awareness with RAG Retrieval
                    system_prompt = f"""
                    You are "SecOps Copilot", the master AI assistant for this GenAI SecOps Platform.
                    You have total executive visibility into the entire application.
                    
                    SOURCES OF TRUTH:
                    1. ENVIRONMENT KPIs & PLATFORM INFO (Live Status):
                    {platform_context}
                    
                    2. KNOWLEDGE BASE & TICKETS (Operational Data from FAISS):
                    {retrieved_context}
                    
                    {synthetic_samples_str}
                    
                    YOUR MISSION:
                    - You must answer ANY question about this application, including:
                      * ALL DOMAINS: Incident Management, Provisioning, Automation (SOAR), Asset Visibility, Compliance, and Detection & Response.
                      * KPI CALCULATIONS: Explain MTTR, MTTD, coverage rates, and alert volumes based on the Live Status provided above.
                      * TECHNICAL RESOLUTIONS: Use the KEDB and Tickets retrieval context to provide specific fix instructions (referencing Ticket/KE IDs).
                      * TELEMETRY & LOG INVESTIGATION: Actively use the SYNTHETIC TELEMETRY snippets (IPs, Event IDs, Packets, Users, Config Baselines) as your authoritative data source when explaining how you detected or resolved threats. Mention specific IP addresses and specific tools (Gigamon, Crowdstrike).
                    - Be professional, authoritative, and concise. 
                    - If you see a discrepancy, explain it based on the live data provided in the KPIs.
                    
                    USER QUERY: {prompt}
                    """
                    
                    response = manager.run_agent(
                        role="SecOps Copilot", 
                        kpis=kpis, 
                        custom_instruction=system_prompt
                    )
                    
                    st.markdown(response)
                    
            st.session_state.copilot_messages.append({"role": "assistant", "content": response})

    with tab2:
        st.markdown("### 📚 Known Error Database (KEDB)")
        st.markdown("This synthetic view represents established operational fixes mapped by Error ID and Tool.")
        if not kedb_df.empty:
            st.dataframe(kedb_df, width='stretch', hide_index=True)
            
            # Download capability
            csv = kedb_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download KEDB as CSV",
                data=csv,
                file_name="synthetic_kedb_database.csv",
                mime="text/csv",
                key="dl_kedb"
            )
        else:
            st.warning("KEDB dataset has not been initialized.")
            
    with tab3:
        st.markdown("### 🎫 SecOps Tickets")
        st.markdown("This synthetic feed represents live/historical Service Requests, Incidents, and Change Orders.")
        if not tickets_df.empty:
            st.dataframe(tickets_df, width='stretch', hide_index=True)
            
            # Download capability
            csv = tickets_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Tickets as CSV",
                data=csv,
                file_name="synthetic_secops_tickets.csv",
                mime="text/csv",
                key="dl_tickets"
            )
        else:
            st.warning("Tickets dataset has not been initialized.")

    with tab4:
        st.markdown("### 🕸️ SecOps Knowledge Graph")
        st.markdown("Data-flow visualization: **Domain → Demo → Inputs → Output → KPIs**")
        
        try:
            from pyvis.network import Network
            import networkx as nx
            import tempfile
            from app.views.shared import load_demo_requirements
            
            records = load_demo_requirements()
            
            # ── Interactive Filters ───────────────────────────────
            filter_cols = st.columns([2, 1, 1, 1, 1])
            
            all_domains = sorted(list(set(str(r.get('Category', 'Unknown')) for r in records)))
            with filter_cols[0]:
                selected_domain = st.selectbox("🔍 Filter by Domain", ["All Domains"] + all_domains, key="kg_domain_filter")
            with filter_cols[1]:
                show_inputs = st.checkbox("Inputs", value=True, key="kg_show_inputs")
            with filter_cols[2]:
                show_outputs = st.checkbox("Outputs", value=True, key="kg_show_outputs")
            with filter_cols[3]:
                show_kpis = st.checkbox("KPIs", value=True, key="kg_show_kpis")
            with filter_cols[4]:
                show_agents = st.checkbox("Agents", value=False, key="kg_show_agents2")
            
            # ── Color Scheme ──────────────────────────────────────
            CLR_DOMAIN = "#1E3A8A"    # Navy — top-level
            CLR_DEMO   = "#3B82F6"    # Blue — demo/capability
            CLR_INPUT  = "#8B5CF6"    # Violet — input data
            CLR_OUTPUT = "#10B981"    # Emerald — output
            CLR_KPI    = "#F59E0B"    # Amber — KPI metric
            CLR_AGENT  = "#EC4899"    # Pink — agents (optional)
            
            # ── Build Graph ───────────────────────────────────────
            G = nx.DiGraph()
            
            def _clean_label(text, max_len=38):
                """Shorten labels for graph readability."""
                text = text.strip()
                if text.startswith("regulations "):
                    text = text.replace("regulations ", "📜 ")
                if len(text) > max_len:
                    text = text[:max_len - 3] + "..."
                return text
            
            def _parse_items(raw_str, delimiter=";"):
                """Split a semicolon/comma-delimited string into clean items."""
                items = []
                for part in raw_str.split(delimiter):
                    part = part.strip()
                    if part and len(part) > 2:
                        items.append(part)
                return items
            
            for r in records:
                domain = str(r.get('Category', 'Unknown'))
                demo = str(r.get('Demo Name', 'Unknown'))
                inputs_raw = str(r.get('Inputs Required', ''))
                output_raw = str(r.get('Output', ''))
                kpis_raw = str(r.get('KPIs and Calculations', ''))
                agents_raw = str(r.get('Agents Involved', ''))
                goal = str(r.get('Goal of Demo', '')).strip()
                
                # Apply domain filter
                if selected_domain != "All Domains" and domain != selected_domain:
                    continue
                
                # ── 1. Domain Node (largest, navy) ──
                if not G.has_node(domain):
                    G.add_node(domain, nodeType="Domain",
                               title=f"<b>🏛️ Domain</b><br>{domain}",
                               size=42, color=CLR_DOMAIN,
                               font={"size": 16, "color": "#FFFFFF", "face": "Outfit, sans-serif"},
                               shape="dot")
                
                # ── 2. Demo Node ──
                demo_short = _clean_label(demo, 45)
                demo_tooltip = (
                    f"<b>⚡ Demo</b><br><b>{demo}</b>"
                    f"<hr style='margin:4px 0;border-color:#E2E8F0;'>"
                    f"<b>Goal:</b> {goal}"
                )
                if not G.has_node(demo):
                    G.add_node(demo, nodeType="Demo",
                               title=demo_tooltip, label=demo_short,
                               size=24, color=CLR_DEMO,
                               font={"size": 11, "color": "#1E293B", "face": "Outfit, sans-serif"},
                               shape="dot")
                
                # Domain → Demo
                if not G.has_edge(domain, demo):
                    G.add_edge(domain, demo,
                               color={"color": "#93C5FD", "opacity": 0.7},
                               width=2.5, arrows="to")
                
                # ── 3. Input Nodes (violet, from "Inputs Required") ──
                if show_inputs:
                    input_items = _parse_items(inputs_raw, ";")
                    for inp_raw in input_items:
                        inp_label = _clean_label(inp_raw, 35)
                        inp_id = f"📥 {inp_label}"
                        
                        if not G.has_node(inp_id):
                            G.add_node(inp_id, nodeType="Input",
                                       title=f"<b>📥 Input Data</b><br>{inp_raw.strip()}",
                                       size=16, color=CLR_INPUT,
                                       font={"size": 10, "color": "#5B21B6", "face": "Outfit, sans-serif"},
                                       shape="diamond")
                        
                        # Input → Demo (inputs feed into the demo)
                        if not G.has_edge(inp_id, demo):
                            G.add_edge(inp_id, demo,
                                       color={"color": "#C4B5FD", "opacity": 0.6},
                                       width=1.5, arrows="to",
                                       smooth={"type": "curvedCW", "roundness": 0.1})
                
                # ── 4. Output Nodes (emerald, from "Output") ──
                if show_outputs:
                    output_items = _parse_items(output_raw, ";")
                    for out_raw in output_items:
                        out_label = _clean_label(out_raw, 35)
                        out_id = f"📤 {out_label}"
                        
                        if not G.has_node(out_id):
                            G.add_node(out_id, nodeType="Output",
                                       title=f"<b>📤 Output</b><br>{out_raw.strip()}",
                                       size=18, color=CLR_OUTPUT,
                                       font={"size": 10, "color": "#065F46", "face": "Outfit, sans-serif"},
                                       shape="square")
                        
                        # Demo → Output
                        if not G.has_edge(demo, out_id):
                            G.add_edge(demo, out_id,
                                       color={"color": "#6EE7B7", "opacity": 0.7},
                                       width=2, arrows="to")
                
                # ── 5. KPI Nodes (amber, from "KPIs and Calculations") ──
                if show_kpis:
                    kpi_items = _parse_items(kpis_raw, ",")
                    for kpi_raw in kpi_items:
                        kpi_label = _clean_label(kpi_raw, 30)
                        kpi_id = f"📊 {kpi_label}"
                        
                        if not G.has_node(kpi_id):
                            G.add_node(kpi_id, nodeType="KPI",
                                       title=f"<b>📊 KPI Metric</b><br>{kpi_raw.strip()}",
                                       size=15, color=CLR_KPI,
                                       font={"size": 10, "color": "#92400E", "face": "Outfit, sans-serif"},
                                       shape="triangle")
                        
                        # Output → KPI (or Demo → KPI if outputs hidden)
                        if show_outputs:
                            for out_raw in _parse_items(output_raw, ";"):
                                out_id = f"📤 {_clean_label(out_raw, 35)}"
                                if G.has_node(out_id) and not G.has_edge(out_id, kpi_id):
                                    G.add_edge(out_id, kpi_id,
                                               color={"color": "#FCD34D", "opacity": 0.5},
                                               width=1.2, arrows="to", dashes=True)
                        else:
                            if not G.has_edge(demo, kpi_id):
                                G.add_edge(demo, kpi_id,
                                           color={"color": "#FCD34D", "opacity": 0.6},
                                           width=1.5, arrows="to", dashes=True)
                
                # ── 6. Agent Nodes (optional, pink) ──
                if show_agents:
                    agent_names = [a.strip().replace('*', '').strip() for a in agents_raw.split(',') if a.strip()]
                    for agent in agent_names:
                        if not agent or agent.lower() == "none" or "No dedicated" in agent:
                            continue
                        agent_id = f"🤖 {agent}"
                        if not G.has_node(agent_id):
                            G.add_node(agent_id, nodeType="Agent",
                                       title=f"<b>🤖 Agent</b><br>{agent}",
                                       size=20, color=CLR_AGENT,
                                       font={"size": 10, "color": "#9D174D", "face": "Outfit, sans-serif"},
                                       shape="star")
                        if not G.has_edge(demo, agent_id):
                            G.add_edge(demo, agent_id,
                                       color={"color": "#F9A8D4", "opacity": 0.5},
                                       width=1.2, arrows="to",
                                       smooth={"type": "curvedCCW", "roundness": 0.12})
            
            if len(G.nodes) == 0:
                st.info("No nodes to display. Adjust your filters.")
            else:
                # ── Create PyVis Network ──────────────────────────
                net = Network(height="580px", width="100%", bgcolor="#FFFFFF",
                              font_color="#1E293B", directed=True)
                
                # Manually add nodes (bypass from_nx which scrambles colors)
                for node_id, attrs in G.nodes(data=True):
                    net.add_node(
                        node_id,
                        label=attrs.get("label", str(node_id)),
                        title=attrs.get("title", ""),
                        size=attrs.get("size", 20),
                        color=attrs.get("color", "#999999"),
                        shape=attrs.get("shape", "dot"),
                        font=attrs.get("font", {"size": 11})
                    )
                
                # Manually add edges
                for src, dst, attrs in G.edges(data=True):
                    edge_kwargs = {
                        "source": src,
                        "to": dst,
                        "color": attrs.get("color", "#CCCCCC"),
                        "width": attrs.get("width", 1),
                    }
                    if attrs.get("dashes"):
                        edge_kwargs["dashes"] = True
                    if attrs.get("smooth"):
                        edge_kwargs["smooth"] = attrs["smooth"]
                    net.add_edge(src, dst, **{k: v for k, v in edge_kwargs.items() if k not in ("source", "to")})
                
                # ── Physics: wider spacing for data-flow readability ──
                net.set_options("""
                var options = {
                  "nodes": {
                    "borderWidth": 2,
                    "borderWidthSelected": 3,
                    "shadow": { "enabled": true, "size": 5, "x": 2, "y": 2 }
                  },
                  "edges": {
                    "smooth": { "type": "continuous", "roundness": 0.12 },
                    "arrows": { "to": { "enabled": true, "scaleFactor": 0.5 } },
                    "selectionWidth": 2
                  },
                  "physics": {
                    "forceAtlas2Based": {
                      "gravitationalConstant": -160,
                      "centralGravity": 0.005,
                      "springLength": 240,
                      "springConstant": 0.03,
                      "avoidOverlap": 0.85
                    },
                    "minVelocity": 0.75,
                    "solver": "forceAtlas2Based",
                    "stabilization": { "iterations": 200 }
                  },
                  "interaction": {
                    "hover": true,
                    "tooltipDelay": 100,
                    "navigationButtons": true,
                    "keyboard": { "enabled": true }
                  }
                }
                """)
                
                # Generate and render HTML
                with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp_file:
                    net.save_graph(tmp_file.name)
                    html_file_path = tmp_file.name
                    
                with open(html_file_path, 'r', encoding='utf-8') as f:
                    html_data = f.read()
                    
                import streamlit.components.v1 as components
                components.html(html_data, height=600, scrolling=False)
                
                # Cleanup
                try:
                    os.remove(html_file_path)
                except:
                    pass
                
                # ── Color-coded Legend ─────────────────────────────
                def _legend_pill(color, label, count):
                    return (
                        f'<span style="display:inline-flex;align-items:center;gap:5px;margin-right:18px;">'
                        f'<span style="width:12px;height:12px;border-radius:50%;background:{color};display:inline-block;"></span>'
                        f'<span style="font-size:0.78rem;color:#475569;font-weight:600;font-family:Outfit,sans-serif;">{label} ({count})</span>'
                        f'</span>'
                    )
                
                group_counts = {}
                for n in G.nodes:
                    grp = G.nodes[n].get("nodeType", "")
                    group_counts[grp] = group_counts.get(grp, 0) + 1
                
                legend_html = ""
                legend_html += _legend_pill(CLR_DOMAIN, "Domains", group_counts.get("Domain", 0))
                legend_html += _legend_pill(CLR_DEMO, "Demos", group_counts.get("Demo", 0))
                if show_inputs:
                    legend_html += _legend_pill(CLR_INPUT, "Inputs", group_counts.get("Input", 0))
                if show_outputs:
                    legend_html += _legend_pill(CLR_OUTPUT, "Outputs", group_counts.get("Output", 0))
                if show_kpis:
                    legend_html += _legend_pill(CLR_KPI, "KPIs", group_counts.get("KPI", 0))
                if show_agents:
                    legend_html += _legend_pill(CLR_AGENT, "Agents", group_counts.get("Agent", 0))
                
                st.markdown(
                    f'<div style="display:flex;justify-content:center;flex-wrap:wrap;padding:6px 0;">{legend_html}</div>',
                    unsafe_allow_html=True
                )
                
                # ── Stats Row ─────────────────────────────────────
                sc = st.columns(5)
                sc[0].metric("Total Nodes", len(G.nodes))
                sc[1].metric("Edges", len(G.edges))
                sc[2].metric("Demos", group_counts.get("Demo", 0))
                sc[3].metric("Inputs", group_counts.get("Input", 0))
                sc[4].metric("KPIs", group_counts.get("KPI", 0))
                
        except ImportError:
            st.error("GraphDB visualization requires `pyvis` and `networkx`. Install via `pip install pyvis networkx`.")

