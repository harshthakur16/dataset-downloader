#!/usr/bin/env python3
import os
import io
import sys
import argparse
import requests
import pandas as pd
from dotenv import load_dotenv

from .utils import parseAdCreative, snakeToCamel

DEFAULT_API_BASE = "https://analytics.seekho.in/api/queries/41583/results.csv"

def fetchCsv(apiKey: str, apiBase: str, timeout: int = 60) -> str:
    url = f"{apiBase}?api_key={apiKey}"
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.text

def renameColumnsCamel(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns=lambda c: snakeToCamel(c))

def main():
    load_dotenv()  # Loads .env if present

    parser = argparse.ArgumentParser(description="Download and refine Seekho analytics CSV.")
    parser.add_argument("--apiKey", dest="apiKey", default=os.getenv("SEEKHO_API_KEY"),
                        help="API key for analytics.seekho.in (or set SEEKHO_API_KEY in .env).")
    parser.add_argument("--out", dest="outPath", default="dataset.csv",
                        help="Output CSV filename (default: dataset.csv)")
    parser.add_argument("--timeout", dest="timeout", type=int, default=60,
                        help="HTTP timeout seconds (default: 60)")
    parser.add_argument("--apiBase", dest="apiBase", default=os.getenv("API_BASE", DEFAULT_API_BASE),
                        help="Override base API URL (normally you don't need this).")

    args = parser.parse_args()

    if not args.apiKey:
        print("Error: provide --apiKey or set SEEKHO_API_KEY in .env", file=sys.stderr)
        sys.exit(1)

    try:
        csvText = fetchCsv(args.apiKey, args.apiBase, timeout=args.timeout)
    except requests.HTTPError as e:
        print(f"HTTP error: {e} | Response: {getattr(e.response, 'text', '')}", file=sys.stderr)
        sys.exit(2)
    except requests.RequestException as e:
        print(f"Network error: {e}", file=sys.stderr)
        sys.exit(3)

    # Load CSV to DataFrame
    df = pd.read_csv(io.StringIO(csvText))

    # Preserve original ad_creative and then build adCreative from it
    if "ad_creative" not in df.columns:
        print("Error: 'ad_creative' column not found in the downloaded CSV.", file=sys.stderr)
        sys.exit(4)

    df["adCreativeOriginal"] = df["ad_creative"].astype(str)

    # Parse new fields from ad_creative
    parsedRows = df["ad_creative"].astype(str).apply(parseAdCreative)
    parsedDf = pd.DataFrame(list(parsedRows.values))

    # Convert all column names to camelCase (including CSV originals)
    df = df.rename(columns=lambda c: "adCreative" if c == "ad_creative" else snakeToCamel(c))

    # Join parsed fields
    refinedDf = pd.concat([df, parsedDf], axis=1)

    # Save to CSV
    refinedDf.to_csv(args.outPath, index=False, encoding="utf-8")
    print(f"Saved refined CSV to {args.outPath} (rows: {len(refinedDf)}, cols: {len(refinedDf.columns)})")

if __name__ == "__main__":
    main()
