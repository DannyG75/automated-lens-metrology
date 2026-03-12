#!/usr/bin/env python3
"""
generate_index.py
-----------------
Scans the datasheets/ folder for PDF files and writes datasheets/index.json.
Run this from the ROOT of your repo before committing and pushing to GitHub.

Usage:
    python generate_index.py

Output:
    datasheets/index.json   (overwritten each run)
"""

import os
import json
from datetime import datetime, timezone

DATASHEETS_DIR = os.path.join(os.path.dirname(__file__), "datasheets")
OUTPUT_FILE    = os.path.join(DATASHEETS_DIR, "index.json")


def human_size(num_bytes: int) -> str:
    """Convert bytes to a readable string e.g. '1.2 MB'."""
    for unit in ("B", "KB", "MB", "GB"):
        if num_bytes < 1024:
            return f"{num_bytes:.1f} {unit}" if unit != "B" else f"{num_bytes} B"
        num_bytes /= 1024
    return f"{num_bytes:.1f} GB"


def main():
    if not os.path.isdir(DATASHEETS_DIR):
        print(f"Creating directory: {DATASHEETS_DIR}")
        os.makedirs(DATASHEETS_DIR)

    pdfs = [f for f in os.listdir(DATASHEETS_DIR) if f.lower().endswith(".pdf")]

    if not pdfs:
        print("No PDF files found in datasheets/ — index.json will be empty.")

    entries = []
    for filename in pdfs:
        filepath = os.path.join(DATASHEETS_DIR, filename)
        stat     = os.stat(filepath)

        # Use file modification time as the "uploaded" timestamp
        mtime_utc = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)

        entries.append({
            "filename": filename,
            "uploaded": mtime_utc.isoformat(),        # ISO-8601, e.g. "2025-03-12T14:30:00+00:00"
            "size":     human_size(stat.st_size),
        })

    # Sort newest first
    entries.sort(key=lambda e: e["uploaded"], reverse=True)

    payload = {
        "generated": datetime.now(tz=timezone.utc).isoformat(),
        "count":     len(entries),
        "datasheets": entries,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"✓ Written {OUTPUT_FILE}  ({len(entries)} datasheet{'s' if len(entries) != 1 else ''})")
    for e in entries:
        print(f"  • {e['filename']}  {e['uploaded']}  {e['size']}")


if __name__ == "__main__":
    main()