import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. Page Configuration
st.set_page_config(page_title="Fastech | Dashboard Monitoring", layout="wide", page_icon="🏗️")

# 2. CSS Premium: Orange, Black, White
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

    /* Background Utama Putih */
    .stApp {
        background-color: #ffffff !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Hilangkan Elemen Default Streamlit */
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Header Premium Orange-Hitam */
    .premium-header {
        background: linear-gradient(135deg, #FF6B00 0%, #E65C00 100%);
        padding: 55px 45px;
        border-radius: 20px;
        margin-bottom: 25px;
        color: white !important;
        box-shadow: 0 10px 30px rgba(255, 107, 0, 0.2);
        border-bottom: 8px solid #1a1a1a;
    }
    .premium-header h1 { 
        color: #ffffff !important; 
        font-weight: 800; 
        margin: 0; 
        font-size: 2.8rem; 
        letter-spacing: -1.5px;
    }
    .premium-header p { 
        color: #1a1a1a !important; 
        font-size: 1.15rem; 
        margin-top: 8px; 
        font-weight: 600;
        opacity: 0.9;
    }

    /* Metric Cards - Orange Accent */
    div[data-testid="stMetric"] {
        background: #ffffff !important;
        border: 2px solid #f0f0f0 !important;
        padding: 25px !important;
        border-radius: 18px !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.02) !important;
        border-top: 5px solid #FF6B00 !important;
    }
    div[data-testid="stMetric"] label { color: #1a1a1a !important; font-weight: 700 !important; }
    div[data-testid="stMetric"] div { color: #FF6B00 !important; font-weight: 800 !important; }

    /* Jam Real-time - Black & Orange */
    .clock-widget {
        background: #1a1a1a;
        padding: 12px 28px;
        border-radius: 50px;
        color: #FF6B00 !important;
        font-weight: 800;
        display: inline-block;
        border: 2px solid #FF6B00;
        margin-bottom: 20px;
        font-size: 1rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    /* Form Expander - Orange Theme */
    .stExpander {
        border: 1px solid #FF6B00 !important;
        border-radius: 15px !important;
        background-color: #fff9f5 !important;
    }

    /* Tombol Hitam Premium */
    .stButton>button {
        background-color: #1a1a1a !important;
        color: #FF6B00 !important;
        border: 2px solid #FF6B00 !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #FF6B00 !important;
        color: #1a1a1a !important;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 15px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f8f9fa;
        border-radius: 12px 12px 0 0;
        padding: 12px 25px;
        color: #1a1a1a;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF6B00 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Real-time Clock Logic (Orange Accent)
st.markdown("""
    <div style="text-align: right;">
        <div id="orange-clock" class="clock-widget">🕒 Sinkronisasi Waktu...</div>
    </div>
    <script>
    function refreshClock() {
        const skr = new Date();
        const opsi = { 
            weekday: 'long', day: 'numeric', month: 'long', year: 'numeric',
            hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false 
        };
        const jamStr = new Intl.DateTimeFormat('id-ID', opsi).format(skr);
        const el = document.getElementById('orange-clock');
        if (el) { el.innerHTML = '🕒 ' + jamStr; }
    }
    setInterval(refreshClock, 1000);
    refreshClock();
    </script>
    """, unsafe_allow_html=True)

# 4. Database Helper
DB_FILE = "tasks_fastech_v7.csv"
def load_db():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["Proyek", "Tugas", "PIC", "Deadline", "Status", "Waktu"])

# --- HEADER ---
st.markdown("""
    <div class="premium-header">
        <h1>Fastech Architect | Dashboard Monitoring</h1>
        <p>TIM CREATIVE • OPERATIONAL CONTROL SYSTEM</p>
    </div>
    """, unsafe_allow_html=True)

# --- PANEL TAMBAH TUGAS (Orange Accents) ---
with st.expander("➕ TAMBAH TUGAS BARU (KLIK DISINI)", expanded=False):
    with st.form("form_fastech", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Nama Proyek", placeholder="Contoh: Gedung Arsitektur A")
            # List PIC sesuai request
            pic = st.selectbox("Assign Ke", ["Tim CS", "PIC / Owner", "Tim Drafter", "Other"])
        with c2:
            limit = st.date_input("Deadline")
            short_task = st.text_input("Ringkasan Tugas", placeholder="Contoh: Revisi Fasad")
        
        detail = st.text_area("Detail Instruksi Lengkap")
        
        if st.form_submit_button("SIMPAN DATA KE SISTEM"):
            if name and short_task:
                new_row = pd.DataFrame([[name, f"{short_task} - {detail}", pic, str(limit), "To Do", datetime.now().strftime("%d/%m/%Y %H:%M")]],
                                        columns=["Proyek", "Tugas", "PIC", "Deadline", "Status", "Waktu"])
                df = load_db()
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.balloons()
                st.rerun()

# --- DASHBOARD STATS ---
df = load_db()
col_a, col_b, col_c = st.columns(3)
col_a.metric("Total Proyek", len(df))
col_b.metric("On Progress", len(df[df['Status'] != "Done"]))
col_c.metric("Selesai", len(df[df['Status'] == "Done"]))

st.markdown("<br>", unsafe_allow_html=True)

# --- TASK MONITORING ---
t_active, t_done = st.tabs(["🔥 Pekerjaan Berjalan", "📜 Riwayat Archive"])

with t_active:
    ongoing = df[df['Status'] != "Done"]
    if not ongoing.empty:
        for i, r in ongoing.iterrows():
            st.markdown(f"""
            <div style="background: white; padding: 25px; border: 1px solid #eee; border-radius: 18px; margin-bottom: 20px; border-left: 10px solid #FF6B00; box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
                <h3 style="margin:0; color:#1a1a1a;">{r['Proyek']}</h3>
                <p style="color:#FF6B00; font-weight: bold; margin-bottom: 10px;">PIC: {r['PIC']} | Deadline: {r['Deadline']}</p>
                <div style="background:#fdfdfd; padding:15px; border-radius:10px; border:1px dashed #FF6B00; color:#333; font-size:0.95rem;">{r['Tugas']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Control Row
            ca, cb = st.columns([4, 1])
            up_status = ca.select_slider("Status Update", options=["To Do", "In Progress", "Done"], value=r['Status'], key=f"up_{i}")
            if cb.button("🗑️ Hapus", key=f"del_{i}"):
                df = df.drop(i)
                df.to_csv(DB_FILE, index=False)
                st.rerun()
            
            if up_status != r['Status']:
                df.at[i, 'Status'] = up_status
                df.to_csv(DB_FILE, index=False)
                st.rerun()
    else:
        st.info("Semua proyek sudah selesai atau belum ada input baru.")

with t_done:
    arsip = df[df['Status'] == "Done"]
    if not arsip.empty:
        st.table(arsip[["Proyek", "PIC", "Deadline", "Waktu"]])
    else:
        st.caption("Arsip pekerjaan selesai masih kosong.")
