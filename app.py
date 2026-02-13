import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. Page Configuration
st.set_page_config(page_title="FASTECH | Project Control", layout="wide", page_icon="🏗️")

# 2. Ultra-Clean Premium CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');

    /* Paksa Background Putih Bersih */
    .stApp {
        background-color: #ffffff !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Hilangkan Header Streamlit yang mengganggu */
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Header Box Premium */
    .premium-header {
        background: linear-gradient(135deg, #001f3f 0%, #004a99 100%);
        padding: 40px;
        border-radius: 20px;
        margin-bottom: 30px;
        color: white !important;
        box-shadow: 0 10px 30px rgba(0,74,153,0.15);
    }
    .premium-header h1 { color: #ffffff !important; font-weight: 700; margin-bottom: 0; }
    .premium-header p { color: #d1d1d1 !important; font-size: 1.1rem; }

    /* Glassmorphism Cards untuk Statistik */
    div[data-testid="stMetric"] {
        background: #f8f9fa !important;
        border: 1px solid #eeeeee !important;
        padding: 25px !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02) !important;
    }
    div[data-testid="stMetric"] label { color: #666666 !important; font-weight: 600 !important; }
    div[data-testid="stMetric"] div { color: #001f3f !important; font-weight: 700 !important; }

    /* Sidebar Dark Mode (Stay Professional) */
    section[data-testid="stSidebar"] {
        background-color: #001f3f !important;
        color: white !important;
    }
    section[data-testid="stSidebar"] .stMarkdown h2, 
    section[data-testid="stSidebar"] label {
        color: white !important;
    }

    /* Jam & Tanggal Modern */
    .clock-widget {
        background: #f0f2f6;
        padding: 10px 20px;
        border-radius: 50px;
        color: #001f3f !important;
        font-weight: 700;
        display: inline-block;
        border: 1px solid #e0e0e0;
        margin-bottom: 20px;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f8f9fa;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        color: #666;
    }
    .stTabs [aria-selected="true"] {
        background-color: #004a99 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Widget Jam Real-time (UI Bersih)
st.markdown("""
    <div style="text-align: right;">
        <div id="clock" class="clock-widget">Memuat waktu...</div>
    </div>
    <script>
    function updateClock() {
        var now = new Date();
        var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' };
        document.getElementById('clock').innerHTML = '🕒 ' + now.toLocaleDateString('id-ID', options);
    }
    setInterval(updateClock, 1000);
    updateClock();
    </script>
    """, unsafe_allow_html=True)

# 4. Logic Database
DATA_FILE = "tasks_fastech_pro.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Project", "Task", "Pic", "Deadline", "Status", "Timestamp"])

# --- UI CONTENT ---
st.markdown("""
    <div class="premium-header">
        <h1>TIM CREATIVE FASTECH ARCHITECT</h1>
        <p>Operational Control & Monitoring Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.header("➕ Input Task Baru")
    with st.form("new_task", clear_on_submit=True):
        proj = st.text_input("Nama Proyek")
        task = st.text_area("Detail Pekerjaan")
        pic = st.selectbox("Assign Ke", ["Tim CS", "PIC / Owner", "Tim Drafter", "Other"])
        dl = st.date_input("Deadline")
        
        if st.form_submit_button("Daftarkan Pekerjaan"):
            if proj and task:
                new_data = pd.DataFrame([[proj, task, pic, str(dl), "To Do", datetime.now().strftime("%d/%m/%Y %H:%M")]],
                                        columns=["Project", "Task", "Pic", "Deadline", "Status", "Timestamp"])
                df = load_data()
                df = pd.concat([df, new_data], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.success("Tersimpan!")
                st.rerun()

# --- MAIN DASHBOARD ---
df = load_data()

# Statistik Atas
c1, c2, c3 = st.columns(3)
c1.metric("Total Project", len(df))
c2.metric("On Progress", len(df[df['Status'] != "Done"]))
c3.metric("Completed", len(df[df['Status'] == "Done"]))

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🚀 Monitoring Aktif", "📜 Riwayat Selesai"])

with tab1:
    active_tasks = df[df['Status'] != "Done"]
    if not active_tasks.empty:
        for idx, row in active_tasks.iterrows():
            with st.container():
                st.markdown(f"""
                <div style="background: #ffffff; padding: 20px; border: 1px solid #eee; border-radius: 15px; margin-bottom: 15px; border-left: 5px solid #004a99;">
                    <h3 style="margin:0; color:#001f3f;">{row['Project']}</h3>
                    <p style="color:#666; margin-bottom: 5px;">PIC: <b>{row['Pic']}</b> | Deadline: {row['Deadline']}</p>
                    <p style="color:#333;">{row['Task']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Kontrol Status
                col_a, col_b = st.columns([3, 1])
                new_status = col_a.select_slider("Update Progres", options=["To Do", "In Progress", "Done"], value=row['Status'], key=f"s_{idx}")
                if col_b.button("🗑️ Hapus", key=f"d_{idx}"):
                    df = df.drop(idx)
                    df.to_csv(DATA_FILE, index=False)
                    st.rerun()
                
                if new_status != row['Status']:
                    df.at[idx, 'Status'] = new_status
                    df.to_csv(DATA_FILE, index=False)
                    st.rerun()
    else:
        st.info("Belum ada daftar pekerjaan yang berjalan.")

with tab2:
    done_tasks = df[df['Status'] == "Done"]
    if not done_tasks.empty:
        st.dataframe(done_tasks, use_container_width=True)
    else:
        st.caption("Arsip masih kosong.")
