"""
Agentic AI Data Agent - Streamlit Application
A multi-agent data assistant for CSV datasets, safe SQL analysis,
exploratory data analysis, and automated data quality profiling.
"""
import streamlit as st
import os

st.set_page_config(
    page_title="Agentic AI Data Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App Title & Header
st.sidebar.title("🤖 AI Data Agent")
st.sidebar.markdown("**Your Intelligent Data Assistant**")

# Navigation options
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

selected_section = st.sidebar.radio("Navigate to:", sections)

st.sidebar.divider()
st.sidebar.info("Local Deterministic Mode: **Active**\\n\\nNo external LLM key required.")

# Section 1: Home
if selected_section == "1. Home":
    st.title("📊 Agentic AI Data Agent")
    st.markdown("""
    Welcome to the **Agentic AI Data Agent**! This application is designed to act as your pair data engineer,
    SQL specialist, and data analyst.
    
    ### 🚀 Key Capabilities
    - **Dataset Ingestion**: Safe CSV validation and SQLite persistent caching.
    - **Intent-Based Routing**: Automatically routes natural queries to the correct specialized agent:
        - `SQL_ANALYST`: Generates and safely validates SELECT queries.
        - `DATA_ANALYST`: Computes distributions, aggregations, correlations, and visualizations.
        - `DATA_QUALITY_ANALYST`: Detects missing values, duplicates, anomaly indicators, and data type issues.
        - `GENERAL_HELP`: Guidance on system architecture and query syntax.
    - **Multi-layered Security**: Whitelisted read-only SQL parser, AST inspection, and query timeouts.
    - **Zero Paid Dependencies**: Comes with a fully offline deterministic engine.
    
    👈 Use the sidebar navigation to get started by uploading a dataset or exploring the synthetic sample data!
    """)

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
