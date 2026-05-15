"""
classify_parcels.py
────────────────────────────────────────────────────────────────────────────
Classifies 2,398 Tuscaloosa County property parcels using the Anthropic API.

Requirements:
    pip install anthropic pandas openpyxl

Usage:
    Place Marketing_List.xlsx in the same folder as this script, then:
    export ANTHROPIC_API_KEY="sk-ant-..."
    python classify_parcels.py

Output:
    Marketing_List_Classified.xlsx  — full results
    Marketing_List_checkpoint.xlsx  — rolling checkpoint (every 200 rows)
"""

import pandas as pd
import anthropic
import json
import time
import re
from pathlib import Path

INPUT_FILE  = "Marketing_List.xlsx"
OUTPUT_FILE = "Marketing_List_Classified.xlsx"
BATCH_SIZE  = 20
MAX_RETRIES = 3

SYSTEM_PROMPT = """You are a commercial real estate analyst specializing in property classification for Tuscaloosa County, Alabama.
You will receive a batch of property records and classify each one.

Return ONLY a JSON array (no markdown fences, no preamble) with one object per record in the same order as input.
Each object must have exactly these keys:
  "property_type" - choose one exact string from:
      Vacant Land, Single-Family Residential, Multifamily Residential,
      Commercial Retail, Commercial Office, Industrial/Warehouse, Self-Storage,
      Mining/Extraction, Agricultural, Institutional/Government, Religious,
      HOA/Common Area, Utility/Infrastructure, Marina/Recreational, Mixed Use, Unknown
  "business_use"  - 3-8 word description of likely use
  "confidence"    - HIGH, MEDIUM, or LOW

Use LOW confidence when:
  - Property address is only a road/highway name with no number
  - Owner is a generic LLC with no descriptive name clues
  - Data is ambiguous or largely missing

Use all three signals: owner name, property address, and owner mailing address."""


def build_prompt(records):
    lines = [f"{i+1}. Owner: {r['owner']} | Property: {r['prop_addr']} | Mailing: {r['owner_addr']}"
             for i, r in enumerate(records)]
    return "Classify these {} property records:\n\n".format(len(records)) + "\n".join(lines)


def classify_batch(client, records, attempt=0):
    try:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": build_prompt(records)}]
        )
        text = response.content[0].text.strip()
        text = re.sub(r"^```json\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        results = json.loads(text)
        if len(results) != len(records):
            raise ValueError("Got {} results for {} records".format(len(results), len(records)))
        return results
    except Exception as e:
        if attempt < MAX_RETRIES:
            wait = 2 ** attempt
            print("  Retry {}/{} in {}s - {}".format(attempt+1, MAX_RETRIES, wait, e), flush=True)
            time.sleep(wait)
            return classify_batch(client, records, attempt + 1)
        print("  FAILED after {} retries: {}".format(MAX_RETRIES, e), flush=True)
        return [{"property_type": "Unknown", "business_use": "Classification failed", "confidence": "LOW"}] * len(records)


def main():
    df = pd.read_excel(INPUT_FILE, sheet_name='CRSProspectingExport (1)', dtype=str).fillna("")
    client = anthropic.Anthropic()

    prop_types, bus_uses, confidences = [], [], []
    total     = len(df)
    n_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE

    print("Starting classification of {} records in {} batches...\n".format(total, n_batches), flush=True)

    for batch_num in range(n_batches):
        start = batch_num * BATCH_SIZE
        end   = min(start + BATCH_SIZE, total)
        chunk = df.iloc[start:end]

        records = [{
            "owner":      row["Owner Name 1"],
            "prop_addr":  "{} {}".format(row["Property Address"], row["Property Zip"]).strip(),
            "owner_addr": "{} {}".format(row["Owner Address"], row["Owner Zip"]).strip()
        } for _, row in chunk.iterrows()]

        print("Batch {:>3}/{}  rows {:>4}-{:<4}".format(batch_num+1, n_batches, start+1, end), flush=True)
        results = classify_batch(client, records)

        for r in results:
            prop_types.append(r.get("property_type", "Unknown"))
            bus_uses.append(r.get("business_use", ""))
            confidences.append(r.get("confidence", "LOW"))

        # Checkpoint every 10 batches (~200 rows)
        if (batch_num + 1) % 10 == 0:
            df_chk = df.iloc[:end].copy()
            df_chk["Property Type"] = prop_types
            df_chk["Business Use"]  = bus_uses
            df_chk["Confidence"]    = confidences
            chk_path = OUTPUT_FILE.replace(".xlsx", "_checkpoint.xlsx")
            df_chk.to_excel(chk_path, index=False)
            print("  Checkpoint saved -> {}".format(chk_path), flush=True)

        if batch_num < n_batches - 1:
            time.sleep(0.4)

    df["Property Type"] = prop_types
    df["Business Use"]  = bus_uses
    df["Confidence"]    = confidences
    df.to_excel(OUTPUT_FILE, index=False)

    print("\nDone! Saved -> {}\n".format(OUTPUT_FILE))
    print("--- Property Type breakdown ---")
    print(df["Property Type"].value_counts().to_string())
    print("\n--- Confidence breakdown ---")
    print(df["Confidence"].value_counts().to_string())


if __name__ == "__main__":
    main()
