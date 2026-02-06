"""
Utility functions for API Key Checker
"""

from pathlib import Path
from tabulate import tabulate


def load_keys_from_file(filepath):
    """Load API keys from a text file (one per line)"""
    try:
        with open(filepath, "r") as f:
            keys = [line.strip() for line in f if line.strip()]
        return keys
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return []


def print_report(results):
    """Print validation results in a formatted table"""
    if not results:
        print("❌ No results to display")
        return

    # Prepare table data
    table_data = []
    for result in results:
        status_icon = "✅" if result["is_active"] else "❌"
        table_data.append([
            status_icon,
            result["api_type"].upper(),
            result["key_preview"],
            "Valid Format" if result["format_valid"] else "Invalid Format",
            result.get("error") or "N/A",
        ])

    headers = ["Status", "API Type", "Key Preview", "Format", "Details"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

    # Summary
    valid_count = sum(1 for r in results if r["is_active"])
    total_count = len(results)
    print(f"\n📈 Summary: {valid_count}/{total_count} keys are valid and active")
