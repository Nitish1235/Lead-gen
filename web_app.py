"""
Modern Web UI for B2B Lead Discovery System
Built with Streamlit for a clean, intuitive interface
"""
import streamlit as st
import time
import threading
from datetime import datetime
from typing import List, Optional
import pandas as pd
from queue import Queue, Empty
from main import LeadDiscoveryApp
from countries import list_all_countries, search_countries, get_country_config
import config

# Page configuration
st.set_page_config(
    page_title="B2B Lead Discovery",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .status-running {
        color: #28a745;
        font-weight: 600;
    }
    .status-stopped {
        color: #6c757d;
        font-weight: 600;
    }
    .lead-score-high {
        background-color: #d4edda;
        color: #155724;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-weight: 600;
    }
    .lead-score-medium {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-weight: 600;
    }
    .lead-score-low {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'leads_found' not in st.session_state:
    st.session_state.leads_found = []
if 'run_history' not in st.session_state:
    st.session_state.run_history = []
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'current_run_id' not in st.session_state:
    st.session_state.current_run_id = None
if 'discovery_thread' not in st.session_state:
    st.session_state.discovery_thread = None
if 'lead_queue' not in st.session_state:
    st.session_state.lead_queue = Queue()

# Thread-safe lead queue processor
def process_lead_queue():
    """Process leads from the thread-safe queue and add to session state"""
    try:
        while True:
            try:
                lead = st.session_state.lead_queue.get_nowait()
                st.session_state.leads_found.append(lead)
            except Empty:
                break
    except Exception as e:
        # Silently handle any errors to avoid disrupting the UI
        pass

# Create a closure for the callback that captures the queue reference
def create_lead_callback(queue):
    """Create a thread-safe callback function that uses the queue"""
    def on_lead_found(lead):
        """Callback when a lead is found and saved - thread-safe version"""
        try:
            queue.put(lead)
        except Exception:
            # Silently fail if queue operations fail (thread safety)
            pass
    return on_lead_found

# Initialize app with callback (using queue from session state)
if 'app' not in st.session_state:
    lead_callback = create_lead_callback(st.session_state.lead_queue)
    st.session_state.app = LeadDiscoveryApp(lead_callback=lead_callback)

def get_score_class(score: int) -> str:
    """Get CSS class for score styling"""
    if score >= 70:
        return "lead-score-high"
    elif score >= 40:
        return "lead-score-medium"
    else:
        return "lead-score-low"

def run_discovery(app_instance, country: str, city: str, categories: Optional[List[str]]):
    """Run discovery in a separate thread - fully thread-safe version (no Streamlit access)"""
    try:
        # Ensure app is not in a stuck running state
        if app_instance.is_running:
            app_instance.is_running = False
            app_instance.should_stop = False
        
        # Run discovery (this will call callbacks from background thread)
        # The callback puts leads in the queue, which is thread-safe
        app_instance.start(country, city, categories)
    except Exception as e:
        # Error handling - ensure state is reset even on error
        app_instance.is_running = False
        app_instance.should_stop = False
        print(f"Error during discovery: {e}")

# Main Header
st.markdown('<h1 class="main-header">🔍 B2B Lead Discovery System</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Discover high-quality B2B leads worldwide for software development, automation, and AI services</p>', unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Country selection
    countries = list_all_countries()
    selected_country = st.selectbox(
        "Select Country",
        countries,
        index=0 if "United States" in countries else 0
    )
    
    # City input
    city = st.text_input("City", value="New York", placeholder="Enter city name")
    
    # Category selection
    st.subheader("Categories")
    category_mode = st.radio(
        "Category Selection",
        ["All Default Categories", "Custom Selection"],
        help="Choose to use all default categories or select specific ones"
    )
    
    selected_categories = []
    if category_mode == "Custom Selection":
        selected_categories = st.multiselect(
            "Select Categories",
            config.DEFAULT_CATEGORIES,
            default=config.DEFAULT_CATEGORIES[:5],  # Default to first 5
            help="Select specific business categories to search"
        )
    else:
        selected_categories = None  # Will use all default categories
    
    # Minimum score threshold
    min_score = st.slider(
        "Minimum Lead Score",
        min_value=0,
        max_value=100,
        value=30,
        help="Only save leads with score above this threshold"
    )
    st.caption(f"Current default: All leads saved")
    
    # Long-running mode
    long_running = st.checkbox(
        "Long-running Mode",
        value=False,
        help="Allow discovery to run for extended periods (up to 24 hours)"
    )
    
    st.divider()
    
    # Status indicator
    st.subheader("Status")
    if st.session_state.is_running:
        st.markdown('<p class="status-running">● Running</p>', unsafe_allow_html=True)
        status = st.session_state.app.get_status()
        if status.get('current_country'):
            st.write(f"**Country:** {status.get('current_country')}")
            st.write(f"**City:** {status.get('current_city')}")
            st.write(f"**Category:** {status.get('current_category', 'N/A')}")
            st.write(f"**Run ID:** {status.get('run_id', 'N/A')}")
    else:
        st.markdown('<p class="status-stopped">○ Stopped</p>', unsafe_allow_html=True)
    
    st.divider()
    
    # Control buttons
    col1, col2 = st.columns(2)
    
    with col1:
        start_disabled = st.session_state.is_running or not city.strip()
        if st.button("▶️ Start", disabled=start_disabled, use_container_width=True, type="primary"):
            if category_mode == "Custom Selection" and not selected_categories:
                st.error("Please select at least one category")
            else:
                # Reset leads and queue before starting (main thread only)
                st.session_state.leads_found = []
                while not st.session_state.lead_queue.empty():
                    try:
                        st.session_state.lead_queue.get_nowait()
                    except Empty:
                        break
                
                # Update state before starting thread
                st.session_state.is_running = True
                st.session_state.current_run_id = st.session_state.app.run_id
                
                # Start thread (pass app instance, not session state)
                thread = threading.Thread(
                    target=run_discovery,
                    args=(st.session_state.app, selected_country, city, selected_categories)
                )
                thread.daemon = True
                st.session_state.discovery_thread = thread
                thread.start()
                
                # Check thread completion in a separate way
                def check_thread_completion():
                    """Check if thread completed and update state"""
                    if thread.is_alive():
                        return
                    st.session_state.is_running = False
                
                st.rerun()
    
    with col2:
        stop_disabled = not st.session_state.is_running
        if st.button("⏹️ Stop", disabled=stop_disabled, use_container_width=True):
            st.session_state.app.stop()
            st.session_state.is_running = False
            st.rerun()
    
    st.divider()
    
    # Quick stats
    st.subheader("Quick Stats")
    total_leads = len(st.session_state.leads_found)
    if total_leads > 0:
        avg_score = sum(lead.get('lead_score', 0) for lead in st.session_state.leads_found) / total_leads
        st.metric("Total Leads", total_leads)
        st.metric("Avg Score", f"{avg_score:.1f}")
    else:
        st.caption("No leads found yet")

# Main content area
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📋 Recent Leads", "📈 Statistics", "ℹ️ About"])

with tab1:
    st.header("Discovery Dashboard")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status = st.session_state.app.get_status()
        is_running = status.get('is_running', False)
        status_text = "Running" if is_running else "Idle"
        st.metric("Status", status_text)
    
    with col2:
        total_leads = len(st.session_state.leads_found)
        st.metric("Leads Found", total_leads)
    
    with col3:
        if total_leads > 0:
            high_score_leads = sum(1 for lead in st.session_state.leads_found if lead.get('lead_score', 0) >= 70)
            st.metric("High Quality Leads", high_score_leads)
        else:
            st.metric("High Quality Leads", 0)
    
    with col4:
        if st.session_state.current_run_id:
            st.metric("Current Run ID", st.session_state.current_run_id[:8])
        else:
            st.metric("Current Run ID", "N/A")
    
    st.divider()
    
    # Real-time progress (if running)
    if st.session_state.is_running:
        st.info("🔄 Discovery in progress... Check the Recent Leads tab for results.")
        status = st.session_state.app.get_status()
        if status.get('current_category'):
            st.write(f"**Currently processing:** {status.get('current_category')} in {status.get('current_city')}, {status.get('current_country')}")
    else:
        st.info("👈 Configure your search in the sidebar and click 'Start' to begin discovery.")
    
    st.divider()
    
    # Category overview
    st.subheader("Category Overview")
    if selected_categories:
        st.write(f"**Selected Categories:** {len(selected_categories)}")
        # Show selected categories in a nice format
        cols = st.columns(min(4, len(selected_categories)))
        for idx, cat in enumerate(selected_categories[:12]):  # Show first 12
            with cols[idx % 4]:
                st.caption(f"• {cat}")
        if len(selected_categories) > 12:
            st.caption(f"... and {len(selected_categories) - 12} more")
    else:
        st.write(f"**All Default Categories:** {len(config.DEFAULT_CATEGORIES)} categories")

with tab2:
    st.header("Recent Leads")
    
    if st.session_state.leads_found:
        # Filter and sort options
        col1, col2 = st.columns(2)
        with col1:
            sort_by = st.selectbox("Sort by", ["Score (High to Low)", "Score (Low to High)", "Name (A-Z)", "Date (Recent)"])
        with col2:
            filter_score = st.slider("Filter by Score", 0, 150, 0)
        
        # Filter leads
        filtered_leads = [lead for lead in st.session_state.leads_found if lead.get('lead_score', 0) >= filter_score]
        
        # Sort leads
        if "Score (High to Low)" in sort_by:
            filtered_leads.sort(key=lambda x: x.get('lead_score', 0), reverse=True)
        elif "Score (Low to High)" in sort_by:
            filtered_leads.sort(key=lambda x: x.get('lead_score', 0))
        elif "Name (A-Z)" in sort_by:
            filtered_leads.sort(key=lambda x: x.get('business_name', ''))
        
        st.write(f"**Showing {len(filtered_leads)} of {len(st.session_state.leads_found)} leads**")
        
        # Display leads
        for idx, lead in enumerate(filtered_leads[:50]):  # Show first 50
            with st.expander(f"🏢 {lead.get('business_name', 'Unknown')} - Score: {lead.get('lead_score', 0)}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Category:** {lead.get('category', 'N/A')}")
                    st.write(f"**Location:** {lead.get('city', 'N/A')}, {lead.get('country', 'N/A')}")
                    st.write(f"**Address:** {lead.get('address', 'N/A')}")
                    st.write(f"**Rating:** {lead.get('rating', 'N/A')} ⭐ ({lead.get('review_count', 0)} reviews)")
                
                with col2:
                    score = lead.get('lead_score', 0)
                    score_class = get_score_class(score)
                    st.markdown(f'<span class="{score_class}">Score: {score}</span>', unsafe_allow_html=True)
                    st.write(f"**Phone:** {lead.get('phone', 'N/A')}")
                    st.write(f"**Email:** {lead.get('email', 'N/A')}")
                    if lead.get('website'):
                        st.write(f"**Website:** [{lead.get('website')}]({lead.get('website')})")
                    st.write(f"**Justification:** {lead.get('value_justification', 'N/A')}")
        
        if len(filtered_leads) > 50:
            st.info(f"Showing first 50 leads. Total: {len(filtered_leads)}")
    else:
        st.info("No leads found yet. Start a discovery to see results here.")
        st.caption("Leads will appear here in real-time as they are discovered and saved to Google Sheets.")

with tab3:
    st.header("Statistics")
    
    if st.session_state.leads_found:
        # Lead score distribution
        st.subheader("Lead Score Distribution")
        scores = [lead.get('lead_score', 0) for lead in st.session_state.leads_found]
        
        col1, col2 = st.columns(2)
        with col1:
            st.bar_chart(pd.Series(scores))
        
        with col2:
            df_scores = pd.DataFrame({
                'Range': ['0-30', '31-50', '51-70', '71-90', '91+'],
                'Count': [
                    sum(1 for s in scores if 0 <= s <= 30),
                    sum(1 for s in scores if 31 <= s <= 50),
                    sum(1 for s in scores if 51 <= s <= 70),
                    sum(1 for s in scores if 71 <= s <= 90),
                    sum(1 for s in scores if s >= 91)
                ]
            })
            st.dataframe(df_scores, use_container_width=True, hide_index=True)
        
        # Category breakdown
        st.subheader("Leads by Category")
        category_counts = {}
        for lead in st.session_state.leads_found:
            cat = lead.get('category', 'Unknown')
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        if category_counts:
            df_categories = pd.DataFrame(list(category_counts.items()), columns=['Category', 'Count'])
            df_categories = df_categories.sort_values('Count', ascending=False)
            st.bar_chart(df_categories.set_index('Category'))
        
        # Location breakdown
        st.subheader("Leads by Location")
        location_counts = {}
        for lead in st.session_state.leads_found:
            loc = f"{lead.get('city', 'Unknown')}, {lead.get('country', 'Unknown')}"
            location_counts[loc] = location_counts.get(loc, 0) + 1
        
        if location_counts:
            df_locations = pd.DataFrame(list(location_counts.items()), columns=['Location', 'Count'])
            df_locations = df_locations.sort_values('Count', ascending=False)
            st.dataframe(df_locations.head(10), use_container_width=True, hide_index=True)
    else:
        st.info("No statistics available yet. Start a discovery to generate statistics.")

with tab4:
    st.header("About")
    
    st.markdown("""
    ### B2B Lead Discovery System
    
    A personal, high-precision B2B lead intelligence system for discovering businesses worldwide 
    that are ideal clients for software development, automation, cloud infrastructure, and AI services.
    
    #### Features
    - 🌍 Country-aware discovery (20+ countries)
    - 🎯 100+ pre-configured business categories
    - 📊 Intelligent lead scoring
    - 📝 Auto-generated value justifications
    - 📈 Google Sheets integration
    - 🌐 Website quality analysis
    
    #### System Principles
    - **Quality over quantity**: Focus on highly relevant, actionable leads
    - **Manual control**: Start/stop execution as needed
    - **Minimal infrastructure**: Optimized for free GCP credits
    - **Single-user, personal use**: Designed for individual use
    
    #### Usage Tips
    1. Select country and enter city name
    2. Choose categories (or use all defaults)
    3. Click "Start" to begin discovery
    4. Monitor progress in the Dashboard tab
    5. View discovered leads in Recent Leads tab
    6. All leads are automatically saved to Google Sheets
    
    #### Configuration
    - Edit `config.py` to customize categories, scoring weights, and delays
    - Set up Google Sheets API credentials (see QUICKSTART.md)
    - Optional: Add Google Places API key for better results
    
    #### Support
    - See README.md for detailed documentation
    - See QUICKSTART.md for setup instructions
    - See DEPLOYMENT_GCP.md for cloud deployment
    """)
    
    st.divider()
    
    # System info
    st.subheader("System Information")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Total Categories:** {len(config.DEFAULT_CATEGORIES)}")
        st.write(f"**Supported Countries:** {len(list_all_countries())}")
    with col2:
        st.write(f"**Default Delay:** {config.DEFAULT_DELAY_BETWEEN_REQUESTS}s between requests")
        st.write(f"**Max Results per Category:** {config.MAX_RESULTS_PER_CATEGORY}")

# Process lead queue to update UI with new leads (thread-safe)
process_lead_queue()

# Check if discovery thread completed (if running)
if st.session_state.is_running and st.session_state.discovery_thread:
    if not st.session_state.discovery_thread.is_alive():
        # Thread completed, update state
        st.session_state.is_running = False

# Auto-refresh when running (check every 3 seconds)
if st.session_state.is_running:
    time.sleep(3)
    st.rerun()

