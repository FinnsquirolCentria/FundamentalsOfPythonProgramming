# Copyright (c) 2026 Ville Heikkiniemi, Luka Hietala, Luukas Kola
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

# Modified by nnn according to given task

"""
A program that prints reservation information according to requirements

The data structure and example data record:

reservationId | name | email | phone | reservationDate | reservationTime | durationHours | price | confirmed | reservedResource | createdAt
------------------------------------------------------------------------
201 | Moomin Valley | moomin@whitevalley.org | 0509876543 | 2025-11-12 | 09:00:00 | 2 | 18.50 | True | Forest Area 1 | 2025-08-12 14:33:20
int | str | str | str | date | time | int | float | bool | str | datetime

"""

from datetime import datetime


def convert_reservation_data(data: list) -> dict:
    """
    Convert data types to meet program requirements

    Parameters:
     data (list): Unconverted reservation -> 11 columns 

    Returns:
     converted (dict): Converted data types as dictionary
    """
    return {
        "id": int(data[0]),
        "name": str(data[1]),
        "email": str(data[2]),
        "phone": str(data[3]),
        "date": datetime.strptime(data[4], "%Y-%m-%d").date(),
        "time": datetime.strptime(data[5], "%H:%M").time(),
        "duration": int(data[6]),
        "price": float(data[7]),
        "confirmed": True if data[8].strip() == 'True' else False,
        "resource": str(data[9]),
        "created": datetime.strptime(str(data[10]).strip(), "%Y-%m-%d %H:%M:%S"),
    }


def fetch_reservations(reservation_file: str) -> list[dict]:
    """
    Reads reservations from a file and returns the reservations converted
    Does not include the header row

    Parameters:
     reservation_file (str): Name of the file containing the reservations

    Returns:
     reservations (list): Read and converted reservations as dictionaries
    """
    reservations = []
    with open(reservation_file, "r", encoding="utf-8") as f:
        for line in f:
            if len(line) > 1:
                fields = line.split("|")
                reservations.append(convert_reservation_data(fields))
    return reservations

def confirmed_reservations(reservations: list[dict]) -> None:
    """
    Print confirmed reservations

    Parameters:
     reservations (list): Reservations
    """
    for reservation in reservations:
        if reservation["confirmed"]: # If confirmed
            print(f'- {reservation["name"]}, {reservation["resource"]}, {reservation["date"].strftime("%d.%m.%Y")} at {reservation["time"].strftime("%H.%M")}')

def long_reservations(reservations : list[dict]) -> None:
    """
    Print long reservations

    Parameters:
     reservations (list): Reservations
    """
    for reservation in reservations:
        if reservation["duration"] >= 3: # If long
            print(f'- {reservation["name"]}, {reservation["date"].strftime("%d.%m.%Y")} at {reservation["time"].strftime("%H.%M")}, duration {reservation["duration"]} h, {reservation["resource"]}')


def confirmation_statuses(reservations: list[dict]) -> None:
    """
    Print confirmation statuses

    Parameters:
     reservations (list): Reservations
    """
    for reservation in reservations:
        name : str = reservation["name"]
        confirmed : bool = reservation["confirmed"]

        print(f'{name} → {"Confirmed" if confirmed else "NOT Confirmed"}')

def confirmation_summary(reservations: list[dict]) -> None:
    """
    Print confirmation summary

    Parameters:
     reservations (list): Reservations
    """
    confirmed : int = len([x for x in reservations if x["confirmed"]])
    print(f'- Confirmed reservations: {confirmed} pcs\n- Not confirmed reservations: {len(reservations) - confirmed} pcs')

def total_revenue(reservations: list[dict]) -> None:
    """
    Print total revenue

    Parameters:
     reservations (list): Reservations
    """
    revenue : float = sum(x["duration"] * x["price"] for x in reservations if x["confirmed"])
    print(f'Total revenue from confirmed reservations: {revenue:.2f} €'.replace('.', ','))

def main():
    """
    Prints reservation information according to requirements
    Reservation-specific printing is done in functions
    """
    reservations = fetch_reservations("reservations.txt")
    print("1) Confirmed Reservations")
    confirmed_reservations(reservations)
    print("2) Long Reservations (≥ 3 h)")
    long_reservations(reservations)
    print("3) Reservation Confirmation Status")
    confirmation_statuses(reservations)
    print("4) Confirmation Summary")
    confirmation_summary(reservations)
    print("5) Total Revenue from Confirmed Reservations")
    total_revenue(reservations)

if __name__ == "__main__":
    main()
