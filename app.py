import streamlit as st
import pandas as pd
from rapidfuzz import process, fuzz

st.set_page_config(page_title="Pencari Data Excel", page_icon="🔍", layout="centered")

st.title("🔍 Web Tool Pencari Data Excel")
st.write("Unggah file Excel Anda, lalu ketik nama atau kata kunci yang dicari.")

uploaded_file = st.file_uploader("Upload File Excel Anda (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    # 1. Baca Excel
    df = pd.read_excel(uploaded_file)
    
    # 2. Hapus baris sub-header Excel (baris yang mengandung 'Laki-Laki' / 'Perempuan' / 'KTP' di header)
    # Mencari baris pertama yang memiliki Nomor/Angka di kolom pertama
    df_clean = df[pd.to_numeric(df.iloc[:, 0], errors='coerce').notna()].copy()
    df_clean = df_clean.fillna("-")
    
    st.subheader("📋 Preview Data Excel (Sudah Dibersihkan)")
    st.dataframe(df_clean.head())

    tanya = st.text_input("Ketik kata kunci (Contoh: Komarudin, Hartono, dll):")

    if tanya:
        # Cari kolom nama (kolom ke-3 / index 2)
        kolom_nama = df_clean.columns[2]
        daftar_nama = df_clean[kolom_nama].astype(str).tolist()
        
        # Pencarian Fuzzy menggunakan WRatio
        hasil = process.extractOne(tanya, daftar_nama, scorer=fuzz.WRatio)
        
        if hasil and hasil[1] >= 50:
            idx_ditemukan = hasil[2]
            row_ditemukan = df_clean.iloc[[idx_ditemukan]]
            
            st.markdown("---")
            st.success(f"Ditemukan: **{hasil[0]}** (Tingkat Kemiripan: {hasil[1]:.0f}%)")
            
            # Tampilkan detail informasi lengkap
            st.subheader("📄 Detail Informasi:")
            st.dataframe(row_ditemukan)
        else:
            st.warning("Data tidak ditemukan. Coba ketik kata kunci lain.")
