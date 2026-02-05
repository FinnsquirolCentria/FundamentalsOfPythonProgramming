import csv
from datetime import datetime, date
from typing import List, Dict, Any


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


def print_table(daily: Dict[date, Dict[str, List[float]]]) -> None:
    """Prints the daily totals in a formatted table."""
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    print("Week 42 - Electricity Report (kWh)\n")
    print("Day          Date        Consumption (kWh)      Production (kWh)")
    print("           (dd.mm.yyyy)  v1    | v2   | v3           v1   |  v2  | v3")
    print("-" * 70)

    for d in sorted(daily.keys()):
        day_name = days[d.weekday()]
        date_str = d.strftime("%d.%m.%Y")

        cons = daily[d]["cons"]
        prod = daily[d]["prod"]

        cons_str = " | ".join(format_kwh(v) for v in cons)
        prod_str = " | ".join(format_kwh(v) for v in prod)

        print(f"{day_name:<12} {date_str:<11} {cons_str:<27} {prod_str}")


def main() -> None:
    """Main function: reads data, computes daily totals, and prints the report."""
    filename = "week42.csv"
    rows = read_data(filename)
    daily_totals = compute_daily_totals(rows)
    print_table(daily_totals)


if __name__ == "__main__":
    main()
