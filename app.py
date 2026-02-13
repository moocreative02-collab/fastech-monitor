import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. Konfigurasi Halaman
st.set_page_config(page_title="FASTECH | Executive Dashboard", layout="wide", page_icon="🏗️")

# 2. CSS "Premium Architect" - Kunci Warna agar Tidak Putih-di-Putih
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');

    /* Reset Dasar */
    .stApp {
        background-color: #fcfcfc !important;
        color: #1a1a1a !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Tulisan Global agar Selalu Terlihat */
    h1, h2, h3, p, span, label, div {
        color: #1a1a1a !important;
    }

    /* Header Biru Gelap (Executive Look) */
    .header-box {
        background: #001f3f;
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        border-bottom: 5px solid #ffd700;
    }
    .header-box h1 { color: #ffffff !important; margin: 0; font-weight: 800; }
    .header-box p { color: #cccccc !important; margin: 5px 0 0 0; }

    /* Card Statistik */
    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    /* Sidebar - Dibuat Gelap agar Kontras */
    section[data-testid="stSidebar"] {
        background-color: #001f3f !important;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] label {
        color: #ffffff !important;
    }

    /* Jam Real-time */
    .clock-container {
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        font-size: 20px;
        color: #001f3f !important;
        background: #ffd700;
        padding: 5px 15px;
        border-radius: 20px;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Real-time Clock Widget
st.markdown("""
    <div style="text-align: right; margin-bottom: 10px;">
        <div id="realtime-clock" class="clock-container">Memuat Waktu...</div>
    </div>
    <script>
    function updateClock() {
        var now = new Date();
        var days = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'];
        var months = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'];
        
        var dateStr = days[now.getDay()] + ', ' + now.getDate() + ' ' + months[now.getMonth()] + ' ' + now.getFullYear();
        var timeStr = now.getHours().toString().padStart(2, '0') + ':' + 
                      now.getMinutes().toString().padStart(2, '0') + ':' + 
                      now.getSeconds().toString().padStart(2, '0');
        
        document.getElementById('realtime-clock').innerHTML = dateStr + ' | ' + timeStr;
    }
    setInterval(updateClock, 1000);
    updateClock();
    </script>
    """, unsafe_allow_html=True)

# 4. Database Logic
DATA_FILE = "tasks_fastech_pro.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Project", "Task", "Pic", "Deadline", "Status", "Timestamp"])

# --- HEADER ---
st.markdown("""
    <div class="header-box">
        <h1>TIM CREATIVE FASTECH ARCHITECT</h1>
        <p>Dashboard Monitoring & Project Control v3.0</p>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    st.markdown("---")
    st.header("➕ Tambah Tugas")
    with st.form("input_form", clear_on_submit=True):
        p_name = st.text_input("Nama Proyek")
        p_task = st.text_area("Detail Pekerjaan")
        # List PIC sesuai permintaan
        p_pic = st.selectbox("Assign Ke", ["Tim CS", "PIC / Owner", "Tim Drafter", "Other"])
        p_date = st.date_input("Deadline")
        
        if st.form_submit_button("Simpan"):
            if p_name and p_task:
                new_entry = pd.DataFrame([[p_name, p_task, p_pic, str(p_date), "To Do", datetime.now().strftime("%d/%m/%Y %H:%M")]],
                                        columns=["Project", "Task", "Pic", "Deadline", "Status", "Timestamp"])
                df = load_data()
                df = pd.concat([df, new_entry], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.success("Tugas Ditambahkan!")
                st.rerun()

# --- MAIN DASHBOARD ---
df = load_data()

# Quick Statistics
c1, c2, c3 = st.columns(3)
c1.metric("📌 Total Task", len(df))
c2.metric("🚀 Active", len(df[df['Status'] != "Done"]))
c3.metric("✅ Completed", len(df[df['Status'] == "Done"]))

st.markdown("<br>", unsafe_allow_html=True)

# Tabs
tab1, tab2 = st.tabs(["🔥 Pekerjaan Berjalan", "📂 Arsip Selesai"])

with tab1:
    active = df[df['Status'] != "Done"]
    if not active.empty:
        for idx, row in active.iterrows():
            with st.expander(f"📝 {row['Project']} - {row['Pic']}"):
                st.write(f"**Brief:** {row['Task']}")
                st.caption(f"Deadline: {row['Deadline']} | Dibuat: {row['Timestamp']}")
                
                # Update Status
                status_list = ["To Do", "In Progress", "Done"]
                new_status = st.select_slider("Update Progress", options=status_list, 
                                             value=row['Status'], key=f"slide_{idx}")
                
                if new_status != row['Status']:
                    df.at[idx, 'Status'] = new_status
                    df.to_csv(DATA_FILE, index=False)
                    st.rerun()
                
                if st.button("🗑️ Hapus", key=f"del_{idx}"):
                    df = df.drop(idx)
                    df.to_csv(DATA_FILE, index=False)
                    st.rerun()
    else:
        st.info("Belum ada tugas aktif.")

with tab2:
    done = df[df['Status'] == "Done"]
    if not done.empty:
        st.dataframe(done, use_container_width=True)
    else:
        st.caption("Belum ada riwayat tugas selesai.")
