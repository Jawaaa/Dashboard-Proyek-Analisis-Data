import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Memuat data
all_df = pd.read_csv("D:/Dashboard/all_data-Sewa-Sepeda.csv")

# Menggabungkan data
all_df = pd.merge(
    left=day_df,
    right=hour_df,
    how="left",
    left_on="dteday",
    right_on="dteday"
)

# Sidebar untuk filter
with st.sidebar:
    st.image("https://raw.githubusercontent.com/dicodingacademy/assets/raw/main/logo.png")
    season_filter = st.selectbox("Pilih Musim", ["Spring", "Summer", "Fall", "Winter"], index=0)
    year_filter = st.selectbox("Pilih Tahun", [0, 1], index=0, format_func=lambda x: "2011" if x == 0 else "2012")

# Filter data
filtered_df = all_df[(all_df["season_x"] == season_filter) & (all_df["yr_x"] == year_filter)]

# Agregasi data
agg_season = filtered_df.groupby("season_x").agg({
    "cnt_x": "sum",
    "casual_x": "mean",
    "registered_x": "mean"
}).reset_index()

agg_year = filtered_df.groupby("yr_x").agg({
    "cnt_x": "sum",
    "casual_x": "sum",
    "registered_x": "sum"
}).reset_index()

# Dashboard layout
st.title("Dashboard Penyewaan Sepeda 🚴‍♂️")
st.subheader(f"Musim: {season_filter} | Tahun: {'2011' if year_filter == 0 else '2012'}")

# Total Penyewaan
st.metric("Total Penyewaan", value=int(agg_season["cnt_x"].sum()))
st.metric("Rata-rata Casual", value=round(agg_season["casual_x"].mean(), 2))
st.metric("Rata-rata Terdaftar", value=round(agg_season["registered_x"].mean(), 2))

# Visualisasi Total Penyewaan per Tahun
st.subheader("Penyewaan Sepeda per Tahun")
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(data=agg_year, x="yr_x", y="cnt_x", palette="Blues", ax=ax)
ax.set_title("Total Penyewaan Sepeda per Tahun", fontsize=16)
ax.set_xlabel("Tahun")
ax.set_ylabel("Total Penyewaan")
ax.set_xticks([0, 1])
ax.set_xticklabels(["2011", "2012"])
st.pyplot(fig)

# Penyewaan Berdasarkan Musim
st.subheader("Penyewaan Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(data=agg_season, x="season_x", y="cnt_x", palette="viridis", ax=ax)
ax.set_title("Total Penyewaan Sepeda per Musim", fontsize=16)
ax.set_xlabel("Musim")
ax.set_ylabel("Total Penyewaan")
st.pyplot(fig)

# Detail Pengguna
st.subheader("Detail Pengguna")
col1, col2 = st.columns(2)
with col1:
    st.metric("Rata-rata Casual", value=round(agg_season["casual_x"].mean(), 2))
with col2:
    st.metric("Rata-rata Terdaftar", value=round(agg_season["registered_x"].mean(), 2))

# Footer
st.caption("Data diperoleh dari dataset penyewaan sepeda harian dan tiap jam. © Dicoding 2023")
