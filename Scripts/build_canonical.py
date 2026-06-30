from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]

RAW_PATH = BASE_DIR / "Stage 0 - Raw" / "Raw_blood_tests.csv"
OUT_DIR = BASE_DIR / "Stage 1 - Canonical"
OUT_PATH = OUT_DIR / "biomarker_results.csv"


"""
BIOMARKER_UNITS = {
    "Vitamin_D": "nmol/L",
    "B12": "pmol/L",
    "Testosterone": "nmol/L",
    "Omega-3 Index": "%",
}
"""
RANGES_PATH = BASE_DIR / "config" / "biomarker_ranges.csv"



def main():
    df = pd.read_csv(RAW_PATH)

    ranges_df = pd.read_csv(RANGES_PATH)

    unit_map = dict(
        zip(
            ranges_df["biomarker_code"],
            ranges_df["unit"]
        )
    )

    df["test_date"] = pd.to_datetime(df["test_date"], dayfirst=True).dt.date

    biomarker_cols = [col for col in df.columns if col not in ["test_date", "provider"]]

    canonical = df.melt(
        id_vars=["test_date", "provider"],
        value_vars=biomarker_cols,
        var_name="biomarker_code",
        value_name="value",
    )

    canonical = canonical.dropna(subset=["value"])
    canonical["biomarker_name"] = canonical["biomarker_code"].str.replace("_", " ")
    canonical["biomarker_name"] = canonical["biomarker_name"].str.title()

    canonical["biomarker_code"] = canonical["biomarker_code"].str.lower()
    canonical["unit"] = canonical["biomarker_code"].map(unit_map)

    canonical["source_file"] = RAW_PATH.name
    canonical = canonical.sort_values(["biomarker_code", "test_date"])

    canonical = canonical[
        [
            "test_date",
            "provider",
            "biomarker_code",
            "biomarker_name",
            "value",
            "unit",
            "source_file",
        ]
    ]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    canonical.to_csv(OUT_PATH, index=False)

    print(f"Read: {RAW_PATH}")
    print(f"Wrote: {OUT_PATH}")
    print(f"Rows: {len(canonical)}")

    #print(biomarker_cols)

if __name__ == "__main__":
    main()