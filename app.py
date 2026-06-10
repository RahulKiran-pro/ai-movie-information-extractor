import streamlit as st
import json
import os
from dotenv import load_dotenv

load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Movie Info Extractor",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS — dark cinematic theme matching the screenshot ─────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Base reset ── */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif !important;
}
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── App background ── */
.stApp {
    background-color: #141414 !important;
    color: #E8E8E8 !important;
}
.main .block-container {
    padding: 2.5rem 3rem 3rem 3rem !important;
    max-width: 900px !important;
    margin: 0 auto !important;
}

/* ── Section labels (like "MOVIE DESCRIPTION") ── */
.section-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    color: #888888;
    text-transform: uppercase;
    margin-bottom: 10px;
    margin-top: 8px;
}

/* ── Textarea ── */
.stTextArea textarea {
    background-color: #1E1E1E !important;
    color: #D0D0D0 !important;
    border: 1px solid #2E2E2E !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 16px !important;
    resize: vertical !important;
    caret-color: #D0D0D0 !important;
}
.stTextArea textarea::placeholder { color: #555 !important; }
.stTextArea textarea:focus {
    border-color: #3E3E3E !important;
    box-shadow: none !important;
}
.stTextArea label { display: none !important; }

/* ── Text inputs (DB fields) ── */
.stTextInput input {
    background-color: #1E1E1E !important;
    color: #D0D0D0 !important;
    border: 1px solid #2E2E2E !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 12px 16px !important;
    height: 48px !important;
}
.stTextInput input:focus {
    border-color: #444 !important;
    box-shadow: none !important;
}
.stTextInput input::placeholder { color: #555 !important; }
.stTextInput label { display: none !important; }

/* ── Radio buttons → storage tabs ── */
div[data-testid="stHorizontalBlock"] .stRadio { margin-bottom: 0; }
.stRadio > label { display: none !important; }
.stRadio div[role="radiogroup"] {
    display: flex !important;
    flex-direction: row !important;
    gap: 10px !important;
    flex-wrap: wrap;
}
.stRadio div[role="radiogroup"] label {
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    padding: 10px 18px !important;
    border-radius: 10px !important;
    border: 1px solid #2E2E2E !important;
    background: #1A1A1A !important;
    color: #AAAAAA !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: all 0.15s !important;
}
.stRadio div[role="radiogroup"] label:has(input:checked) {
    background: #252525 !important;
    border-color: #555 !important;
    color: #EEEEEE !important;
}
.stRadio div[role="radiogroup"] label span { color: inherit !important; }
.stRadio div[role="radiogroup"] input[type="radio"] { display: none !important; }
.stRadio div[role="radiogroup"] label p { margin: 0 !important; color: inherit !important; }

/* ── Buttons ── */
.stButton > button {
    background: #EEEEEE !important;
    color: #111111 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 700 !important;
    padding: 13px 28px !important;
    letter-spacing: 0.03em;
    transition: all 0.15s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: #FFFFFF !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(255,255,255,0.08) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Save button (secondary) ── */
.save-btn > button {
    background: #1E1E1E !important;
    color: #EEEEEE !important;
    border: 1px solid #333 !important;
}
.save-btn > button:hover {
    background: #252525 !important;
    box-shadow: none !important;
}

/* ── Result card ── */
.result-card {
    background: #1A1A1A;
    border: 1px solid #282828;
    border-radius: 16px;
    padding: 28px 32px;
    margin-top: 8px;
}
.result-movie-title {
    font-size: 1.8rem;
    font-weight: 800;
    color: #EEEEEE;
    letter-spacing: -0.5px;
    line-height: 1.1;
    margin-bottom: 4px;
}
.result-year {
    font-size: 0.88rem;
    color: #666;
    margin-bottom: 20px;
}
.result-field-key {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    color: #666;
    text-transform: uppercase;
    margin-bottom: 5px;
    margin-top: 16px;
}
.result-field-val {
    font-size: 0.92rem;
    color: #CCCCCC;
    line-height: 1.6;
}
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.78rem;
    font-weight: 600;
    margin: 3px 3px 3px 0;
}
.badge-genre { background: #1F2B1F; color: #6DBE73; border: 1px solid #2D3F2D; }
.badge-cast  { background: #1C1F2B; color: #6B8FDB; border: 1px solid #252A3F; }
.rating-pill {
    display: inline-flex; align-items: center; gap: 6px;
    background: #222; border: 1px solid #333;
    border-radius: 8px; padding: 5px 12px;
    font-size: 0.88rem; color: #E8BA4A; font-weight: 700;
}
.divider { border: none; border-top: 1px solid #252525; margin: 20px 0; }
.mono-block {
    background: #141414;
    border: 1px solid #252525;
    border-radius: 10px;
    padding: 14px 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #888;
    white-space: pre-wrap;
    word-break: break-all;
    margin-top: 6px;
    max-height: 160px;
    overflow-y: auto;
}

/* ── Status messages ── */
.stAlert { border-radius: 10px !important; }
.stSuccess { background: #1A261A !important; border-color: #2D4A2D !important; color: #7DBF7D !important; }
.stError   { background: #261A1A !important; border-color: #4A2D2D !important; color: #BF7D7D !important; }
.stInfo    { background: #1A1E26 !important; border-color: #2D354A !important; color: #7D9FBF !important; }
.stWarning { background: #26221A !important; border-color: #4A3D2D !important; color: #BFAA7D !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #EEEEEE !important; }

/* ── History expander ── */
.streamlit-expanderHeader {
    background: #1A1A1A !important;
    border: 1px solid #282828 !important;
    border-radius: 10px !important;
    color: #AAAAAA !important;
}
.streamlit-expanderContent {
    background: #161616 !important;
    border: 1px solid #222 !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #141414; }
::-webkit-scrollbar-thumb { background: #2E2E2E; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
if "extracted" not in st.session_state:
    st.session_state.extracted = None
if "history" not in st.session_state:
    st.session_state.history = []


# ── Helper: build SQL INSERT ──────────────────────────────────────────────────
def build_sql(data: dict, table: str) -> str:
    cols = "title, release_year, director, genre, main_cast, rating, summary"
    genre = "{" + ",".join(data.get("genre", [])) + "}"
    cast  = "{" + ",".join(data.get("main_cast", [])) + "}"
    def esc(s): return str(s).replace("'", "''") if s else ""
    vals = (
        f"'{esc(data.get('movie_title',''))}', "
        f"'{esc(data.get('release_year',''))}', "
        f"'{esc(data.get('director',''))}', "
        f"'{genre}', "
        f"'{cast}', "
        f"{data.get('ratings') or 'NULL'}, "
        f"'{esc(data.get('summary',''))}'"
    )
    return f"INSERT INTO {table} ({cols})\nVALUES ({vals});"


# ── Helper: build Mongo insertOne ─────────────────────────────────────────────
def build_mongo(data: dict, db: str, col: str) -> str:
    doc = {
        "title":        data.get("movie_title"),
        "release_year": data.get("release_year"),
        "director":     data.get("director"),
        "genre":        data.get("genre", []),
        "main_cast":    data.get("main_cast", []),
        "rating":       data.get("ratings"),
        "summary":      data.get("summary"),
    }
    return f'db.getSiblingDB("{db}").{col}.insertOne(\n{json.dumps(doc, indent=2)}\n);'


# ── Helper: save to PostgreSQL ────────────────────────────────────────────────
def save_to_postgres(data: dict, host, port, dbname, table, user, password):
    try:
        import psycopg2
        conn = psycopg2.connect(
            host=host, port=int(port), dbname=dbname,
            user=user, password=password, connect_timeout=5
        )
        cur = conn.cursor()
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {table} (
                id SERIAL PRIMARY KEY,
                title TEXT, release_year TEXT, director TEXT,
                genre TEXT[], main_cast TEXT[],
                rating FLOAT, summary TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        cur.execute(
            f"INSERT INTO {table} (title,release_year,director,genre,main_cast,rating,summary) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (
                data.get("movie_title"), data.get("release_year"),
                data.get("director"),   data.get("genre", []),
                data.get("main_cast", []), data.get("ratings"),
                data.get("summary")
            )
        )
        conn.commit(); conn.close()
        return True, "Record inserted successfully into PostgreSQL!"
    except ImportError:
        return False, "psycopg2 not installed. Run: pip install psycopg2-binary"
    except Exception as e:
        return False, f"PostgreSQL error: {e}"


# ── Helper: save to MongoDB ───────────────────────────────────────────────────
def save_to_mongo(data: dict, uri, dbname, collection):
    try:
        from pymongo import MongoClient
        client = MongoClient(uri, serverSelectionTimeoutMS=4000)
        client.server_info()
        db = client[dbname]
        col = db[collection]
        doc = {
            "title": data.get("movie_title"), "release_year": data.get("release_year"),
            "director": data.get("director"), "genre": data.get("genre", []),
            "main_cast": data.get("main_cast", []), "rating": data.get("ratings"),
            "summary": data.get("summary"),
        }
        col.insert_one(doc)
        client.close()
        return True, f"Document inserted into `{dbname}.{collection}`!"
    except ImportError:
        return False, "pymongo not installed. Run: pip install pymongo"
    except Exception as e:
        return False, f"MongoDB error: {e}"


# ── LLM extraction ────────────────────────────────────────────────────────────
def extract_movie_info(description: str) -> dict:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY not found in .env file")

    from langchain_mistralai import ChatMistralAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import PydanticOutputParser
    from pydantic import BaseModel
    from typing import Optional, List

    class MovieInfo(BaseModel):
        movie_title: str
        release_year: Optional[str] = None
        director: Optional[str] = None
        genre: List[str] = []
        main_cast: List[str] = []
        ratings: Optional[float] = None
        summary: str

    model = ChatMistralAI(model="mistral-small-latest", api_key=api_key)
    parser = PydanticOutputParser(pydantic_object=MovieInfo)

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Extract structured information about a movie {format_instructions} "
         "from the given movie description."),
        ("human", "{movie_description}")
    ])

    response = model.invoke(
        prompt.invoke({
            "movie_description": description,
            "format_instructions": parser.get_format_instructions()
        })
    )

    # Try Pydantic parse first, fall back to raw JSON
    try:
        parsed = parser.parse(response.content)
        return parsed.model_dump()
    except Exception:
        import re
        raw = response.content
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError("Could not parse LLM response as JSON.")


# ══════════════════════════════════════════════════════════════════════════════
#  UI LAYOUT
# ══════════════════════════════════════════════════════════════════════════════

# ── App header ────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom: 2rem;">
    <div style="font-size:0.7rem;font-weight:700;letter-spacing:0.2em;color:#555;
                text-transform:uppercase;margin-bottom:6px;">🎬 LangChain + Mistral AI</div>
    <div style="font-size:2.2rem;font-weight:800;color:#EEEEEE;letter-spacing:-1px;
                line-height:1.1;">Movie Info Extractor</div>
    <div style="font-size:0.9rem;color:#666;margin-top:6px;">
        Paste a movie description → extract structured data → save to SQL or MongoDB
    </div>
</div>
""", unsafe_allow_html=True)


# ── Input section ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Movie description</div>', unsafe_allow_html=True)
movie_desc = st.text_area(
    label="movie_description",
    placeholder="e.g. Inception (2010) is a sci-fi thriller directed by Christopher Nolan, starring Leonardo DiCaprio as a thief who steals secrets from dreams. It received an 8.8 on IMDb...",
    height=130,
    key="movie_desc_input",
    label_visibility="collapsed",
)

st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

# ── Storage target ────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Storage target</div>', unsafe_allow_html=True)
storage = st.radio(
    "storage",
    ["🗄️  SQL (PostgreSQL)", "🍃  MongoDB", "👁️  Preview only"],
    horizontal=True,
    label_visibility="collapsed",
    key="storage_choice",
)

st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

# ── DB Config fields ──────────────────────────────────────────────────────────
if "SQL" in storage:
    c1, c2 = st.columns(2)
    with c1: sql_host  = st.text_input("Host",     value="localhost",  key="sql_host",  label_visibility="collapsed", placeholder="Host (e.g. localhost)")
    with c2: sql_port  = st.text_input("Port",     value="5432",       key="sql_port",  label_visibility="collapsed", placeholder="Port")
    c3, c4 = st.columns(2)
    with c3: sql_db    = st.text_input("Database", value="movies_db",  key="sql_db",    label_visibility="collapsed", placeholder="Database name")
    with c4: sql_table = st.text_input("Table",    value="movies",     key="sql_table", label_visibility="collapsed", placeholder="Table name")
    c5, c6 = st.columns(2)
    with c5: sql_user  = st.text_input("User",     value="postgres",   key="sql_user",  label_visibility="collapsed", placeholder="Username")
    with c6: sql_pass  = st.text_input("Password", value="",           key="sql_pass",  type="password", label_visibility="collapsed", placeholder="Password")

elif "MongoDB" in storage:
    mongo_uri = st.text_input("URI",        value="mongodb://localhost:27017", key="mongo_uri",  label_visibility="collapsed", placeholder="Connection URI")
    c1, c2   = st.columns(2)
    with c1: mongo_db  = st.text_input("Database",   value="movies_db", key="mongo_db",  label_visibility="collapsed", placeholder="Database name")
    with c2: mongo_col = st.text_input("Collection", value="movies",    key="mongo_col", label_visibility="collapsed", placeholder="Collection")

st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

# ── Extract button ─────────────────────────────────────────────────────────────
col_btn, col_pad = st.columns([2, 3])
with col_btn:
    extract_clicked = st.button("⚡  Extract & Analyse", key="extract_btn", use_container_width=True)

# ── Extraction logic ───────────────────────────────────────────────────────────
if extract_clicked:
    if not movie_desc.strip():
        st.error("Please enter a movie description first.")
    else:
        with st.spinner("Extracting structured information via Mistral AI…"):
            try:
                result = extract_movie_info(movie_desc.strip())
                st.session_state.extracted = result
                st.success("Extraction complete!")
            except Exception as e:
                st.error(f"Extraction failed: {e}")
                st.session_state.extracted = None


# ── Result display ────────────────────────────────────────────────────────────
if st.session_state.extracted:
    data = st.session_state.extracted

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Extracted information</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-card">
        <div class="result-movie-title">{data.get('movie_title', 'Unknown Title')}</div>
        <div class="result-year">{data.get('release_year', '') or 'Year unknown'} &nbsp;·&nbsp; Directed by {data.get('director', 'Unknown')}</div>
        <hr class="divider">
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:0 32px;">
            <div>
                <div class="result-field-key">Genre</div>
                <div class="result-field-val">
                    {''.join(f'<span class="badge badge-genre">{g}</span>' for g in data.get('genre', [])) or '—'}
                </div>
            </div>
            <div>
                <div class="result-field-key">Rating</div>
                <div class="result-field-val">
                    {'<span class="rating-pill">⭐ ' + str(data.get("ratings")) + ' / 10</span>' if data.get("ratings") else '—'}
                </div>
            </div>
        </div>
        <div class="result-field-key">Main Cast</div>
        <div class="result-field-val">
            {''.join(f'<span class="badge badge-cast">{c}</span>' for c in data.get('main_cast', [])) or '—'}
        </div>
        <div class="result-field-key">Summary</div>
        <div class="result-field-val">{data.get('summary', '—')}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── DB preview / save ──────────────────────────────────────────────────────
    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    if "SQL" in storage:
        table = st.session_state.get("sql_table", "movies")
        st.markdown('<div class="section-label">SQL Insert Preview</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="mono-block">{build_sql(data, table)}</div>', unsafe_allow_html=True)
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="save-btn">', unsafe_allow_html=True)
            if st.button("💾  Save to PostgreSQL", key="save_sql", use_container_width=False):
                with st.spinner("Connecting to PostgreSQL…"):
                    ok, msg = save_to_postgres(
                        data,
                        st.session_state.sql_host, st.session_state.sql_port,
                        st.session_state.sql_db,   st.session_state.sql_table,
                        st.session_state.sql_user, st.session_state.sql_pass,
                    )
                if ok:
                    st.success(msg)
                    st.session_state.history.append({"title": data.get("movie_title"), "db": "PostgreSQL"})
                else:
                    st.error(msg)
            st.markdown('</div>', unsafe_allow_html=True)

    elif "MongoDB" in storage:
        _db  = st.session_state.get("mongo_db", "movies_db")
        _col = st.session_state.get("mongo_col", "movies")
        st.markdown('<div class="section-label">MongoDB insertOne Preview</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="mono-block">{build_mongo(data, _db, _col)}</div>', unsafe_allow_html=True)
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        if st.button("🍃  Save to MongoDB", key="save_mongo"):
            with st.spinner("Connecting to MongoDB…"):
                ok, msg = save_to_mongo(
                    data,
                    st.session_state.mongo_uri,
                    st.session_state.mongo_db,
                    st.session_state.mongo_col,
                )
            if ok: st.success(msg); st.session_state.history.append({"title": data.get("movie_title"), "db": "MongoDB"})
            else:  st.error(msg)

    else:
        # Preview only — show raw JSON
        st.markdown('<div class="section-label">Raw JSON Output</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="mono-block">{json.dumps(data, indent=2)}</div>', unsafe_allow_html=True)

    # ── Copy JSON button ───────────────────────────────────────────────────────
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    st.code(json.dumps(data, indent=2), language="json")


# ── Session history ────────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
    with st.expander(f"📋  Session history ({len(st.session_state.history)} saved)", expanded=False):
        for i, item in enumerate(reversed(st.session_state.history), 1):
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;padding:8px 4px;'
                f'border-bottom:1px solid #222;font-size:0.88rem;">'
                f'<span style="color:#CCC;">{i}. {item["title"]}</span>'
                f'<span style="color:#666;">{item["db"]}</span></div>',
                unsafe_allow_html=True
            )