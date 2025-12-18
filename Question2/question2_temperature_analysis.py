{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 Menlo-Regular;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import os\
import pandas as pd\
import numpy as np\
\
TEMPERATURES_FOLDER = "temperatures"\
\
SEASONS = \{\
    "Summer": [12, 1, 2],\
    "Autumn": [3, 4, 5],\
    "Winter": [6, 7, 8],\
    "Spring": [9, 10, 11]\
\}\
\
def load_all_data():\
    all_data = []\
    for file in os.listdir(TEMPERATURES_FOLDER):\
        if file.endswith(".csv"):\
            path = os.path.join(TEMPERATURES_FOLDER, file)\
            df = pd.read_csv(path)\
            all_data.append(df)\
    return pd.concat(all_data, ignore_index=True)\
\
def calculate_seasonal_averages(df):\
    df["Month"] = pd.to_datetime(df["Date"]).dt.month\
    results = \{\}\
\
    for season, months in SEASONS.items():\
        temps = df[df["Month"].isin(months)]["Temperature"]\
        results[season] = temps.mean()\
\
    with open("average_temp.txt", "w") as f:\
        for season, avg in results.items():\
            f.write(f"\{season\}: \{avg:.1f\}\'b0C\\n")\
\
def calculate_temperature_ranges(df):\
    grouped = df.groupby("Station")["Temperature"]\
    stats = grouped.agg(["min", "max"])\
    stats["range"] = stats["max"] - stats["min"]\
\
    max_range = stats["range"].max()\
    top_stations = stats[stats["range"] == max_range]\
\
    with open("largest_temp_range_station.txt", "w") as f:\
        for station, row in top_stations.iterrows():\
            f.write(\
                f"Station \{station\}: Range \{row['range']:.1f\}\'b0C "\
                f"(Max: \{row['max']:.1f\}\'b0C, Min: \{row['min']:.1f\}\'b0C)\\n"\
            )\
\
def calculate_temperature_stability(df):\
    std_dev = df.groupby("Station")["Temperature"].std()\
\
    min_std = std_dev.min()\
    max_std = std_dev.max()\
\
    with open("temperature_stability_stations.txt", "w") as f:\
        for station in std_dev[std_dev == min_std].index:\
            f.write(f"Most Stable: Station \{station\}: StdDev \{min_std:.1f\}\'b0C\\n")\
        for station in std_dev[std_dev == max_std].index:\
            f.write(f"Most Variable: Station \{station\}: StdDev \{max_std:.1f\}\'b0C\\n")\
\
def main():\
    df = load_all_data()\
    df = df.dropna(subset=["Temperature"])\
\
    calculate_seasonal_averages(df)\
    calculate_temperature_ranges(df)\
    calculate_temperature_stability(df)\
\
    print("Question 2 analysis complete.")\
\
if __name__ == "__main__":\
    main()\
}