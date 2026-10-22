
import fastf1
import pandas as pd

# Enable cache for faster data loading
fastf1.Cache.enable_cache("f1_cache")

def ingest_telemetry(year=2024, race="Monaco", driver="VER"):
    # Load race session
    session = fastf1.get_session(year, race, "R")
    session.load(telemetry=True, laps=True)

    # Get driver's lap data
    laps = session.laps.pick_drivers(driver)

    if laps.empty:
        print("No lap data found.")
        return None

    # Extract telemetry for each lap
    data = []

    for _, lap in laps.iterrows():
        try:
            telemetry = lap.get_telemetry()
            telemetry["LapNumber"] = lap["LapNumber"]
            telemetry["Compound"] = lap["Compound"]
            telemetry["TyreLife"] = lap["TyreLife"]
            data.append(telemetry)
        except Exception:
            continue

    if not data:
        print("No telemetry collected.")
        return None

    # Combine and clean telemetry
    df = pd.concat(data, ignore_index=True)
    df = df.dropna(subset=["Speed", "Throttle", "Brake"])
    df = df.drop_duplicates()

    # Save processed dataset
    df.to_csv("f1_telemetry.csv", index=False)
    print(f"Saved {len(df)} telemetry records.")

    return df

# Run pipeline
df = ingest_telemetry()
if df is not None:
    print(df.head())
