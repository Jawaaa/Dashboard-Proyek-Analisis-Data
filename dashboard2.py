
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

# Gabungkan data
all_df = pd.merge(
    day_df, hour_df, 
    how="left", 
    left_on="dteday", 
    right_on="dteday"
)

# STEP 2: Buat Fungsi Helper untuk Data Agregasi
def aggregate_by_season(data):
    return data.groupby(["season_x", "season_y"]).agg({
        "cnt_x": "sum",
        "cnt_y": "sum"
    }).reset_index()

def aggregate_by_year(data):
    return data.groupby(["yr_x", "yr_y"]).agg({
        "cnt_x": "sum",
        "cnt_y": "sum",
        "registered_x": "sum",
        "registered_y": "sum",
        "casual_x": "sum",
        "casual_y": "sum"
    }).reset_index()

season_data = aggregate_by_season(all_df)
year_data = aggregate_by_year(all_df)

# STEP 3: Tambahkan Filter Sidebar
year_filter = st.sidebar.selectbox("Pilih Tahun", options=[0, 1], format_func=lambda x: "2011" if x == 0 else "2012")
season_filter = st.sidebar.selectbox("Pilih Musim", options=[1, 2, 3, 4], format_func=lambda x: ["Spring", "Summer", "Fall", "Winter"][x-1])

filtered_data = all_df[(all_df["yr_x"] == year_filter) & (all_df["season_x"] == season_filter)]

# STEP 4: Bangun Visualisasi
# jumlah Total Penyewaan sepeda rata2 per Musim
season_avg = day_df.groupby("season").agg({"cnt": "mean"}).reset_index()
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
season_avg["season"] = season_avg["season"].map(season_mapping)

plt.figure(figsize=(8, 6))
sns.barplot(x="season", y="cnt", data=season_avg, palette="Blues_d")
plt.title("Rata-rata Jumlah Penyewaan Sepeda Harian Berdasarkan Musim (2011-2012)", fontsize=14)
plt.xlabel("Musim", fontsize=12)
plt.ylabel("Rata-rata Penyewaan Sepeda", fontsize=12)
plt.grid(alpha=0.3)
plt.show()

# Total Penyewaan Sepeda per Tahun
day_df["month"] = pd.to_datetime(day_df["dteday"]).dt.month
monthly_data = day_df.groupby(["month", "yr"]).agg({"casual": "mean", "registered": "mean"}).reset_index()

plt.figure(figsize=(12, 7))

# Plot untuk pengguna casual
sns.lineplot(
    x="month", 
    y="casual", 
    data=monthly_data[monthly_data["yr"] == 0], 
    marker="o", 
    label="Casual 2011", 
    color="red"
)
sns.lineplot(
    x="month", 
    y="casual", 
    data=monthly_data[monthly_data["yr"] == 1], 
    marker="o", 
    label="Casual 2012", 
    color="orange"
)

# Plot untuk pengguna registered
sns.lineplot(
    x="month", 
    y="registered", 
    data=monthly_data[monthly_data["yr"] == 0], 
    marker="o", 
    label="Registered 2011", 
    color="blue"
)
sns.lineplot(
    x="month", 
    y="registered", 
    data=monthly_data[monthly_data["yr"] == 1], 
    marker="o", 
    label="Registered 2012", 
    color="green"
)

# Menambahkan detail pada plot
plt.title("Pola Perubahan Penyewaan Sepeda Bulanan\n(Casual vs Registered, Tahun 2011 dan 2012)", fontsize=14)
plt.xlabel("Bulan", fontsize=12)
plt.ylabel("Rata-rata Penyewaan Sepeda", fontsize=12)
plt.xticks(
    ticks=np.arange(1, 13), 
    labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
)
plt.legend(title="Kategori Pengguna dan Tahun")
plt.grid(alpha=0.3)
plt.show()



# STEP 5: Ekspor dan Tampilkan Data
st.sidebar.download_button("Download Data Gabungan", data=all_df.to_csv(index=False), file_name="all_data_sewa_sepeda.csv")
