import streamlit as st
import pandas as pd
from rapidfuzz import process, fuzz

st.set_page_config(page_title="Pencari Data Excel", page_icon="🔍", layout="centered")

st.title("🔍 Web Tool Pencari Data Excel")
st.write("Unggah file Excel Anda, lalu ketik kata kunci yang ingin dicari.")

uploaded_file = st.file_uploader("Upload File Excel Anda (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    # 1. Read Excel & ganti nilai NaN dengan teks kosong
    df = pd.read_excel(uploaded_file).fillna("")
    
    # 2. Hapus baris yang sama sekali tidak memiliki isi teks (baris header kosong)
    df = df[df.astype(str).apply(lambda row: "".join(row).strip() != "", axis=1)].reset_index(drop=True)
    
    st.subheader("📋 Preview Data Excel")
    st.dataframe(df.head())

    tanya = st.text_input("Ketik kata kunci (Nama, Wilayah, dll):")

    if tanya:
        # Gabungkan teks per baris untuk pencarian global
        daftar_teks = df.astype(str).apply(lambda x: " ".join(x), axis=1).tolist()
        
        # Cari menggunakan RapidFuzz
        hasil = process.extractOne(tanya, daftar_teks, scorer=fuzz.partial_ratio)
        
        if hasil and hasil[1] >= 50:
            idx_ditemukan = hasil[2]
            row_ditemukan = df.iloc[[idx_ditemukan]]
            
            st.markdown("---")
            st.success(f"Ditemukan Data yang Cocok! (Kemiripan: {hasil[1]:.0f}%)")
            
            # Tampilkan detail baris yang cocok dengan rapi
            st.subheader("📄 Detail Informasi:")
            st.dataframe(row_ditemukan)
        else:
            st.warning("Data tidak ditemukan. Coba ketik kata kunci lain.")
