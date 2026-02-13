import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. Konfigurasi Halaman & Tab Browser
st.set_page_config(page_title="Fastech | Dashboard Monitoring", layout="wide", page_icon="🏗️")

# 2. CSS Ultra-Premium (Clean & High Contrast)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');

    /* Paksa Tema Terang */
    .stApp {
        background-color: #ffffff !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Sembunyikan Header Streamlit */
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Header Box Premium - Navy Gradient */
    .premium-header {
        background: linear-gradient(135deg, #001f3f 0%, #004a99 100%);
        padding: 50px 40px;
        border-radius: 20px;
        margin-bottom: 30px;
        color: white !important;
        box-shadow: 0 10px 30px rgba(0,74,153,0.15);
        text-align: left;
    }
    .premium-header h1 { 
        color: #ffffff !important; 
        font-weight: 700; 
        margin: 0; 
        font-size: 2.5rem;
        letter-spacing: -1px;
    }
    .premium-header p { 
        color: #d1d1d1 !important; 
        font-size: 1.1rem; 
        margin-top: 5px;
        opacity: 0.8;
    }

    /* Card Statistik Elegan */
    div[data-testid="stMetric"] {
        background: #fdfdfd !important;
        border: 1px solid #f0f0f0 !important;
        padding: 25px !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03) !important;
    }
    div[data-testid="stMetric"] label { 
        color: #555555 !important; 
        font-weight: 600 !important; 
        font-size: 1rem !important;
    }
    div[data-testid="stMetric"] div { 
        color: #001f3f !important; 
        font-weight: 700 !important; 
        font-size: 2rem !important;
    }

    /* Sidebar Professional Dark */
    section[data-testid="stSidebar"] {
        background-color: #001f3f !important;
    }
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    .stButton>button {
        background-color: #ffd700 !important;
        color: #001f3f !important;
        font-weight: bold !important;
        border: none !important;
        width: 100%;
        border-radius: 10px !important;
    }

    /* Widget Jam Real-time */
    .clock-pill {
        background: #f0f2f6;
        padding: 12px 25px;
        border-radius: 50px;
        color: #001f3f !important;
        font-weight: 700;
        display: inline-block;
        border: 1px solid #e0e0e0;
        margin-bottom: 25px;
        font-size: 0.95rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. JavaScript untuk Jam Real-time (Fix Leak)
st.markdown("""
    <div style="text-align: right;">
        <div id="live-clock" class="clock-pill">Memuat waktu...</div>
    </div>
    <script>
    function updateClock() {
        const now = new Date();
        const options = { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric', 
            hour: '2-digit', 
            minute: '2-digit', 
            second: '2-digit',
            hour12: false 
        };
        const formatter = new Intl.DateTimeFormat('id-ID', options);
        document.getElementById('live-clock').innerHTML = '🕒 ' + formatter.format(now);
    }
    // Update setiap detik
    setInterval(updateClock, 1000);
    // Jalankan langsung saat load
    updateClock();
    </script>
    """, unsafe_allow_html=True)

# 4. Fungsi Database Sederhana
DATA_FILE = "tasks_fastech_v5.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Project", "Task", "Pic", "Deadline", "Status", "Timestamp"])

# --- HEADER SECTION ---
st.markdown("""
    <div class="premium-header">
        <h1>Fastech Architect | Dashboard Monitoring</h1>
        <p>Operational Control System & Creative Team Analytics</p>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR: INPUT ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("➕ Tambah Tugas Baru")
    with st.form("task_entry", clear_on_submit=True):
        p_name = st.text_input("Nama Proyek")
        p_task = st.text_area("Detail Pekerjaan")
        # Daftar PIC sesuai permintaan
        p_pic = st.selectbox("Assign Ke", ["Tim CS", "PIC / Owner", "Tim Drafter", "Other"])
        p_date = st.date_input("Deadline")
        
        if st.form_submit_button("Daftarkan"):
            if p_name and p_task:
                new_row = pd.DataFrame([[p_name, p_task, p_pic, str(p_date), "To Do", datetime.now().strftime("%d/%m/%Y %H:%M")]],
                                        columns=["Project", "Task", "Pic", "Deadline", "Status", "Timestamp"])
                df = load_data()
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.toast("Tugas berhasil disimpan!", icon="✅")
                st.rerun()

# --- MAIN DASHBOARD ---
df = load_data()

# Statistik Utama
c1, c2, c3 = st.columns(3)
c1.metric("Total Project", len(df))
c2.metric("Sedang Jalan", len(df[df['Status'] != "Done"]))
c3.metric("Sudah Selesai", len(df[df['Status'] == "Done"]))

st.markdown("<br>", unsafe_allow_html=True)

# Tabs untuk Organisasi Data
tab_act, tab_rec = st.tabs(["🚀 Monitoring Progres", "📜 Arsip Pekerjaan"])

with tab_act:
    active = df[df['Status'] != "Done"]
    if not active.empty:
        for idx, row in active.iterrows():
            with st.container():
                st.markdown(f"""
                <div style="background: #ffffff; padding: 25px; border: 1px solid #eee; border-radius: 15px; margin-bottom: 20px; border-left: 6px solid #004a99;">
                    <h3 style="margin:0; color:#001f3f; font-size: 1.4rem;">{row['Project']}</h3>
                    <p style="color:#777; margin-bottom: 10px;">PIC: <b>{row['Pic']}</b> | Deadline: {row['Deadline']}</p>
                    <div style="background: #f9f9f9; padding: 15px; border-radius: 10px; color: #444; border: 1px inset #f0f0f0;">
                        {row['Task']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Kontrol Aksi
                col_s, col_d = st.columns([4, 1])
                new_st = col_s.select_slider("Status", options=["To Do", "In Progress", "Done"], value=row['Status'], key=f"sl_{idx}")
                
                if col_d.button("🗑️ Hapus", key=f"bt_{idx}"):
                    df = df.drop(idx)
                    df.to_csv(DATA_FILE, index=False)
                    st.rerun()
                
                if new_st != row['Status']:
                    df.at[idx, 'Status'] = new_st
                    df.to_csv(DATA_FILE, index=False)
                    st.rerun()
    else:
        st.info("Belum ada tugas aktif. Semua aman!")

with tab_rec:
    done = df[df['Status'] == "Done"]
    if not done.empty:
        st.dataframe(done[["Project", "Pic", "Deadline", "Timestamp"]], use_container_width=True)
    else:
        st.write("Belum ada riwayat pekerjaan selesai.")
