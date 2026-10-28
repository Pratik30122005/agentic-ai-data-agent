"""
Agentic AI Data Agent - Streamlit Application
A multi-agent data assistant for CSV datasets, safe SQL analysis,
exploratory data analysis, and automated data quality profiling.
"""
import streamlit as st
import os

# Page Configuration
st.set_page_config(
    page_title="NexusData | Agentic AI Data Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Premium Styling & Navigation
with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 0 15px 0;">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 6px;">
            <div style="background: linear-gradient(135deg, #38bdf8, #818cf8); width: 38px; height: 38px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; box-shadow: 0 4px 12px rgba(56, 189, 248, 0.35);">⚡</div>
            <div>
                <div style="font-size: 1.35rem; font-weight: 800; background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -0.02em;">NexusData</div>
                <div style="font-size: 0.72rem; color: #94a3b8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em;">AI Data Agent v1.0</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Active Session Indicator
    if "active_table" in st.session_state:
        st.markdown(f"""
        <div style="background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 12px; padding: 12px; margin-bottom: 18px;">
            <div style="display: flex; align-items: center; gap: 6px;">
                <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #22c55e; box-shadow: 0 0 8px #22c55e;"></span>
                <span style="font-size: 0.75rem; color: #86efac; text-transform: uppercase; font-weight: 700;">Active Dataset</span>
            </div>
            <div style="font-size: 0.85rem; font-weight: 600; color: #f0fdf4; margin-top: 4px; word-break: break-all; font-family: monospace;">
                {st.session_state["active_table"]}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.25); border-radius: 12px; padding: 12px; margin-bottom: 18px;">
            <div style="display: flex; align-items: center; gap: 6px;">
                <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #f59e0b;"></span>
                <span style="font-size: 0.75rem; color: #fcd34d; text-transform: uppercase; font-weight: 700;">Engine Standby</span>
            </div>
            <div style="font-size: 0.8rem; color: #fef3c7; margin-top: 4px;">
                No dataset loaded. Ingest via Home or Upload.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='font-size: 0.75rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;'>Navigation Workflows</div>", unsafe_allow_html=True)

    sections = [
        "1. Home",
        "2. Upload Dataset",
        "3. Dataset Explorer",
        "4. AI Data Assistant",
        "5. SQL Query Results",
        "6. Data Quality Report",
        "7. Analytics Dashboard",
        "8. Query History"
    ]

    selected_section = st.radio("Navigation", sections, label_visibility="collapsed")

    st.markdown("<hr style='border-color: rgba(255, 255, 255, 0.08); margin: 20px 0;'>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 12px; padding: 14px;">
        <div style="font-size: 0.75rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin-bottom: 8px;">System Security</div>
        <div style="font-size: 0.8rem; color: #cbd5e1; display: flex; align-items: center; gap: 6px; margin-bottom: 4px;">
            <span style="color: #38bdf8;">✔</span> AST Query Isolation
        </div>
        <div style="font-size: 0.8rem; color: #cbd5e1; display: flex; align-items: center; gap: 6px; margin-bottom: 4px;">
            <span style="color: #38bdf8;">✔</span> 100% Offline Heuristics
        </div>
        <div style="font-size: 0.8rem; color: #cbd5e1; display: flex; align-items: center; gap: 6px;">
            <span style="color: #38bdf8;">✔</span> Zero SQL Injection
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Overall Page Theme - Pastel Pink & Rose */
    .stApp {
        background: linear-gradient(135deg, #fff5f7 0%, #fdf2f8 50%, #fce7f3 100%) !important;
        color: #4a1d34 !important;
    }
    
    /* Sidebar Light Pink Theme */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #fdf2f8 0%, #fbcfe8 100%) !important;
        border-right: 2px solid #f472b6 !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] > div {
        gap: 8px;
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label {
        background: rgba(255, 255, 255, 0.8);
        border: 1.5px solid #f9a8d4;
        border-radius: 14px;
        padding: 10px 14px;
        transition: all 0.2s ease;
        margin-bottom: 2px;
        cursor: pointer;
        color: #831843 !important;
        font-weight: 700;
        box-shadow: 0 2px 6px rgba(244, 114, 182, 0.1);
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {
        background: #ffffff;
        border-color: #ec4899;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(236, 72, 153, 0.2);
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-checked="true"] {
        background: linear-gradient(90deg, #ec4899, #f43f5e) !important;
        border-color: #db2777 !important;
        box-shadow: 0 4px 14px rgba(236, 72, 153, 0.35);
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-checked="true"] p {
        color: #ffffff !important;
        font-weight: 800;
    }
    
    /* Hero Banner Cute Pink */
    .hero-banner {
        background: linear-gradient(135deg, #ffffff 0%, #fff1f2 50%, #ffe4e6 100%);
        border: 2px solid #fbcfe8;
        border-radius: 28px;
        padding: 40px 48px;
        margin-bottom: 28px;
        box-shadow: 0 16px 36px rgba(244, 114, 182, 0.16);
    }
    .hero-tag {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #fce7f3;
        border: 1.5px solid #f472b6;
        color: #be185d;
        padding: 6px 16px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 800;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 14px;
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #db2777 0%, #e11d48 50%, #f43f5e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
        margin-bottom: 12px;
        letter-spacing: -0.02em;
    }
    .hero-sub {
        font-size: 1.15rem;
        color: #701a75;
        line-height: 1.65;
        max-width: 840px;
        font-weight: 600;
    }
    
    /* Stats Bar */
    .stat-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 30px;
    }
    .stat-box {
        background: #ffffff;
        border: 2px solid #fce7f3;
        border-radius: 18px;
        padding: 18px 22px;
        text-align: center;
        box-shadow: 0 6px 16px rgba(244, 114, 182, 0.1);
    }
    .stat-num {
        font-size: 1.8rem;
        font-weight: 800;
        color: #e11d48;
    }
    .stat-label {
        font-size: 0.82rem;
        color: #9d174d;
        font-weight: 700;
        text-transform: uppercase;
        margin-top: 2px;
    }
    
    /* Robot Agent Cards */
    .robot-card {
        background: #ffffff;
        border: 2px solid #fbcfe8;
        border-radius: 24px;
        padding: 26px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 8px 22px rgba(244, 114, 182, 0.1);
        height: 100%;
    }
    .robot-card:hover {
        transform: translateY(-6px);
        border-color: #ec4899;
        box-shadow: 0 16px 32px rgba(236, 72, 153, 0.24);
    }
    .robot-avatar {
        font-size: 3.2rem;
        margin-bottom: 10px;
        display: inline-block;
        filter: drop-shadow(0 4px 8px rgba(244, 114, 182, 0.3));
    }
    .robot-name {
        font-size: 1.25rem;
        font-weight: 800;
        color: #9d174d;
        margin-bottom: 6px;
    }
    .robot-badge {
        font-size: 0.75rem;
        font-weight: 800;
        background: #fdf2f8;
        color: #db2777;
        padding: 4px 12px;
        border-radius: 12px;
        display: inline-block;
        margin-bottom: 12px;
        border: 1px solid #fbcfe8;
    }
    .robot-desc {
        font-size: 0.92rem;
        color: #64748b;
        line-height: 1.55;
        font-weight: 600;
    }
    
    /* Tech Stack Pills */
    .tech-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #ffffff;
        border: 1.5px solid #fbcfe8;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.85rem;
        color: #9d174d;
        font-weight: 700;
        margin-right: 8px;
        margin-bottom: 8px;
        box-shadow: 0 2px 6px rgba(244, 114, 182, 0.08);
    }

    /* Primary Buttons */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #ec4899 0%, #f43f5e 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 800 !important;
        border-radius: 14px !important;
        padding: 12px 26px !important;
        box-shadow: 0 4px 16px rgba(236, 72, 153, 0.4) !important;
        transition: all 0.25s ease !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 8px 22px rgba(236, 72, 153, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

# Section 1: Home
if selected_section == "1. Home" or selected_section == "1. Home & Overview":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-tag">🤖 Meet Your Friendly AI Robot Squad 💖</div>
        <div class="hero-title">
            Hi! Welcome to NexusData <br>Your Agentic AI Data Buddy!
        </div>
        <div class="hero-sub">
            I turn messy CSV datasets into clean SQL queries, delightful chart visualizations, and deep statistical reports. Built with 100% offline deterministic heuristics — no paid APIs, no servers, zero hallucination, completely student-built & placement ready!
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Key Performance Metrics Ticker
    st.markdown("""
    <div class="stat-container">
        <div class="stat-box">
            <div class="stat-num">4 🤖</div>
            <div class="stat-label">Cartoon Robot Agents</div>
        </div>
        <div class="stat-box">
            <div class="stat-num">&lt; 10ms ⚡</div>
            <div class="stat-label">Fast Routing Latency</div>
        </div>
        <div class="stat-box">
            <div class="stat-num">100% 🛡️</div>
            <div class="stat-label">SQL Injection Guard</div>
        </div>
        <div class="stat-box">
            <div class="stat-num">0 $ 🌸</div>
            <div class="stat-label">Free & Offline Local Engine</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Agent Swarm Cards
    st.markdown("### 🤖 Meet Your Special Robot Buddies")
    st.markdown("Your questions are classified and routed to the most qualified robot helper:")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class="robot-card">
            <div class="robot-avatar">🤖⚡</div>
            <div class="robot-name">Router Bot</div>
            <div class="robot-badge">Intent Classifier</div>
            <div class="robot-desc">Listens to your question in plain English and dispatches the perfect robot buddy for the job!</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="robot-card">
            <div class="robot-avatar">🛡️👾</div>
            <div class="robot-name">SQL Bot</div>
            <div class="robot-badge">Database Specialist</div>
            <div class="robot-desc">Generates read-only SELECT queries with AST token isolation to prevent any database tampering!</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="robot-card">
            <div class="robot-avatar">📊🎨</div>
            <div class="robot-name">Analyst Bot</div>
            <div class="robot-badge">Stats & Charts Guru</div>
            <div class="robot-desc">Computes means, medians, correlation heatmaps, and draws beautiful dynamic visualizations!</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="robot-card">
            <div class="robot-avatar">🧪🔍</div>
            <div class="robot-name">Quality Bot</div>
            <div class="robot-badge">Dataset Doctor</div>
            <div class="robot-desc">Detects missing values, duplicate records, and spots crazy statistical outliers using IQR math!</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Interactive Architecture Diagram
    st.markdown("### 🔄 Production Architecture Pipeline")
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown("""
        <div class="step-card">
            <span class="step-num">1</span>
            <div style="font-weight: 700; color: #f8fafc; font-size: 0.95rem;">CSV Ingestion</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 4px;">25MB limit check, schema validation & table hashing</div>
        </div>
        """, unsafe_allow_html=True)
    with s2:
        st.markdown("""
        <div class="step-card">
            <span class="step-num">2</span>
            <div style="font-weight: 700; color: #f8fafc; font-size: 0.95rem;">Intent Classifier</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 4px;">Confidence scoring & heuristic agent dispatching</div>
        </div>
        """, unsafe_allow_html=True)
    with s3:
        st.markdown("""
        <div class="step-card">
            <span class="step-num">3</span>
            <div style="font-weight: 700; color: #f8fafc; font-size: 0.95rem;">Safe Execution</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 4px;">AST security policies, SQLite sandbox & aggregations</div>
        </div>
        """, unsafe_allow_html=True)
    with s4:
        st.markdown("""
        <div class="step-card">
            <span class="step-num">4</span>
            <div style="font-weight: 700; color: #f8fafc; font-size: 0.95rem;">Telemetry & Audit</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 4px;">Session execution audit history & latency metrics</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick Action Card
    st.markdown("""
    <div style="background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 18px; padding: 24px; margin-bottom: 24px;">
        <h4 style="margin: 0 0 10px 0; color: #f8fafc;">🚀 Quick Launch Demo</h4>
        <p style="color: #94a3b8; margin-bottom: 16px; font-size: 0.95rem;">
            Load the included synthetic Spotify dataset (30 records with natural features, outliers, and nulls) and test the agents immediately:
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_btn, _ = st.columns([1.5, 3])
    with col_btn:
        if st.button("⚡ Ingest Sample Dataset & Start", type="primary", use_container_width=True):
            from services.data_loader import DataLoaderService
            from core.database import DatabaseManager
            db = DatabaseManager()
            loader = DataLoaderService(db)
            sample_path = "data/sample_spotify.csv"
            if os.path.exists(sample_path):
                with open(sample_path, "rb") as f:
                    table_name, profile = loader.ingest_csv(f.read(), "sample_spotify.csv")
                    st.session_state["active_table"] = table_name
                    st.session_state["active_profile"] = profile
                    st.success(f"Successfully ingested `{table_name}`! Navigate to '4. AI Data Assistant' in the sidebar.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🛠️ Core Engineering Stack")
    st.markdown("""
    <div>
        <span class="tech-pill">🐍 Python 3.13</span>
        <span class="tech-pill">⚡ Streamlit</span>
        <span class="tech-pill">🐼 Pandas 2.2+</span>
        <span class="tech-pill">🗄️ SQLite & SQLAlchemy</span>
        <span class="tech-pill">🛡️ sqlparse AST Security</span>
        <span class="tech-pill">📐 Pydantic v2</span>
        <span class="tech-pill">🧪 pytest Suite (12 Tests)</span>
    </div>
    """, unsafe_allow_html=True)

# Section 2: Upload Dataset
elif selected_section == "2. Upload Dataset":
    st.header("📁 Upload & Ingest Dataset")
    st.markdown("Upload a CSV file to begin analysis (Max limit: **25 MB**).")
    
    from services.data_loader import DataLoaderService
    from core.database import DatabaseManager
    import pandas as pd
    
    db = DatabaseManager()
    loader = DataLoaderService(db)
    
    col_up, col_sample = st.columns([2, 1])
    with col_up:
        uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    with col_sample:
        st.markdown("**Or load sample data:**")
        if st.button("Load Synthetic Spotify Dataset"):
            sample_path = "data/sample_spotify.csv"
            if os.path.exists(sample_path):
                with open(sample_path, "rb") as f:
                    table_name, profile = loader.ingest_csv(f.read(), "sample_spotify.csv")
                    st.session_state["active_table"] = table_name
                    st.session_state["active_profile"] = profile
                    st.success(f"Loaded synthetic dataset into `{table_name}`!")
    
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        try:
            with st.spinner("Validating and storing dataset..."):
                table_name, profile = loader.ingest_csv(file_bytes, uploaded_file.name)
                st.session_state["active_table"] = table_name
                st.session_state["active_profile"] = profile
                st.success(f"Successfully processed `{uploaded_file.name}` into table `{table_name}`")
        except Exception as e:
            st.error(f"Upload Error: {str(e)}")
            
    if "active_profile" in st.session_state:
        p = st.session_state["active_profile"]
        st.subheader("📊 Dataset Overview")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Rows", f"{p['row_count']:,}")
        m2.metric("Columns", p["column_count"])
        m3.metric("Missing Cells", p["total_missing_cells"])
        m4.metric("Active Table", p["table_name"])
        
        st.markdown("### Column Profiling Summary")
        st.dataframe(pd.DataFrame(p["columns_summary"]), use_container_width=True)

# Section 3: Dataset Explorer
elif selected_section == "3. Dataset Explorer":
    st.header("🔍 Dataset Explorer")
    from core.database import DatabaseManager
    db = DatabaseManager()
    
    if "active_table" not in st.session_state:
        st.warning("No active dataset selected. Please upload a CSV in 'Upload Dataset' or load the sample data.")
    else:
        table_name = st.session_state["active_table"]
        st.info(f"Viewing active table: `{table_name}`")
        
        limit = st.slider("Preview row limit", min_value=5, max_value=100, value=20)
        df_preview = db.read_table(table_name, limit=limit)
        st.dataframe(df_preview, use_container_width=True)
        
        st.markdown("### Schema Details")
        st.write(df_preview.dtypes.to_frame(name="Pandas Dtype"))

# Section 4: AI Data Assistant
elif selected_section == "4. AI Data Assistant":
    st.header("💬 AI Data Assistant")
    
    if "active_table" not in st.session_state:
        st.warning("⚠️ Please upload a dataset or load the sample data first (Navigate to 'Upload Dataset').")
    else:
        active_table = st.session_state["active_table"]
        st.caption(f"Currently querying active dataset: `{active_table}`")
        
        # Example suggestion pills
        st.markdown("**Sample Prompts:**")
        cols_p = st.columns(4)
        sample_q = ""
        if cols_p[0].button("Show top 5 records"):
            sample_q = "Show top 5 records"
        if cols_p[1].button("Average popularity by artist"):
            sample_q = "Average popularity by artist"
        if cols_p[2].button("Find missing values"):
            sample_q = "Find missing values in every column"
        if cols_p[3].button("Calculate summary statistics"):
            sample_q = "Calculate summary statistics for numeric attributes"
            
        user_input = st.text_input("Ask a question about your data:", value=sample_q, placeholder="e.g. Show top 10 songs by energy")
        
        if st.button("Run Assistant", type="primary") and user_input:
            from agents.router import RequestRouter
            from agents.sql_analyst import SQLAnalystAgent
            from agents.data_analyst import DataAnalystAgent
            from agents.data_quality_analyst import DataQualityAnalystAgent
            from models.schemas import AgentIntent, QueryExecutionStatus, QueryHistoryRecord
            from datetime import datetime
            import time
            
            router = RequestRouter()
            with st.spinner("Routing intent and executing agent workflow..."):
                start_t = time.time()
                route = router.classify_request(user_input)
                
                # Render Routing Badge
                st.markdown(f"**Detected Intent:** `{route.detected_intent.value}` | **Agent:** `{route.selected_agent}` (Confidence: {route.confidence * 100:.0f}%)")
                st.caption(f"Routing rationale: {route.reason}")
                
                # Dispatch agent
                result = None
                if route.detected_intent == AgentIntent.SQL_ANALYST:
                    agent = SQLAnalystAgent()
                    result = agent.process(user_input, active_table)
                elif route.detected_intent == AgentIntent.DATA_ANALYST:
                    agent = DataAnalystAgent()
                    result = agent.process(user_input, active_table)
                elif route.detected_intent == AgentIntent.DATA_QUALITY_ANALYST:
                    agent = DataQualityAnalystAgent()
                    result = agent.process(user_input, active_table)
                else:
                    # GENERAL_HELP
                    from models.schemas import AgentExecutionResult
                    result = AgentExecutionResult(
                        success=True,
                        agent_name="General Help Assistant",
                        message="**Agentic AI Data Agent Guide:**\\n\\n"
                                "- **SQL Analyst**: Ask to view, slice, filter, or sort records (e.g., 'Show top 10 songs').\\n"
                                "- **Data Analyst**: Ask for aggregations, correlations, distributions, or plots (e.g., 'Average popularity by artist').\\n"
                                "- **Data Quality Analyst**: Ask for audit checks (e.g., 'Find missing values' or 'Check for outliers')."
                    )
                
                elapsed = (time.time() - start_t) * 1000
                
                # Record to Query History
                if "query_history" not in st.session_state:
                    st.session_state["query_history"] = []
                st.session_state["query_history"].append(QueryHistoryRecord(
                    timestamp=datetime.utcnow(),
                    user_question=user_input,
                    detected_intent=route.detected_intent,
                    selected_workflow=route.selected_agent,
                    execution_status=QueryExecutionStatus.SUCCESS if result.success else QueryExecutionStatus.ERROR,
                    details=result.message,
                    execution_time_ms=elapsed
                ))
                
                # Display Result
                if result.success:
                    st.success(result.message)
                    if result.sql_query:
                        st.session_state["last_sql_result"] = result
                        st.code(result.sql_query, language="sql")
                    if result.data:
                        import pandas as pd
                        df_res = pd.DataFrame(result.data)
                        st.dataframe(df_res, use_container_width=True)
                        if result.chart_spec and result.chart_spec.get("type") == "bar":
                            x_col = result.chart_spec["x"]
                            y_col = result.chart_spec["y"]
                            st.bar_chart(df_res.set_index(x_col)[y_col])
                    if result.quality_issues:
                        st.session_state["last_quality_result"] = result
                        for issue in result.quality_issues:
                            st.warning(issue)
                    if result.summary_metrics:
                        st.session_state["last_analytics_result"] = result
                        st.json(result.summary_metrics)
                else:
                    st.error(result.message)

# Section 5: SQL Query Results
elif selected_section == "5. SQL Query Results":
    st.header("🛡️ Safe SQL Execution & Results")
    if "last_sql_result" in st.session_state:
        res = st.session_state["last_sql_result"]
        st.subheader("Executed SQL Query")
        st.code(res.sql_query, language="sql")
        st.info(res.message)
        if res.data:
            import pandas as pd
            st.dataframe(pd.DataFrame(res.data), use_container_width=True)
    else:
        st.info("No SQL queries executed yet. Ask a record or limit query in the AI Data Assistant section.")

# Section 6: Data Quality Report
elif selected_section == "6. Data Quality Report":
    st.header("🧪 Automated Data Quality Report")
    if "active_table" not in st.session_state:
        st.warning("Please upload a dataset first.")
    else:
        from agents.data_quality_analyst import DataQualityAnalystAgent
        if st.button("Run Full Data Quality Audit", type="primary"):
            agent = DataQualityAnalystAgent()
            with st.spinner("Analyzing dataset health..."):
                audit_res = agent.process("perform quality audit", st.session_state["active_table"])
                st.session_state["last_quality_result"] = audit_res
        
        if "last_quality_result" in st.session_state:
            q_res = st.session_state["last_quality_result"]
            st.markdown(f"### Status: {q_res.message}")
            if q_res.quality_issues:
                for issue in q_res.quality_issues:
                    st.warning(f"⚠️ {issue}")
            else:
                st.success("✅ No quality anomalies detected.")
                
            metrics = q_res.summary_metrics or {}
            c1, c2 = st.columns(2)
            c1.metric("Total Rows Evaluated", metrics.get("total_rows", 0))
            c2.metric("Duplicate Rows", metrics.get("duplicate_rows", 0))
            
            if metrics.get("outliers"):
                st.markdown("#### Detected Numerical Outliers (IQR Method)")
                st.json(metrics["outliers"])

# Section 7: Analytics Dashboard
elif selected_section == "7. Analytics Dashboard":
    st.header("📈 Analytics Dashboard")
    if "active_table" not in st.session_state:
        st.warning("Please upload a dataset first.")
    else:
        from core.database import DatabaseManager
        from services.analytics_service import AnalyticsService
        import pandas as pd
        
        db = DatabaseManager()
        analytics = AnalyticsService()
        df = db.read_table(st.session_state["active_table"])
        
        st.subheader("Descriptive Statistics")
        stats = analytics.compute_summary_statistics(df)
        st.json(stats)
        
        st.subheader("Correlation Heatmap")
        corrs = analytics.compute_correlations(df)
        if corrs:
            corr_df = pd.DataFrame(corrs)
            st.dataframe(corr_df.style.background_gradient(cmap="Blues"), use_container_width=True)
        else:
            st.info("Fewer than 2 numeric columns found.")
            
        num_cols = df.select_dtypes(include=["number"]).columns.tolist()
        if num_cols:
            st.subheader("Distribution Viewer")
            chosen_col = st.selectbox("Select numeric feature to visualize:", num_cols)
            st.bar_chart(df[chosen_col].value_counts().sort_index())

# Section 8: Query History
elif selected_section == "8. Query History":
    st.header("📜 Query & Execution History")
    history = st.session_state.get("query_history", [])
    
    col_cnt, col_clr = st.columns([3, 1])
    col_cnt.markdown(f"Total Logged Queries: **{len(history)}**")
    if col_clr.button("Clear History"):
        st.session_state["query_history"] = []
        st.rerun()
        
    if history:
        import pandas as pd
        hist_records = [{
            "Timestamp": h.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "Question": h.user_question,
            "Intent": h.detected_intent.value,
            "Workflow": h.selected_workflow,
            "Status": h.execution_status.value,
            "Latency (ms)": round(h.execution_time_ms or 0, 1),
            "Details": h.details
        } for h in reversed(history)]
        st.dataframe(pd.DataFrame(hist_records), use_container_width=True)
    else:
        st.info("No queries have been executed yet in this session.")
