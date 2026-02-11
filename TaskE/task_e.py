# Copyright (c) 2026 Ville Heikkiniemi, Luka Hietala, Luukas Kola
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

# Modified by nnn according to given task
import csv
from datetime import datetime, date
from typing import List, Dict, Any
from pathlib import Path


def read_data(filename: str) -> List[Dict[str, Any]]:
    """Reads the CSV file and returns the rows in a suitable structure."""
    rows: List[Dict[str, Any]] = []

    with open(filename, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")

        for row in reader:
            ts = datetime.fromisoformat(row["Time"])

            consumption = [int(row[f"Consumption phase {i+1} Wh"]) for i in range(3)]
            production = [int(row[f"Production phase {i+1} Wh"]) for i in range(3)]

            rows.append(
                {
                    "timestamp": ts,
                    "date": ts.date(),
                    "consumption": consumption,
                    "production": production,
                }
            )

    return rows


def compute_daily_totals(rows: List[Dict[str, Any]]) -> Dict[date, Dict[str, List[float]]]:
    """Groups hourly CSV rows by date and converts consumption and production into kWh."""
    daily: Dict[date, Dict[str, List[float]]] = {}

    for entry in rows:
        d = entry["date"]

        if d not in daily:
            daily[d] = {
                "cons": [0.0, 0.0, 0.0],
                "prod": [0.0, 0.0, 0.0],
            }

        for i in range(3):
            daily[d]["cons"][i] += entry["consumption"][i] / 1000.0
            daily[d]["prod"][i] += entry["production"][i] / 1000.0

    return daily


def format_kwh(value: float) -> str:
    return f"{value:.2f}".replace(".", ",")


def generate_table_text(week_number: int, daily: Dict[date, Dict[str, List[float]]]) -> str:
    """Returns the formatted weekly table text."""
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    lines: List[str] = []
    lines.append(f"Week {week_number} - Electricity Report (kWh)\n")
    lines.append("Day          Date        Consumption (kWh)      Production (kWh)")
    lines.append("           (dd.mm.yyyy)  v1    | v2   | v3           v1   |  v2  | v3")
    lines.append("-" * 70)

    for d in sorted(daily.keys()):
        day_name = days[d.weekday()]
        date_str = d.strftime("%d.%m.%Y")

        cons = daily[d]["cons"]
        prod = daily[d]["prod"]

        cons_str = " | ".join(format_kwh(v) for v in cons)
        prod_str = " | ".join(format_kwh(v) for v in prod)

        lines.append(f"{day_name:<12} {date_str:<11} {cons_str:<27} {prod_str}")

    lines.append("\n")
    return "\n".join(lines)


def main() -> None:
    """Reads all weeks.csv files, generates all tables, and writes them to summary.txt."""
    csv_files = sorted(Path(".").glob("week*.csv"))

    all_text: List[str] = []

    for csv_path in csv_files:
        week_digits = "".join(c for c in csv_path.stem if c.isdigit())
        week_number = int(week_digits) if week_digits.isdigit() else 0

        rows = read_data(str(csv_path))
        daily_totals = compute_daily_totals(rows)
        week_text = generate_table_text(week_number, daily_totals)

        all_text.append(week_text)

    with open("summary.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_text))

    print("summary.txt created")


if __name__ == "__main__":
    main()