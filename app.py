import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. Page Configuration
st.set_page_config(page_title="Fastech | Dashboard Monitoring", layout="wide", page_icon="🏗️")

# 2. CSS Ultra-Premium (Fixed Visibility & Layout)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');

    .stApp {
        background-color: #ffffff !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Header Navy Premium */
    .premium-header {
        background: linear-gradient(135deg, #001f3f 0%, #004a99 100%);
        padding: 60px 40px;
        border-radius: 20px;
        margin-bottom: 20px;
        color: white !important;
        box-shadow: 0 10px 30px rgba(0,74,153,0.15);
    }
    .premium-header h1 { color: #ffffff !important; font-weight: 700; margin: 0; font-size: 2.8rem; }

    /* Widget Jam Real-time - Fixed */
    .clock-pill {
        background: #f0f2f6;
        padding: 12px 25px;
        border-radius: 50px;
        color: #001f3f !important;
        font-weight: 700;
        display: inline-block;
        border: 1px solid #e0e0e0;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }

    /* Container Form Tambah Tugas */
    .add-task-container {
        background-color: #f8f9fa;
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #eee;
        margin-bottom: 30px;
    }
    
    /* Tombol Submit Premium */
    .stButton>button {
        background-color: #004a99 !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 10px 25px !important;
        font-weight: 600 !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. JavaScript Jam Real-time (Fixed agar Berdetak)
st.markdown("""
    <div style="text-align: right;">
        <div id="live-clock" class="clock-pill">🕒 Memuat Waktu...</div>
    </div>
    <script>
    function updateTime() {
        const now = new Date();
        const options = { 
            weekday: 'long', day: 'numeric', month: 'long', year: 'numeric',
            hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false 
        };
        const timeString = new Intl.DateTimeFormat('id-ID', options).format(now);
        const clockElement = document.getElementById('live-clock');
        if (clockElement) {
            clockElement.innerHTML = '🕒 ' + timeString;
        }
    }
    setInterval(updateTime, 1000);
    updateTime();
    </script>
    """, unsafe_allow_html=True)

# 4. Database Initialization
DATA_FILE = "tasks_fastech_v6.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Project", "Task", "Pic", "Deadline", "Status", "Timestamp"])

# --- HEADER ---
st.markdown("""
    <div class="premium-header">
        <h1>Fastech Architect | Dashboard Monitoring</h1>
        <p>Operational Control & Creative Management System</p>
    </div>
    """, unsafe_allow_html=True)

# --- PANEL TAMBAH TUGAS (Sekarang di Halaman Utama) ---
with st.expander("➕ KLIK DISINI UNTUK TAMBAH TUGAS BARU", expanded=False):
    st.markdown('<div class="add-task-container">', unsafe_allow_html=True)
    with st.form("main_task_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            p_name = st.text_input("Nama Proyek", placeholder="Contoh: Villa Sentul")
            p_pic = st.selectbox("Assign Ke (PIC)", ["Tim CS", "PIC / Owner", "Tim Drafter", "Other"])
        with col2:
            p_date = st.date_input("Deadline")
            p_task = st.text_input("Ringkasan Tugas", placeholder="Apa yang harus dikerjakan?")
        
        full_detail = st.text_area("Detail Pekerjaan Lengkap")
        
        if st.form_submit_button("Daftarkan Pekerjaan"):
            if p_name and p_task:
                new_row = pd.DataFrame([[p_name, full_detail, p_pic, str(p_date), "To Do", datetime.now().strftime("%d/%m/%Y %H:%M")]],
                                        columns=["Project", "Task", "Pic", "Deadline", "Status", "Timestamp"])
                df = load_data()
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.success("Tugas Berhasil Terdaftar!")
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- DASHBOARD STATS ---
df = load_data()
c1, c2, c3 = st.columns(3)
c1.metric("Total Project", len(df))
c2.metric("Sedang Jalan", len(df[df['Status'] != "Done"]))
c3.metric("Sudah Selesai", len(df[df['Status'] == "Done"]))

st.markdown("---")

# --- MONITORING LIST ---
tab_act, tab_done = st.tabs(["🚀 Pekerjaan Aktif", "📜 Arsip Pekerjaan"])

with tab_act:
    active = df[df['Status'] != "Done"]
    if not active.empty:
        for idx, row in active.iterrows():
            st.markdown(f"""
            <div style="background: white; padding: 25px; border: 1px solid #eee; border-radius: 15px; margin-bottom: 20px; border-left: 8px solid #004a99;">
                <h3 style="margin:0; color:#001f3f;">{row['Project']}</h3>
                <p style="color:#666;"><b>PIC:</b> {row['Pic']} | <b>Deadline:</b> {row['Deadline']}</p>
                <div style="background:#f9f9f9; padding:15px; border-radius:10px; border:1px solid #f0f0f0; color:#333;">{row['Task']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Kontrol Aksi
            col_s, col_d = st.columns([4, 1])
            new_st = col_s.select_slider("Update Progres", options=["To Do", "In Progress", "Done"], value=row['Status'], key=f"s_{idx}")
            if col_d.button("🗑️ Hapus", key=f"d_{idx}"):
                df = df.drop(idx)
                df.to_csv(DATA_FILE, index=False)
                st.rerun()
            
            if new_st != row['Status']:
                df.at[idx, 'Status'] = new_st
                df.to_csv(DATA_FILE, index=False)
                st.rerun()
    else:
        st.info("Belum ada tugas yang berjalan.")

with tab_done:
    done = df[df['Status'] == "Done"]
    if not done.empty:
        st.dataframe(done, use_container_width=True)
