# Agentic AI Data Agent 📊🤖

A production-grade, extensible AI Data Assistant that lets users upload CSV datasets, ask questions in plain English, execute safe read-only SQL queries, perform exploratory data analysis, and run automated data quality audits.

Built with **Streamlit**, **pandas**, **SQLite**, **SQLAlchemy**, and **Pydantic**. Includes a 100% offline **Local Deterministic Engine** that requires no paid LLM API keys.

---

## 1. Architecture & Design Principles

```
User Query / CSV Dataset
       │
       ▼
 ┌─────────────┐
 │ Streamlit UI│ (8 Navigational Views: Upload, Explorer, AI Assistant, etc.)
 └──────┬──────┘
        │
        ├─────────────────────────────────────────────────┐
        ▼                                                 ▼
┌──────────────────┐                           ┌────────────────────┐
│ DataLoaderService│                           │  Request Router    │
│ (25MB validation,│                           │ (Intent Classifier)│
│  type profiling) │                           └──────────┬─────────┘
└───────┬──────────┘                                      │
        │                                ┌────────────────┼────────────────┐
        ▼                                ▼                ▼                ▼
┌─────────────────┐             ┌───────────────┐ ┌───────────────┐ ┌────────────────┐
│ DatabaseManager │             │  SQL Analyst  │ │ Data Analyst  │ │ Quality Analyst│
│ (Sanitization,  │             │(Template/Safe)│ │ (Aggregations,│ │ (Missing, IQR  │
│  Catalog Table) │             └───────┬───────┘ │  Correlations)│ │  Outliers,     │
└───────┬─────────┘                     │         └───────┬───────┘ │  Duplicates)  │
        ▼                               ▼                 ▼         └────────┬───────┘
┌───────────────────────────────────────────────┐         │                  │
│               SQLite Engine                   │◄────────┴──────────────────┘
│  (Sanitized tables & read-only enforcement)   │
└───────────────────────────────────────────────┘
```

### Request Classification
The application classifies queries into 4 distinct intents:
1. `SQL_ANALYST`: Queries asking for specific records, slices, top/bottom rows, or sorting.
2. `DATA_ANALYST`: Queries requesting summary statistics, mean/median, correlations, distributions, or charts.
3. `DATA_QUALITY_ANALYST`: Inquiries asking for missing values, duplicates, outliers, or anomalies.
4. `GENERAL_HELP`: Assistance explaining the application architecture and how to write queries.

> **Distinction Note**: Local mode uses deterministic keyword matching and AST templates rather than black-box autonomous AI. This ensures predictability, zero cost, and zero hallucination.

### Multi-Layer SQL Security
The SQL execution engine implements multi-layered security:
- **Strict SELECT Policy**: Rejects all `DROP`, `INSERT`, `UPDATE`, `DELETE`, `ALTER`, `ATTACH`, `PRAGMA`, etc.
- **Stacked Query Prevention**: Rejects multi-statement injections and semicolons.
- **Table Whitelisting**: Analyzes SQL AST using `sqlparse` and guarantees queries only reference authorized dataset tables.
- **Dangerous Function Blocking**: Rejects SQLite system calls (`load_extension`, `writefile`, etc.).
- **Automatic Row Limiting**: Enforces strict row limits to prevent memory exhaustion.

---

## 2. Project Directory Structure

```
agentic-ai-data-agent/
├── app.py                      # Multi-page Streamlit application
├── requirements.txt            # Project dependencies
├── .env.example                # Configuration template
├── README.md                   # Full documentation & guide
├── agents/
│   ├── router.py               # Deterministic request router
│   ├── sql_analyst.py          # SQL generator and runner
│   ├── data_analyst.py         # Statistical analysis agent
│   └── data_quality_analyst.py # Automated data profiling agent
├── core/
│   ├── config.py               # Application settings
│   ├── database.py             # SQLAlchemy engine & catalog manager
│   └── security.py             # SQL AST security validator
├── services/
│   ├── data_loader.py          # CSV validator, profiler & ingestor
│   ├── query_service.py        # Safe query executor
│   ├── analytics_service.py    # Descriptive statistics & correlation engine
│   └── quality_service.py      # Missing values & IQR outlier auditor
├── models/
│   └── schemas.py              # Pydantic data schemas
├── data/
│   ├── sample_spotify.csv      # Synthetic sample dataset (30 records)
│   └── agent_data.db           # SQLite database
└── tests/
    ├── test_placeholder.py     # Scaffolding and model smoke tests
    ├── test_data_loader.py     # CSV upload & storage tests
    └── test_agents_and_security.py # Router, agents & SQL security tests
```

---

## 3. Installation & Getting Started

### 1. Setup Virtual Environment
```bash
git clone <repo-url> agentic-ai-data-agent
cd agentic-ai-data-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment (Optional)
```bash
cp .env.example .env
```
*(By default, the application runs 100% locally with zero API keys required).*

### 3. Run Automated Tests
```bash
pytest tests/ -v
```

### 4. Launch the Streamlit Web Application
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 4. Example Questions to Try

1. **SQL Analyst**:
   - `Show top 5 records`
   - `Which artist has the highest average popularity?`
   - `Show top 10 songs by energy`
2. **Data Analyst**:
   - `Calculate average popularity by artist`
   - `Calculate summary statistics for numeric attributes`
   - `Compute correlation between danceability and energy`
3. **Data Quality Analyst**:
   - `Find missing values in every column`
   - `Check for outliers and duplicate rows`
4. **General Help**:
   - `How do I use this application?`

---

## 5. Known Limitations & Future Enhancements

- **Current Heuristic Routing**: Rule-based routing covers standard patterns; nuanced phrasing may fall back to exploratory data analysis. Future versions can plug in LLM embeddings or classification models.
- **Single-Table SQL**: Focused on single-dataset analysis. Future versions can support multi-table relational joins.
- **Distributed Scale**: Built on SQLite and pandas (optimal for CSVs < 100MB). For gigabyte-scale datasets, future versions can incorporate DuckDB or Polars.
