import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pencari Data Excel", page_icon="🔍", layout="centered")

st.title("🔍 Web Tool Pencari Data Excel")
st.write("Unggah file Excel Anda, lalu ketik kata kunci yang ingin dicari.")

uploaded_file = st.file_uploader("Upload File Excel Anda (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    # 1. Baca Excel dan bersihkan baris kosong
    df = pd.read_excel(uploaded_file).fillna("")
    df_clean = df[pd.to_numeric(df.iloc[:, 0], errors='coerce').notna()].copy()
    
    st.subheader("📋 Preview Data Excel (Sudah Dibersihkan)")
    st.dataframe(df_clean.head())

    # 2. Kotak input pencarian
    tanya = st.text_input("Ketik kata kunci (Contoh: Komarudin, RW 01, dll):")

    if tanya:
        # Cari kata kunci di seluruh kolom secara otomatis (Case-insensitive / tidak peduli huruf besar/kecil)
        mask = df_clean.astype(str).apply(lambda col: col.str.contains(tanya, case=False, na=False)).any(axis=1)
        hasil_df = df_clean[mask]
        
        if not hasil_df.empty:
            st.markdown("---")
            st.success(f"Ditemukan **{len(hasil_df)}** data yang cocok!")
            
            # Tampilkan hasil pencarian dalam bentuk tabel rapi
            st.subheader("📄 Detail Informasi:")
            st.dataframe(hasil_df)
        else:
            st.warning("Data tidak ditemukan. Coba ketik kata kunci lain.")
