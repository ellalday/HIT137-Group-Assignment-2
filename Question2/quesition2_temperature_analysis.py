import os
import pandas as pd
import numpy as np
# load and analyse temperature data from multiple csv files
TEMPERATURES_FOLDER = "temperatures"

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

SEASONS = {
    "Summer": ["December", "January", "February"],
    "Autumn": ["March", "April", "May"],
    "Winter": ["June", "July", "August"],
    "Spring": ["September", "October", "November"]
}

# read and combine all CSV files in the temeratures folder into a single Data Frame
def load_all_data():
    frames = []
    if not os.path.isdir(TEMPERATURES_FOLDER):
        raise FileNotFoundError(f"Folder '{TEMPERATURES_FOLDER}' not found.")

    for file in os.listdir(TEMPERATURES_FOLDER):
        if file.lower().endswith(".csv"):
            path = os.path.join(TEMPERATURES_FOLDER, file)
            df = pd.read_csv(path)
            frames.append(df)

    if not frames:
        raise FileNotFoundError(f"No CSV files found in '{TEMPERATURES_FOLDER}'.")

    return pd.concat(frames, ignore_index=True)


def calculate_seasonal_averages(df):
    with open("average_temp.txt", "w", encoding="utf-8") as f:
        for season, months in SEASONS.items():
            # flatten month columns so seasonal averages are calculated across all stations and years
            temps = pd.to_numeric(df[months].values.flatten(), errors="coerce")
            temps = temps[~np.isnan(temps)]
            if len(temps) == 0:
                f.write(f"{season}: No data\n")
            else:
                f.write(f"{season}: {np.mean(temps):.1f}°C\n")


def calculate_temperature_ranges(df):
    # Collect ALL temperatures for each station across ALL years
    station_temps = {}

    for _, row in df.iterrows():
        station = str(row["STATION_NAME"]).strip()

        values = pd.to_numeric(row[MONTHS], errors="coerce").to_numpy()
        values = values[~np.isnan(values)]

        if len(values) == 0:
            continue

        station_temps.setdefault(station, []).extend(values.tolist())

    if not station_temps:
        with open("largest_temp_range_station.txt", "w", encoding="utf-8") as f:
            f.write("No station data found.\n")
        return

    # Range per station = max(all) - min(all)
    station_ranges = {}
    for station, vals in station_temps.items():
        mn = float(np.min(vals))
        mx = float(np.max(vals))
        station_ranges[station] = (mx - mn, mx, mn)

    max_range = max(rng for rng, _, _ in station_ranges.values())

    with open("largest_temp_range_station.txt", "w", encoding="utf-8") as f:
        for station, (rng, mx, mn) in sorted(station_ranges.items(), key=lambda x: x[0].lower()):
            if np.isclose(rng, max_range):
                f.write(f"{station}: Range {rng:.1f}°C (Max: {mx:.1f}°C, Min: {mn:.1f}°C)\n")

# identify the most stable and most variable stations using standard deviation
def calculate_temperature_stability(df):
    station_temps = {}

    for _, row in df.iterrows():
        station = str(row["STATION_NAME"]).strip()

        values = pd.to_numeric(row[MONTHS], errors="coerce").to_numpy()
        values = values[~np.isnan(values)]

        if len(values) == 0:
            continue

        station_temps.setdefault(station, []).extend(values.tolist())

    # Need at least 2 values for meaningful std dev
    station_stds = {st: float(np.std(vals)) for st, vals in station_temps.items() if len(vals) > 1}

    with open("temperature_stability_stations.txt", "w", encoding="utf-8") as f:
        if not station_stds:
            f.write("Not enough data to calculate standard deviation.\n")
            return

        min_sd = min(station_stds.values())
        max_sd = max(station_stds.values())

        for st, sd in sorted(station_stds.items(), key=lambda x: x[0].lower()):
            if np.isclose(sd, min_sd):
                f.write(f"Most Stable: {st}: StdDev {sd:.1f}°C\n")
        for st, sd in sorted(station_stds.items(), key=lambda x: x[0].lower()):
            if np.isclose(sd, max_sd):
                f.write(f"Most Variable: {st}: StdDev {sd:.1f}°C\n")

# main program entry point
def main():
    df = load_all_data()

    # Quick column check so you get a clear error message if a CSV is different
    required = set(MONTHS + ["STATION_NAME"])
    missing = required - set(df.columns)
    if missing:
        raise KeyError(f"Missing expected columns in CSV data: {sorted(missing)}")

    calculate_seasonal_averages(df)
    calculate_temperature_ranges(df)
    calculate_temperature_stability(df)

    print("Question 2 analysis complete.")


if __name__ == "__main__":
    main()
