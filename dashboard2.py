import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns

# STEP 1: Persiapkan DataFrame
st.title("Dashboard Sewa Sepeda")
st.sidebar.header("Filter")

# Load datasets
day_df = pd.read_csv("https://raw.githubusercontent.com/Jawaaa/Dataset-Proyek-Data-Scient/refs/heads/main/day.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/Jawaaa/Dataset-Proyek-Data-Scient/refs/heads/main/hour.csv")

# Periksa data
day_df.drop_duplicates(inplace=True)
hour_df.drop_duplicates(inplace=True)

# Tambahkan kolom "month" ke day_df
day_df["month"] = pd.to_datetime(day_df["dteday"]).dt.month

# STEP 2: Filter Sidebar
year_filter = st.sidebar.selectbox("Pilih Tahun", options=[0, 1], format_func=lambda x: "2011" if x == 0 else "2012")
season_filter = st.sidebar.selectbox("Pilih Musim", options=[1, 2, 3, 4], format_func=lambda x: ["Spring", "Summer", "Fall", "Winter"][x - 1])

filtered_data = day_df[(day_df["yr"] == year_filter) & (day_df["season"] == season_filter)]

# STEP 3: Visualisasi 1 - Pola Penyewaan Sepeda Bulanan
monthly_data = day_df.groupby(["month", "yr"]).agg({"casual": "mean", "registered": "mean"}).reset_index()

st.subheader("Pola Perubahan Penyewaan Sepeda Bulanan")
fig, ax = plt.subplots(figsize=(12, 7))

# Plot pengguna casual
sns.lineplot(
    x="month", 
    y="casual", 
    data=monthly_data[monthly_data["yr"] == 0], 
    marker="o", 
    label="Casual 2011", 
    color="red", 
    ax=ax
)
sns.lineplot(
    x="month", 
    y="casual", 
    data=monthly_data[monthly_data["yr"] == 1], 
    marker="o", 
    label="Casual 2012", 
    color="orange", 
    ax=ax
)

# Plot pengguna registered
sns.lineplot(
    x="month", 
    y="registered", 
    data=monthly_data[monthly_data["yr"] == 0], 
    marker="o", 
    label="Registered 2011", 
    color="blue", 
    ax=ax
)
sns.lineplot(
    x="month", 
    y="registered", 
    data=monthly_data[monthly_data["yr"] == 1], 
    marker="o", 
    label="Registered 2012", 
    color="green", 
    ax=ax
)

# Detil pada plot
ax.set_title("Pola Perubahan Penyewaan Sepeda Bulanan\n(Casual vs Registered, Tahun 2011 dan 2012)", fontsize=14)
ax.set_xlabel("Bulan", fontsize=12)
ax.set_ylabel("Rata-rata Penyewaan Sepeda", fontsize=12)
ax.set_xticks(np.arange(1, 13))
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
ax.legend(title="Kategori Pengguna dan Tahun")
ax.grid(alpha=0.3)

st.pyplot(fig)

# STEP 4: Visualisasi 2 - Rata-rata Penyewaan Sepeda Berdasarkan Musim
season_avg = day_df.groupby("season").agg({"cnt": "mean"}).reset_index()
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
season_avg["season"] = season_avg["season"].map(season_mapping)

st.subheader("Rata-rata Penyewaan Sepeda Harian Berdasarkan Musim")
fig2, ax2 = plt.subplots(figsize=(8, 6))

sns.barplot(x="season", y="cnt", data=season_avg, palette="Blues_d", ax=ax2)
ax2.set_title("Rata-rata Jumlah Penyewaan Sepeda Harian Berdasarkan Musim (2011-2012)", fontsize=14)
ax2.set_xlabel("Musim", fontsize=12)
ax2.set_ylabel("Rata-rata Penyewaan Sepeda", fontsize=12)
ax2.grid(alpha=0.3)

st.pyplot(fig2)

# STEP 5: Ekspor Data Gabungan
st.sidebar.download_button("Download Data Gabungan", data=day_df.to_csv(index=False), file_name="data_sewa_sepeda.csv")
