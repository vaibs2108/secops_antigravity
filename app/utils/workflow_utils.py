import streamlit as st
import pandas as pd
import json
import base64
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
import plotly.graph_objects as go

class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder for datetime objects"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)

class RemediationWorkflow:
    """Enhanced remediation workflow with human-in-the-loop approval"""
    
    @staticmethod
    def generate_remediation_id(phase: str) -> str:
        """Generate unique remediation ID"""
        if 'remediation_workflows' not in st.session_state:
            st.session_state.remediation_workflows = {}
        
        phase_key = phase.lower()
        if phase_key not in st.session_state.remediation_workflows:
            st.session_state.remediation_workflows[phase_key] = []
            
        count = len(st.session_state.remediation_workflows[phase_key])
        return f"REM-{phase[:3].upper()}-{datetime.now().strftime('%Y%m%d')}-{count+1:04d}"
    
    @staticmethod
    def create_remediation_ticket(
        phase: str,
        title: str,
        description: str,
        priority: str,
        category: str,
        ai_recommendation: str,
        requires_approval: bool = True,
        approver_role: str = "lead"
    ) -> Dict:
        """Create a new remediation ticket"""
        # Ensure state is initialized
        if 'remediation_workflows' not in st.session_state:
            st.session_state.remediation_workflows = {}
        if 'approval_queue' not in st.session_state:
            st.session_state.approval_queue = []
        if 'workflow_audit_log' not in st.session_state:
            st.session_state.workflow_audit_log = []
            
        phase_key = phase.lower()
        if phase_key not in st.session_state.remediation_workflows:
            st.session_state.remediation_workflows[phase_key] = []

        ticket = {
            'id': RemediationWorkflow.generate_remediation_id(phase),
            'phase': phase,
            'title': title,
            'description': description,
            'ai_recommendation': ai_recommendation,
            'category': category,
            'priority': priority,
            'status': 'draft',
            'created_by': 'AI Agent',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'requires_approval': requires_approval,
            'approver_role': approver_role,
            'current_approver': None,
            'approval_status': 'pending' if requires_approval else 'not_required',
            'approval_history': [],
            'assigned_to': None,
            'due_date': (datetime.now() + timedelta(days=7)).isoformat(),
            'sla': '7 days',
            'implementation_steps': [],
            'verification_required': True,
            'verified': False,
            'workflow_stage': 'identified',
            'notes': [],
            'attachments': []
        }
        
        # Add to workflow
        st.session_state.remediation_workflows[phase_key].append(ticket)
        
        # If requires approval, add to approval queue
        if requires_approval:
            approval_item = {
                'ticket_id': ticket['id'],
                'phase': phase,
                'title': title,
                'priority': priority,
                'submitted_at': datetime.now().isoformat(),
                'submitted_by': 'AI Agent',
                'approver_role': approver_role,
                'status': 'pending',
                'escalation_level': 0
            }
            st.session_state.approval_queue.append(approval_item)
        
        # Log audit
        RemediationWorkflow.log_audit(
            action='ticket_created',
            ticket_id=ticket['id'],
            phase=phase,
            details=f"Remediation ticket created: {title}"
        )
        
        return ticket
    
    @staticmethod
    def log_audit(action: str, ticket_id: str, phase: str, details: str, user: str = "System"):
        """Log workflow audit trail"""
        if 'workflow_audit_log' not in st.session_state:
            st.session_state.workflow_audit_log = []
            
        audit_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'ticket_id': ticket_id,
            'phase': phase,
            'user': user,
            'details': details
        }
        st.session_state.workflow_audit_log.append(audit_entry)
    
    @staticmethod
    def get_approval_queue(phase: str = None, status: str = 'pending'):
        """Get approval queue items"""
        if 'approval_queue' not in st.session_state:
            st.session_state.approval_queue = []
            
        queue = st.session_state.approval_queue
        if phase:
            queue = [item for item in queue if item['phase'].lower() == phase.lower()]
        if status:
            queue = [item for item in queue if item['status'] == status]
        return queue
    
    @staticmethod
    def approve_ticket(ticket_id: str, approver: str, justification: str, comments: str = ""):
        """Approve a remediation ticket"""
        if 'remediation_workflows' not in st.session_state:
            return False
            
        # Find ticket in workflows
        ticket = None
        phase = None
        for phase_key, tickets in st.session_state.remediation_workflows.items():
            for t in tickets:
                if t['id'] == ticket_id:
                    ticket = t
                    phase = phase_key
                    break
            if ticket:
                break
        
        if not ticket:
            return False
        
        # Update ticket
        ticket['approval_status'] = 'approved'
        ticket['current_approver'] = approver
        ticket['status'] = 'approved'
        ticket['workflow_stage'] = 'approved'
        ticket['updated_at'] = datetime.now().isoformat()
        
        # Add approval history
        approval_record = {
            'action': 'approved',
            'approver': approver,
            'justification': justification,
            'comments': comments,
            'timestamp': datetime.now().isoformat()
        }
        ticket['approval_history'].append(approval_record)
        
        # Update approval queue
        for item in st.session_state.approval_queue:
            if item['ticket_id'] == ticket_id:
                item['status'] = 'approved'
                item['approved_at'] = datetime.now().isoformat()
                item['approved_by'] = approver
                break
        
        # Log audit
        RemediationWorkflow.log_audit(
            action='ticket_approved',
            ticket_id=ticket_id,
            phase=phase,
            details=f"Ticket approved by {approver}. Justification: {justification}",
            user=approver
        )
        
        return True
    
    @staticmethod
    def reject_ticket(ticket_id: str, rejecter: str, reason: str, comments: str = ""):
        """Reject a remediation ticket"""
        if 'remediation_workflows' not in st.session_state:
            return False
            
        # Find ticket in workflows
        ticket = None
        phase = None
        for phase_key, tickets in st.session_state.remediation_workflows.items():
            for t in tickets:
                if t['id'] == ticket_id:
                    ticket = t
                    phase = phase_key
                    break
            if ticket:
                break
        
        if not ticket:
            return False
        
        # Update ticket
        ticket['approval_status'] = 'rejected'
        ticket['current_approver'] = rejecter
        ticket['status'] = 'rejected'
        ticket['workflow_stage'] = 'rejected'
        ticket['updated_at'] = datetime.now().isoformat()
        
        # Add rejection history
        rejection_record = {
            'action': 'rejected',
            'rejecter': rejecter,
            'reason': reason,
            'comments': comments,
            'timestamp': datetime.now().isoformat()
        }
        ticket['approval_history'].append(rejection_record)
        
        # Update approval queue
        for item in st.session_state.approval_queue:
            if item['ticket_id'] == ticket_id:
                item['status'] = 'rejected'
                item['rejected_at'] = datetime.now().isoformat()
                item['rejected_by'] = rejecter
                break
        
        # Log audit
        RemediationWorkflow.log_audit(
            action='ticket_rejected',
            ticket_id=ticket_id,
            phase=phase,
            details=f"Ticket rejected by {rejecter}. Reason: {reason}",
            user=rejecter
        )
        
        return True
    
    @staticmethod
    def get_workflow_metrics(phase: str = None):
        """Get workflow performance metrics"""
        if 'remediation_workflows' not in st.session_state:
            return {
                'total_tickets': 0,
                'pending_approval': 0,
                'approved': 0,
                'rejected': 0,
                'in_progress': 0,
                'completed': 0,
                'avg_approval_time_hours': 0,
                'sla_compliance_rate': 0
            }

        if phase:
            tickets = st.session_state.remediation_workflows.get(phase.lower(), [])
        else:
            tickets = []
            for phase_tickets in st.session_state.remediation_workflows.values():
                tickets.extend(phase_tickets)
        
        if not tickets:
            return {
                'total_tickets': 0,
                'pending_approval': 0,
                'approved': 0,
                'rejected': 0,
                'in_progress': 0,
                'completed': 0,
                'avg_approval_time_hours': 0,
                'sla_compliance_rate': 0
            }
        
        # Calculate metrics
        total = len(tickets)
        pending = len([t for t in tickets if t.get('approval_status') == 'pending'])
        approved = len([t for t in tickets if t.get('approval_status') == 'approved'])
        rejected = len([t for t in tickets if t.get('approval_status') == 'rejected'])
        in_progress = len([t for t in tickets if t.get('status') == 'in_progress'])
        completed = len([t for t in tickets if t.get('status') == 'completed'])
        
        # Calculate average approval time (simulated)
        avg_approval_time = random.randint(4, 48)
        
        # Calculate SLA compliance (simulated)
        sla_compliance = random.randint(70, 95)
        
        return {
            'total_tickets': total,
            'pending_approval': pending,
            'approved': approved,
            'rejected': rejected,
            'in_progress': in_progress,
            'completed': completed,
            'avg_approval_time_hours': avg_approval_time,
            'sla_compliance_rate': sla_compliance
        }
    
    @staticmethod
    def render_remediation_tab(phase: str):
        """Render the remediation workflow tab for a phase"""
        st.markdown(f"### 🔧 {phase} Remediation Workflow")
        st.info("""
        **Human-in-the-Loop Remediation Process:**
        1. **AI Identifies Issue** → 2. **Generate Remediation Ticket** → 3. **Human Approval Required** → 
        4. **Approval/Rejection** → 5. **Implementation** → 6. **Verification** → 7. **Closure**
        """)
        
        # Create tabs for workflow components
        tab1, tab2, tab3, tab4 = st.tabs([
            "🎯 Generate Ticket", 
            "📋 Approval Queue", 
            "🚀 Implementation", 
            "📊 Workflow Analytics"
        ])
        
        with tab1:
            RemediationWorkflow.render_ticket_generation(phase)
        
        with tab2:
            RemediationWorkflow.render_approval_queue(phase)
        
        with tab3:
            RemediationWorkflow.render_implementation(phase)
        
        with tab4:
            RemediationWorkflow.render_workflow_analytics(phase)
    
    @staticmethod
    def render_ticket_generation(phase: str):
        """Render ticket generation interface"""
        st.markdown("#### 📝 Generate Remediation Ticket")
        
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input(
                "Ticket Title",
                value=f"{phase} Issue - {datetime.now().strftime('%Y-%m-%d')}",
                key=f"{phase}_ticket_title"
            )
            
            category = st.selectbox(
                "Category",
                ["Policy", "Configuration", "Access Control", "Vulnerability", "Compliance", "Other"],
                key=f"{phase}_ticket_category"
            )
            
            priority = st.select_slider(
                "Priority",
                options=["Low", "Medium", "High", "Critical"],
                value="Medium",
                key=f"{phase}_ticket_priority"
            )
            
            description = st.text_area(
                "Issue Description",
                value=f"AI-identified issue in {phase} phase requiring remediation.",
                height=100,
                key=f"{phase}_ticket_desc"
            )
        
        with col2:
            ai_recommendation = st.text_area(
                "AI Recommendation",
                value=f"AI suggests implementing security controls for {phase} phase issue.",
                height=100,
                key=f"{phase}_ai_rec"
            )
            
            requires_approval = st.checkbox(
                "Requires Approval", 
                value=True,
                key=f"{phase}_req_approval"
            )
            
            approver_role = "lead"
            if requires_approval:
                approver_role = st.selectbox(
                    "Approver Role",
                    ["analyst", "lead", "manager", "ciso"],
                    index=1,
                    key=f"{phase}_approver_role"
                )
            
            sla_days = st.slider(
                "SLA (Days)",
                1, 30, 7,
                key=f"{phase}_sla_days"
            )
        
        if st.button("🎫 Create Remediation Ticket", key=f"{phase}_create_ticket", use_container_width=True):
            ticket = RemediationWorkflow.create_remediation_ticket(
                phase=phase,
                title=title,
                description=description,
                priority=priority,
                category=category,
                ai_recommendation=ai_recommendation,
                requires_approval=requires_approval,
                approver_role=approver_role if requires_approval else None
            )
            
            st.success(f"✅ Ticket created: **{ticket['id']}**")
            st.json(ticket, expanded=False)
    
    @staticmethod
    def render_approval_queue(phase: str):
        """Render approval queue interface"""
        st.markdown("#### 📋 Approval Queue")
        
        # Get pending approvals for this phase
        pending_approvals = RemediationWorkflow.get_approval_queue(phase, 'pending')
        
        if not pending_approvals:
            st.info("No pending approvals for this phase.")
        else:
            for approval in pending_approvals:
                with st.expander(f"🔸 {approval['ticket_id']}: {approval['title']} ({approval['priority']})", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Phase:** {approval['phase']}")
                        st.markdown(f"**Submitted:** {approval['submitted_at']}")
                        st.markdown(f"**Requires:** {approval['approver_role']} approval")
                    
                    with col2:
                        justification = st.text_area(
                            "Approval Justification (Required)",
                            value="",
                            placeholder="Explain why this should be approved...",
                            key=f"justify_{approval['ticket_id']}"
                        )
                        
                        comments = st.text_area(
                            "Additional Comments",
                            value="",
                            placeholder="Any additional comments...",
                            key=f"comments_{approval['ticket_id']}"
                        )
                    
                    col_approve, col_reject, col_view = st.columns(3)
                    
                    with col_approve:
                        if st.button("✅ Approve", key=f"approve_{approval['ticket_id']}", use_container_width=True):
                            if justification.strip():
                                RemediationWorkflow.approve_ticket(
                                    ticket_id=approval['ticket_id'],
                                    approver="Current User",
                                    justification=justification,
                                    comments=comments
                                )
                                st.success(f"Ticket {approval['ticket_id']} approved!")
                                st.rerun()
                            else:
                                st.error("Justification is required for approval.")
                    
                    with col_reject:
                        if st.button("❌ Reject", key=f"reject_{approval['ticket_id']}", use_container_width=True):
                            if justification.strip():
                                RemediationWorkflow.reject_ticket(
                                    ticket_id=approval['ticket_id'],
                                    rejecter="Current User",
                                    reason=justification,
                                    comments=comments
                                )
                                st.warning(f"Ticket {approval['ticket_id']} rejected!")
                                st.rerun()
                            else:
                                st.error("Reason is required for rejection.")
                    
                    with col_view:
                        if st.button("👁️ View Details", key=f"view_{approval['ticket_id']}", use_container_width=True):
                            # Find and display ticket details
                            for phase_key, tickets in st.session_state.remediation_workflows.items():
                                for ticket in tickets:
                                    if ticket['id'] == approval['ticket_id']:
                                        st.json(ticket, expanded=False)
                                        break
        
        # Show recent approvals
        st.markdown("#### ✅ Recently Approved/Rejected")
        recent_actions = []
        if 'approval_queue' in st.session_state:
            for item in st.session_state.approval_queue:
                if item['phase'].lower() == phase.lower() and item['status'] in ['approved', 'rejected']:
                    recent_actions.append(item)
        
        if recent_actions:
            for action in recent_actions[-5:]:  # Last 5 actions
                status_icon = "✅" if action['status'] == 'approved' else "❌"
                st.caption(f"{status_icon} **{action['ticket_id']}**: {action['status'].title()} by {action.get('approved_by', action.get('rejected_by', 'Unknown'))}")
    
    @staticmethod
    def render_implementation(phase: str):
        """Render implementation tracking interface"""
        st.markdown("#### 🚀 Implementation Tracking")
        
        # Get approved tickets for this phase
        phase_tickets = st.session_state.remediation_workflows.get(phase.lower(), [])
        approved_tickets = [t for t in phase_tickets if t.get('approval_status') == 'approved']
        
        if not approved_tickets:
            st.info("No approved tickets ready for implementation.")
            return
        
        for ticket in approved_tickets:
            with st.expander(f"🔧 {ticket['id']}: {ticket['title']}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Status:** {ticket.get('status', 'draft')}")
                    st.markdown(f"**Priority:** {ticket['priority']}")
                    st.markdown(f"**Due Date:** {ticket['due_date']}")
                    st.markdown(f"**SLA:** {ticket['sla']}")
                
                with col2:
                    current_status = st.selectbox(
                        "Update Status",
                        ["draft", "approved", "in_progress", "completed", "verified", "closed"],
                        index=["draft", "approved", "in_progress", "completed", "verified", "closed"].index(
                            ticket.get('status', 'draft')
                        ),
                        key=f"status_{ticket['id']}"
                    )
                    
                    assigned_to = st.selectbox(
                        "Assign To",
                        ["Unassigned", "SOC Team", "Network Team", "Security Team", "Compliance Team"],
                        key=f"assign_{ticket['id']}"
                    )
                
                # Implementation steps
                st.markdown("##### 📋 Implementation Steps")
                steps = ticket.get('implementation_steps', [])
                
                for i, step in enumerate(steps):
                    col_step, col_status = st.columns([3, 1])
                    with col_step:
                        st.text_input(f"Step {i+1}", value=step['description'], key=f"step_{ticket['id']}_{i}")
                    with col_status:
                        st.selectbox("Status", ["pending", "in_progress", "completed"], 
                                    index=["pending", "in_progress", "completed"].index(step['status']),
                                    key=f"step_status_{ticket['id']}_{i}")
                
                if st.button("➕ Add Implementation Step", key=f"add_step_{ticket['id']}"):
                    steps.append({
                        'description': "New implementation step",
                        'status': 'pending',
                        'added_at': datetime.now().isoformat()
                    })
                
                st.markdown("##### ✅ Verification")
                verified = st.checkbox(
                    "Remediation Verified",
                    value=ticket.get('verified', False),
                    key=f"verify_{ticket['id']}"
                )
                
                verification_notes = st.text_area(
                    "Verification Notes",
                    value="",
                    placeholder="Notes on how verification was performed...",
                    key=f"verify_notes_{ticket['id']}"
                )
                
                if st.button("💾 Update Ticket", key=f"update_{ticket['id']}", use_container_width=True):
                    ticket['status'] = current_status
                    ticket['assigned_to'] = assigned_to
                    ticket['verified'] = verified
                    ticket['updated_at'] = datetime.now().isoformat()
                    
                    if verified and current_status == 'completed':
                        ticket['workflow_stage'] = 'verified'
                    
                    RemediationWorkflow.log_audit(
                        action='ticket_updated',
                        ticket_id=ticket['id'],
                        phase=phase,
                        details=f"Ticket updated: Status={current_status}, Assigned={assigned_to}, Verified={verified}",
                        user="Current User"
                    )
                    
                    st.success(f"Ticket {ticket['id']} updated!")
    
    @staticmethod
    def render_workflow_analytics(phase: str):
        """Render workflow analytics dashboard"""
        st.markdown("#### 📊 Workflow Performance Analytics")
        
        metrics = RemediationWorkflow.get_workflow_metrics(phase)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Tickets", metrics['total_tickets'])
        with col2:
            st.metric("Pending Approval", metrics['pending_approval'])
        with col3:
            st.metric("Approved", metrics['approved'])
        with col4:
            st.metric("Completed", metrics['completed'])
        
        col5, col6 = st.columns(2)
        with col5:
            st.metric("Avg Approval Time", f"{metrics['avg_approval_time_hours']}h")
        with col6:
            st.metric("SLA Compliance", f"{metrics['sla_compliance_rate']}%")
        
        st.markdown("##### 📈 Workflow Stages")
        stages = ['identified', 'draft', 'pending_approval', 'approved', 'in_progress', 'completed', 'verified']
        stage_counts = {stage: 0 for stage in stages}
        
        phase_tickets = st.session_state.remediation_workflows.get(phase.lower(), [])
        for ticket in phase_tickets:
            stage = ticket.get('workflow_stage', 'identified')
            if stage in stage_counts:
                stage_counts[stage] += 1
        
        fig = go.Figure(data=[go.Bar(
            x=[s.replace('_', ' ').title() for s in list(stage_counts.keys())],
            y=list(stage_counts.values()),
            marker_color='#1E3A8A'
        )])
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Workflow Stage",
            yaxis_title="Number of Tickets",
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("##### 📝 Recent Audit Trail")
        phase_audits = [a for a in st.session_state.get('workflow_audit_log', []) if a['phase'].lower() == phase.lower()]
        
        if phase_audits:
            recent_audits = phase_audits[-10:]
            for audit in recent_audits:
                st.caption(f"**{audit['timestamp'][11:16]}** - {audit['action']} by {audit['user']}: {audit['details'][:80]}...")
        else:
            st.info("No audit entries for this phase yet.")
        
        st.markdown("##### 📤 Export Workflow Data")
        col_exp1, col_exp2 = st.columns(2)
        
        with col_exp1:
            if st.button("📊 Export Tickets", key=f"export_tickets_{phase}", use_container_width=True):
                tickets_data = {
                    'phase': phase,
                    'tickets': phase_tickets,
                    'exported_at': datetime.now().isoformat()
                }
                json_str = json.dumps(tickets_data, indent=2, cls=DateTimeEncoder)
                b64 = base64.b64encode(json_str.encode()).decode()
                href = f'<a href="data:file/json;base64,{b64}" download="{phase}_remediation_tickets.json">Download Tickets JSON</a>'
                st.markdown(href, unsafe_allow_html=True)
        
        with col_exp2:
            if st.button("📋 Export Audit Trail", key=f"export_audit_{phase}", use_container_width=True):
                audit_data = {
                    'phase': phase,
                    'audit_log': phase_audits,
                    'exported_at': datetime.now().isoformat()
                }
                json_str = json.dumps(audit_data, indent=2, cls=DateTimeEncoder)
                b64 = base64.b64encode(json_str.encode()).decode()
                href = f'<a href="data:file/json;base64,{b64}" download="{phase}_audit_trail.json">Download Audit JSON</a>'
                st.markdown(href, unsafe_allow_html=True)
