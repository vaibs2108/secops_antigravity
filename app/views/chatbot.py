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
        
        # Initialize chat history
        if "copilot_messages" not in st.session_state:
            st.session_state.copilot_messages = [
                {
                    "role": "assistant", 
                    "content": "Hello! I am your SecOps Copilot. I have analyzed the active Known Error Database and current Incident Tickets. How can I assist with your investigation today?"
                }
            ]

        # Display chat messages
        for msg in st.session_state.copilot_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # React to user input
        if prompt := st.chat_input("E.g., A CrowdStrike sensor went offline. How do I fix it based on the KEDB?"):
            
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
        st.markdown("Interactive visualization of relationships between Security Domains, Capabilities, and AI Agents.")
        
        try:
            from pyvis.network import Network
            import networkx as nx
            import tempfile
            from app.views.shared import load_demo_requirements
            import re
            
            records = load_demo_requirements()
            
            # ── Interactive Filters ───────────────────────────────
            filter_cols = st.columns([2, 1, 1, 1, 1])
            
            # Domain filter
            all_domains = sorted(list(set(str(r.get('Category', 'Unknown')) for r in records)))
            with filter_cols[0]:
                selected_domain = st.selectbox("🔍 Filter by Domain", ["All Domains"] + all_domains, key="kg_domain_filter")
            
            with filter_cols[1]:
                show_domains = st.checkbox("Domains", value=True, key="kg_show_domains")
            with filter_cols[2]:
                show_demos = st.checkbox("Capabilities", value=True, key="kg_show_demos")
            with filter_cols[3]:
                show_agents = st.checkbox("Agents", value=True, key="kg_show_agents")
            with filter_cols[4]:
                show_activities = st.checkbox("Activities", value=False, key="kg_show_activities")
            
            # ── Build Filtered Graph ──────────────────────────────
            G = nx.DiGraph()
            
            # Color scheme
            DOMAIN_COLOR = "#1E3A8A"
            DEMO_COLOR = "#3B82F6"
            AGENT_COLOR = "#10B981"
            ACTIVITY_COLOR = "#F59E0B"
            
            # Track agent-to-demo mappings for rich tooltips
            agent_demos = {}
            agent_domains = {}
            
            for r in records:
                domain = str(r.get('Category', 'Unknown Domain'))
                demo = str(r.get('Demo Name', 'Unknown'))
                agents_str = str(r.get('Agents Involved', 'SecOps Copilot'))
                goal = str(r.get('Goal of Demo', '')).strip()
                kpis = str(r.get('KPIs and Calculations', '')).strip()
                tools = str(r.get('Relevant Vendor Tools', '')).strip()
                
                # Apply domain filter
                if selected_domain != "All Domains" and domain != selected_domain:
                    continue
                
                # ── Domain node ──
                if show_domains and not G.has_node(domain):
                    G.add_node(domain, group="Domain",
                               title=f"<b>🏛️ Security Domain</b><br>{domain}",
                               size=40, color=DOMAIN_COLOR,
                               font={"size": 16, "color": "#FFFFFF", "face": "Outfit, sans-serif"},
                               shape="dot")
                
                # ── Demo/Capability node ──
                if show_demos:
                    demo_short = demo if len(demo) <= 45 else demo[:42] + "..."
                    demo_tooltip = (
                        f"<b>⚡ Capability</b><br><b>{demo}</b>"
                        f"<hr style='margin:4px 0;border-color:#E2E8F0;'>"
                        f"<b>Goal:</b> {goal}<br>"
                        f"<b>KPIs:</b> {kpis}<br>"
                        f"<b>Tools:</b> {tools}"
                    )
                    if not G.has_node(demo):
                        G.add_node(demo, group="Capability",
                                   title=demo_tooltip, label=demo_short,
                                   size=22, color=DEMO_COLOR,
                                   font={"size": 11, "color": "#1E293B", "face": "Outfit, sans-serif"},
                                   shape="dot")
                    
                    # Domain → Demo edge
                    if show_domains and not G.has_edge(domain, demo):
                        G.add_edge(domain, demo, color={"color": "#93C5FD", "opacity": 0.7},
                                   width=2, arrows="to", smooth={"type": "curvedCW", "roundness": 0.15})
                
                # ── Agent nodes ──
                agent_names = [a.strip().replace('*', '').strip() for a in agents_str.split(',') if a.strip()]
                for agent in agent_names:
                    if not agent or agent.lower() == "none" or "No dedicated" in agent:
                        continue
                    
                    # Track agent capabilities
                    if agent not in agent_demos:
                        agent_demos[agent] = []
                        agent_domains[agent] = set()
                    agent_demos[agent].append(demo)
                    agent_domains[agent].add(domain)
                    
                    if show_agents:
                        # Build rich tooltip for agent
                        linked_demos = agent_demos[agent]
                        linked_doms = agent_domains[agent]
                        agent_tooltip = (
                            f"<b>🤖 AI Agent</b><br><b>{agent}</b>"
                            f"<hr style='margin:4px 0;border-color:#E2E8F0;'>"
                            f"<b>Domains:</b> {', '.join(linked_doms)}<br>"
                            f"<b>Capabilities ({len(linked_demos)}):</b><br>"
                            + "<br>".join(f"• {d[:50]}" for d in linked_demos[:5])
                        )
                        
                        if not G.has_node(agent):
                            G.add_node(agent, group="Agent",
                                       title=agent_tooltip,
                                       size=28, color=AGENT_COLOR,
                                       font={"size": 12, "color": "#1E293B", "face": "Outfit, sans-serif"},
                                       shape="dot")
                        else:
                            # Update tooltip with latest info
                            G.nodes[agent]['title'] = agent_tooltip
                        
                        # Demo → Agent edge
                        if show_demos and not G.has_edge(demo, agent):
                            G.add_edge(demo, agent, color={"color": "#A7F3D0", "opacity": 0.6},
                                       width=1.5, arrows="to", smooth={"type": "curvedCCW", "roundness": 0.12})
                        
                        # Domain → Agent edge (if demos hidden, connect directly)
                        if not show_demos and show_domains and not G.has_edge(domain, agent):
                            G.add_edge(domain, agent, color={"color": "#86EFAC", "opacity": 0.7},
                                       width=2, arrows="to")
                
                # ── Activity node (optional) ──
                if show_activities and goal:
                    activity = goal.split(',')[0].strip() if ',' in goal else goal
                    if len(activity) > 35:
                        activity = activity[:32] + "..."
                    activity_node = "🎯 " + activity
                    
                    if not G.has_node(activity_node):
                        G.add_node(activity_node, group="Activity",
                                   title=f"<b>🎯 Objective</b><br>{goal}",
                                   size=14, color=ACTIVITY_COLOR,
                                   font={"size": 9, "color": "#92400E", "face": "Outfit, sans-serif"},
                                   shape="dot")
                    
                    # Connect to demo
                    if show_demos and not G.has_edge(demo, activity_node):
                        G.add_edge(demo, activity_node, color={"color": "#FCD34D", "opacity": 0.5},
                                   width=1, arrows="to", dashes=True)
            
            if len(G.nodes) == 0:
                st.info("No nodes to display. Adjust your filters.")
            else:
                # ── Create PyVis Network ──────────────────────────
                net = Network(height="550px", width="100%", bgcolor="#FFFFFF",
                              font_color="#1E293B", directed=True)
                net.from_nx(G)
                
                # ── Optimized Physics & Layout ────────────────────
                net.set_options("""
                var options = {
                  "nodes": {
                    "borderWidth": 2,
                    "borderWidthSelected": 3,
                    "shadow": { "enabled": true, "size": 6, "x": 2, "y": 2 }
                  },
                  "edges": {
                    "smooth": { "type": "continuous", "roundness": 0.15 },
                    "arrows": { "to": { "enabled": true, "scaleFactor": 0.6 } },
                    "selectionWidth": 2
                  },
                  "physics": {
                    "forceAtlas2Based": {
                      "gravitationalConstant": -120,
                      "centralGravity": 0.008,
                      "springLength": 200,
                      "springConstant": 0.04,
                      "avoidOverlap": 0.8
                    },
                    "minVelocity": 0.75,
                    "solver": "forceAtlas2Based",
                    "stabilization": { "iterations": 150 }
                  },
                  "interaction": {
                    "hover": true,
                    "tooltipDelay": 100,
                    "navigationButtons": true,
                    "keyboard": { "enabled": true }
                  }
                }
                """)
                
                # Generate and render
                with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp_file:
                    net.save_graph(tmp_file.name)
                    html_file_path = tmp_file.name
                    
                with open(html_file_path, 'r', encoding='utf-8') as f:
                    html_data = f.read()
                    
                import streamlit.components.v1 as components
                components.html(html_data, height=570, scrolling=False)
                
                # Cleanup
                try:
                    os.remove(html_file_path)
                except:
                    pass
                
                # ── Color Legend ───────────────────────────────────
                legend_items = []
                if show_domains:
                    legend_items.append(f'<span style="display:inline-flex;align-items:center;gap:5px;margin-right:20px;"><span style="width:14px;height:14px;border-radius:50%;background:{DOMAIN_COLOR};display:inline-block;"></span><span style="font-size:0.8rem;color:#475569;font-weight:600;">Domains ({len([n for n in G.nodes if G.nodes[n].get("group")=="Domain"])})</span></span>')
                if show_demos:
                    legend_items.append(f'<span style="display:inline-flex;align-items:center;gap:5px;margin-right:20px;"><span style="width:14px;height:14px;border-radius:50%;background:{DEMO_COLOR};display:inline-block;"></span><span style="font-size:0.8rem;color:#475569;font-weight:600;">Capabilities ({len([n for n in G.nodes if G.nodes[n].get("group")=="Capability"])})</span></span>')
                if show_agents:
                    legend_items.append(f'<span style="display:inline-flex;align-items:center;gap:5px;margin-right:20px;"><span style="width:14px;height:14px;border-radius:50%;background:{AGENT_COLOR};display:inline-block;"></span><span style="font-size:0.8rem;color:#475569;font-weight:600;">Agents ({len([n for n in G.nodes if G.nodes[n].get("group")=="Agent"])})</span></span>')
                if show_activities:
                    legend_items.append(f'<span style="display:inline-flex;align-items:center;gap:5px;margin-right:20px;"><span style="width:14px;height:14px;border-radius:50%;background:{ACTIVITY_COLOR};display:inline-block;"></span><span style="font-size:0.8rem;color:#475569;font-weight:600;">Activities ({len([n for n in G.nodes if G.nodes[n].get("group")=="Activity"])})</span></span>')
                
                st.markdown(
                    f'<div style="display:flex;justify-content:center;flex-wrap:wrap;padding:8px 0;">{"".join(legend_items)}</div>',
                    unsafe_allow_html=True
                )
                
                # ── Stats Row ─────────────────────────────────────
                stats_cols = st.columns(4)
                stats_cols[0].metric("Nodes", len(G.nodes))
                stats_cols[1].metric("Edges", len(G.edges))
                stats_cols[2].metric("Domains", len([n for n in G.nodes if G.nodes[n].get("group") == "Domain"]))
                stats_cols[3].metric("Agents", len([n for n in G.nodes if G.nodes[n].get("group") == "Agent"]))
                
        except ImportError:
            st.error("GraphDB visualization requires `pyvis` and `networkx`. Install via `pip install pyvis networkx`.")

