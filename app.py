import streamlit as st
import pandas as pd
from datetime import date
import os

# 1. Konfigurasi Halaman & Tema
st.set_page_config(
    page_title="FASTECH ARCHITECT | Task Monitor",
    page_icon="🏗️",
    layout="wide"
)

# Custom CSS untuk tampilan lebih elegan
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #004a99;
        color: white;
    }
    .stExpander {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

DATA_FILE = "tasks_fastech_pro.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Project", "Task", "Pic", "Deadline", "Status"])

# --- SIDEBAR: Branding & Input ---
with st.sidebar:
    # FITUR LOGO: Pastikan ada file gambar bernama 'logo.png' di folder yang sama
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.title("🏗️ FASTECH")
        st.caption("Creative Monitoring System")
    
    st.divider()
    st.header("➕ Tambah Pekerjaan")
    with st.form("task_form", clear_on_submit=True):
        project = st.text_input("Nama Proyek", placeholder="Contoh: Villa Bali Project")
        task_desc = st.text_area("Detail Pekerjaan")
        
        # Update Daftar PIC sesuai request kamu
        pic_options = ["Tim CS", "PIC / Owner", "Tim Drafter", "Other"]
        pic = st.selectbox("Assign Ke (PIC)", pic_options)
        
        deadline = st.date_input("Deadline", date.today())
        submit = st.form_submit_button("Simpan ke Database")
        
        if submit:
            if project and task_desc:
                new_data = pd.DataFrame([[project, task_desc, pic, str(deadline), "To Do"]], 
                                        columns=["Project", "Task", "Pic", "Deadline", "Status"])
                df = load_data()
                df = pd.concat([df, new_data], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.success("Tugas berhasil dicatat!")
                st.rerun()
            else:
                st.error("Mohon isi Nama Proyek dan Detail.")

# --- MAIN AREA: Dashboard ---
st.title("📊 Monitoring Progres Tim")
df = load_data()

# Statistik Cepat
if not df.empty:
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Tugas", len(df))
    c2.metric("Sedang Jalan", len(df[df['Status'] == "In Progress"]))
    c3.metric("Selesai", len(df[df['Status'] == "Done"]))
    
    st.divider()

    # Tampilan List Tugas dengan Kolom
    for index, row in df.iterrows():
        # Warna status
        status_color = "🔵" if row['Status'] == "To Do" else "🟡" if row['Status'] == "In Progress" else "🟢"
        
        with st.expander(f"{status_color} {row['Project']} | {row['Pic']} (Deadline: {row['Deadline']})"):
            st.write(f"**Detail:** {row['Task']}")
            
            col_a, col_b, col_c = st.columns([2, 1, 1])
            
            # Ganti Status
            current_idx = ["To Do", "In Progress", "Done"].index(row['Status'])
            new_status = col_a.selectbox("Update Status", ["To Do", "In Progress", "Done"], 
                                         index=current_idx, key=f"st_{index}")
            
            if new_status != row['Status']:
                df.at[index, 'Status'] = new_status
                df.to_csv(DATA_FILE, index=False)
                st.rerun()

            if col_c.button("🗑️ Hapus", key=f"del_{index}"):
                df = df.drop(index)
                df.to_csv(DATA_FILE, index=False)
                st.rerun()
else:
    st.info("Dasbor kosong. Tambahkan tugas pertama kamu melalui sidebar di samping.")