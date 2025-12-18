import os
import pandas as pd
import numpy as np

# Folder containing CSV files
TEMPERATURES_FOLDER = "temperatures"

# Month columns exactly as they appear in your CSV files
MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Australian seasons
SEASONS = {
    "Summer": ["December", "January", "February"],
    "Autumn": ["March", "April", "May"],
    "Winter": ["June", "July", "August"],
    "Spring": ["September", "October", "November"]
}

def load_all_data():
    frames = []
    for file in os.listdir(TEMPERATURES_FOLDER):
        if file.endswith(".csv"):
            path = os.path.join(TEMPERATURES_FOLDER, file)
            df = pd.read_csv(path)
            frames.append(df)
    return pd.concat(frames, ignore_index=True)

def seasonal_averages(df):
    with open("average_temp.txt", "w") as f:
        for season, months in SEASONS.items():
            temps = pd.to_numeric(
                df[months].values.flatten(),
                errors="coerce"
            )
            temps = temps[~np.isnan(temps)]
            f.write(season + ": " + format(np.mean(temps), ".1f") + "C\n")

def temperature_range(df):
    station_ranges = {}

    for _, row in df.iterrows():
        station = row["STATION_NAME"]

        values = pd.to_numeric(
            row[MONTHS],
            errors="coerce"
        ).to_numpy()

        values = values[~np.isnan(values)]

        if len(values) == 0:
            continue

        min_temp = values.min()
        max_temp = values.max()
        temp_range = max_temp - min_temp

        if station not in station_ranges:
            station_ranges[station] = []

        station_ranges[station].append((min_temp, max_temp, temp_range))

    max_range = max(
        r[2] for records in station_ranges.values() for r in records
    )

    with open("largest_temp_range_station.txt", "w") as f:
        for station, records in station_ranges.items():
            for min_t, max_t, r in records:
                if r == max_range:
                    f.write(
                        "Station " + station +
                        ": Range " + format(r, ".1f") + "C " +
                        "(Max: " + format(max_t, ".1f") +
                        "C, Min: " + format(min_t, ".1f") + "C)\n"
                    )

def temperature_stability(df):
    station_values = {}

    for _, row in df.iterrows():
        station = row["STATION_NAME"]

        values = pd.to_numeric(
            row[MONTHS],
            errors="coerce"
        ).to_numpy()

        values = values[~np.isnan(values)]

        if station not in station_values:
            station_values[station] = []

        station_values[station].extend(values)

    stds = {s: np.std(v) for s, v in station_values.items()}

    min_std = min(stds.values())
    max_std = max(stds.values())

    with open("temperature_stability_stations.txt", "w") as f:
        for s, v in stds.items():
            if v == min_std:
                f.write(
                    "Most Stable: Station " + s +
                    ": StdDev " + format(v, ".1f") + "C\n"
                )
        for s, v in stds.items():
            if v == max_std:
                f.write(
                    "Most Variable: Station " + s +
                    ": StdDev " + format(v, ".1f") + "C\n"
                )

def main():
    df = load_all_data()
    seasonal_averages(df)
    temperature_range(df)
    temperature_stability(df)
    print("Question 2 analysis complete.")

main()
