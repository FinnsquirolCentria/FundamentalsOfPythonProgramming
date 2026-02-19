# Copyright (c) 2025 Diego Finnilä
# License: MIT

import csv
from datetime import datetime, date
from typing import List, Dict, Any, TextIO

def read_data(filename: str) -> List[Dict[str, Any]]:
    """
    Reads and parses a CSV file with energy consumption and weather data.
    
    Parameters:
        filename: Path to the CSV file.
    
    Returns:
        A list of dictionaries containing parsed data with keys:
        - 'timestamp' (datetime): Full date and time
        - 'date' (date): Date only
        - 'consumption' (float): Net consumption in kWh
        - 'production' (float): Net production in kWh
        - 'temperature' (float): Daily average temperature in °C
    
    Raises:
        FileNotFoundError: If the CSV file does not exist.
        KeyError: If expected CSV columns are missing.
        ValueError: If data conversion fails.
    """
    rows: List[Dict[str, Any]] = []

    with open(filename, encoding="utf-8") as f:
        reader: csv.DictReader = csv.DictReader(f, delimiter=";")

        for row in reader:
            dt: datetime = datetime.fromisoformat(row["Time"])

            # Convert comma decimals to floats
            cons: float = float(row[" Consumption (net) kWh"].replace(",", "."))
            prod: float = float(row[" Production (net) kWh"].replace(",", "."))
            temp: float = float(row[" Daily average temperature"].replace(",", "."))

            rows.append({
                "timestamp": dt,
                "date": dt.date(),
                "consumption": cons,
                "production": prod,
                "temperature": temp
            })

    return rows

def format_kwh(value: float) -> str:
    """
    Formats a kWh value with Finnish comma decimal formatting.
    
    Parameters:
        value: Numeric value to format.
    
    Returns:
        Formatted string with 2 decimal places and comma as decimal separator.
    """
    return f"{value:.2f}".replace(".", ",")


def format_temp(value: float) -> str:
    """
    Formats a temperature value with Finnish comma decimal formatting.
    
    Parameters:
        value: Temperature value in degrees Celsius.
    
    Returns:
        Formatted string with 2 decimal places and comma as decimal separator.
    """
    return f"{value:.2f}".replace(".", ",")


def format_date(d: date) -> str:
    """
    Formats a date object in Finnish date format.
    
    Parameters:
        d: Date object to format.
    
    Returns:
        Formatted date string in dd.mm.yyyy format.
    """
    return f"{d.day}.{d.month}.{d.year}"

def create_daily_report(data: List[Dict[str, Any]]) -> List[str]:
    """
    Creates an energy report for a user-specified date range.
    
    Parameters:
        data: List of parsed energy data dictionaries from read_data().
    
    Returns:
        A list of formatted report lines showing total consumption, production,
        and average temperature for the specified date range.
    
    Raises:
        ValueError: If date input format is invalid.
    """
    start_str: str = input("Enter start date (dd.mm.yyyy): ")
    end_str: str = input("Enter end date (dd.mm.yyyy): ")

    start_d: date = datetime.strptime(start_str, "%d.%m.%Y").date()
    end_d: date = datetime.strptime(end_str, "%d.%m.%Y").date()

    total_cons: float = 0.0
    total_prod: float = 0.0
    temps: List[float] = []

    for row in data:
        if start_d <= row["date"] <= end_d:
            total_cons += row["consumption"]
            total_prod += row["production"]
            temps.append(row["temperature"])

    avg_temp: float = sum(temps) / len(temps) if temps else 0.0

    lines: List[str] = []
    lines.append("-------------------------------------------")
    lines.append(f"Report for the period {start_str}-{end_str}")
    lines.append(f"Total consumption: {format_kwh(total_cons)} kWh")
    lines.append(f"Total production: {format_kwh(total_prod)} kWh")
    lines.append(f"Average temperature: {format_temp(avg_temp)} °C")

    return lines


def create_monthly_report(data: List[Dict[str, Any]]) -> List[str]:
    """
    Creates an energy report for a user-specified month.
    
    Parameters:
        data: List of parsed energy data dictionaries from read_data().
    
    Returns:
        A list of formatted report lines showing total consumption, production,
        and average temperature for the specified month.
    
    Raises:
        ValueError: If month input is not an integer or outside 1-12 range.
    """
    month_num: int = int(input("Enter month number (1-12): ").strip())

    total_cons: float = 0.0
    total_prod: float = 0.0
    temps: List[float] = []

    for row in data:
        if row["date"].month == month_num:
            total_cons += row["consumption"]
            total_prod += row["production"]
            temps.append(row["temperature"])

    avg_temp: float = sum(temps) / len(temps) if temps else 0.0

    month_names: List[str] = [
        "", "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    lines: List[str] = []
    lines.append("-------------------------------------------")
    lines.append(f"Report for the month: {month_names[month_num]}")
    lines.append(f"Total consumption: {format_kwh(total_cons)} kWh")
    lines.append(f"Total production: {format_kwh(total_prod)} kWh")
    lines.append(f"Average temperature: {format_temp(avg_temp)} °C")

    return lines


def create_yearly_report(data: List[Dict[str, Any]]) -> List[str]:
    """
    Creates an energy report for the entire year 2025.
    
    Parameters:
        data: List of parsed energy data dictionaries from read_data().
    
    Returns:
        A list of formatted report lines showing total annual consumption,
        production, and average temperature.
    """
    total_cons: float = sum(r["consumption"] for r in data)
    total_prod: float = sum(r["production"] for r in data)
    temps: List[float] = [r["temperature"] for r in data]
    avg_temp: float = sum(temps) / len(temps) if temps else 0.0

    lines: List[str] = []
    lines.append("-------------------------------------------")
    lines.append("Report for the year: 2025")
    lines.append(f"Total consumption: {format_kwh(total_cons)} kWh")
    lines.append(f"Total production: {format_kwh(total_prod)} kWh")
    lines.append(f"Average temperature: {format_temp(avg_temp)} °C")

    return lines

def print_report_to_console(lines: List[str]) -> None:
    """
    Displays report lines to the console.
    
    Parameters:
        lines: List of report text lines to display.
    
    Returns:
        None
    """
    for line in lines:
        print(line)


def write_report_to_file(lines: List[str]) -> None:
    """
    Writes report lines to a file named report.txt in the current directory.
    
    Parameters:
        lines: List of report text lines to write.
    
    Returns:
        None
    """
    with open("report.txt", "w", encoding="utf-8") as f:
        file_handle: TextIO = f
        file_handle.write("\n".join(lines))
    print("Report written to report.txt")

def show_main_menu() -> str:
    """
    Displays the main menu and prompts the user for a choice.
    
    Returns:
        The user's menu selection as a string ("1", "2", "3", or "4").
    """
    print("Choose a report type:")
    print("1)Daily summary for a date range")
    print("2)Monthly summary for one month")
    print("3)Full year 2025 summary")
    print("4)Exit the program")
    return input("Your choice: ").strip()


def main() -> None:
    """
    Main entry point for the energy report application.
    
    Controls program flow including menu display, report generation,
    and user interaction. Handles errors and keyboard interrupts gracefully.
    
    Raises:
        FileNotFoundError: If the 2025.csv data file is not found.
    """
    try:
        data: List[Dict[str, Any]] = read_data("2025.csv")

        while True:
            choice: str = show_main_menu()

            if choice == "1":
                report: List[str] = create_daily_report(data)

            elif choice == "2":
                report: List[str] = create_monthly_report(data)

            elif choice == "3":
                report: List[str] = create_yearly_report(data)

            elif choice == "4":
                print("Program exited!")
                return

            else:
                print("That choice is not valid. Please select an option from 1 to 4.")
                continue

            print_report_to_console(report)

            print("\nWhat would you like to do next?")
            print("1)Write the report to the file report.txt")
            print("2)Create a new report")
            print("3)Exit")

            next_choice: str = input("Your choice: ").strip()

            if next_choice == "1":
                write_report_to_file(report)

            elif next_choice == "2":
                continue

            elif next_choice == "3":
                print("Program exited!")
                return

            else:
                print("That choice is not valid. Select an option from 1 to 3.")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")


if __name__ == "__main__":
    main()