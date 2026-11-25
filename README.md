# Smart Parking Management System

A Python command-line application for managing parking spaces, recording vehicle entry and exit events, calculating parking fees, and viewing basic parking and revenue information.

The project is built with Python's standard library and uses plain-text files for data storage. This is my first Python project and it demonstrates functions, modules, dictionaries, loops, input validation, file handling, and basic object-oriented programming.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Parking Layout](#parking-layout)
- [Application Menu](#application-menu)
- [How It Works](#how-it-works)
- [Fee Calculation](#fee-calculation)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation and Setup](#installation-and-setup)
- [Running the Application](#running-the-application)
- [Data Storage](#data-storage)
- [Known Limitations](#known-limitations)
- [Possible Improvements](#possible-improvements)
- [License](#license)

## Overview

Smart Parking Management provides a simple way to manage a parking facility from a terminal. When a vehicle arrives, the application checks whether it is already parked and finds an available space. When the vehicle leaves, the application records the exit time, calculates the parking fee, and makes the space available again.

Parking activity is stored as an event log in `database.txt`. When the program starts, it reads this log to restore the occupied parking spaces.

## Features

- **Vehicle entry:** Register a vehicle using its license plate number and vehicle type.
- **Automatic space selection:** Assign the first available space in the configured parking lots.
- **Manual space selection:** Choose a specific available space by entering its slot ID.
- **Duplicate-entry check:** Prevent a vehicle that is already parked from being registered again.
- **Vehicle exit:** Find a parked vehicle, record its exit time, calculate its parking duration and fee, and release its space.
- **Parking status:** Display all spaces and indicate whether each one is occupied or available.
- **Vehicle search:** Search by license plate number and display the vehicle's latest recorded status and parking details.
- **Revenue report:** Display the number of completed parking sessions, total calculated revenue, and the number of vehicles currently parked.
- **Rate settings:** Change the rate saved in `fee_per_minut.txt` from the Settings menu.
- **File-based persistence:** Keep entry and exit records after the application closes and restore parking occupancy at the next startup.
- **License plate normalization:** Ignore spaces and hyphens and compare license plate numbers without case sensitivity.

## Parking Layout

The default parking facility contains **30 spaces** divided into three lots:

| Parking Lot | Space IDs | Capacity |
|---|---|---:|
| A Lot | `A01`–`A10` | 10 |
| B Lot | `B01`–`B10` | 10 |
| C Lot | `C01`–`C10` | 10 |
| **Total** | | **30** |

The layout is defined in `parking_lot_data.py`. Each space is represented by a dictionary value: `0` means available and `1` means occupied.

## Application Menu

When `main.py` starts, the following menu is displayed:

```text
     Smart Parking Management
1. Vehicle Entry
2. Vehicle Exit
3. View Parking Status
4. Search Vehicle
5. Parking Revenue Report
6. Settings
0. Exit
```

| Option | Description |
|---|---|
| `1` | Register a vehicle and assign a parking space. |
| `2` | Register a vehicle's exit and calculate its fee. |
| `3` | View the occupancy of all parking spaces. |
| `4` | Search for a vehicle by its license plate number. |
| `5` | View the parking revenue summary. |
| `6` | Update the parking rate stored in the settings file. |
| `0` | Close the application. |

## How It Works

### 1. Vehicle Entry

1. Enter the vehicle's license plate number and type.
2. The application normalizes the plate number and checks the event log to determine whether the vehicle is already parked.
3. The application finds the first available space.
4. Press **Enter** to accept the suggested space, or type another available slot ID (for example, `B05`).
5. The application marks the selected space as occupied and appends an `Enter` event to `database.txt`.

If the parking facility is full, the application displays a message and does not register the vehicle.

### 2. Vehicle Exit

1. Enter the license plate number of the vehicle leaving the parking facility.
2. The application searches the event log for the vehicle's current parking session.
3. It records an `Exit` event and marks the corresponding space as available.
4. It calculates the elapsed parking time in whole minutes and calculates the fee using the current rate.
5. The application displays the entry time, exit time, duration, parking space, and total fee.

### 3. Parking Status and Vehicle Search

The parking status view displays the three lots and marks occupied spaces with `[X]` and available spaces with `[ ]`. Vehicle search displays the most recent event found for the specified plate number and indicates whether the vehicle is currently parked.

### 4. Revenue Report

The revenue report processes the saved entry and exit events. It pairs completed parking sessions, calculates their fees using the rate currently stored in `fee_per_minut.txt`, and displays the completed-session count, total revenue, and currently parked vehicle count.

## Fee Calculation

The current configured value in `fee_per_minut.txt` is `5000`. The calculation is:

```text
Parking fee = elapsed whole minutes × rate per minute
```

For example, with a rate of **₩5,000 per minute**:

| Parking duration | Fee |
|---:|---:|
| 1 minute | ₩5,000 |
| 5 minutes | ₩25,000 |
| 10 minutes | ₩50,000 |
| 30 minutes | ₩150,000 |

The duration is calculated using whole elapsed minutes. Any remaining seconds are discarded. For example, a stay shorter than one full minute is currently calculated as zero minutes.

To change the rate, select **Settings** (`6`) from the main menu and enter a new integer value. The new value is written to `fee_per_minut.txt` and is used by subsequent fee calculations and revenue reports.

> **Important:** The current implementation uses the latest configured rate when generating the revenue report, including for older completed sessions. Changing the rate can therefore change the reported total for past sessions. The application does not save a separate rate snapshot for each vehicle entry.

## Project Structure

```text
Smart Parking/
│
├── main.py              # Main menu, vehicle entry, search, and event-log handling
├── exit_.py             # Exit workflow and parking-fee calculation
├── parking_lot_data.py  # Default parking lots and their spaces
├── parking_status.py    # Parking occupancy display
├── revenue.py           # Completed-session and revenue summary
├── utils.py             # License plate normalization helper
│
├── database.txt         # Vehicle entry and exit event log
├── fee_per_minut.txt    # Current parking rate (per minute)
│
├── .gitignore           # Files and folders excluded from Git
└── README.md            # Project documentation
```

## Requirements

- Python 3
- A terminal or command prompt
- No third-party Python packages are required

The application uses Python standard-library modules, including `datetime` and `time`.

## Installation and Setup

1. Download or clone this repository.
2. Open a terminal in the project directory (the directory containing `main.py`).
3. Make sure `fee_per_minut.txt` exists and contains a valid integer rate. The included configuration currently contains `5000`.
4. `database.txt` can contain existing event records. If it does not exist, the application can create it when the first event is saved.

## Running the Application

Run the following command from the project directory:

```bash
python main.py
```

On systems where Python 3 is invoked using `python3`, use:

```bash
python3 main.py
```

The application runs interactively in the terminal. Follow the menu prompts to manage vehicles and parking spaces.

## Data Storage

The application uses two plain-text files instead of a database.

### `database.txt`

This file stores each parking event as a pipe-separated record with six fields:

```text
Action|Timestamp|Lot name|Slot name|Vehicle number|Vehicle type
```

Example:

```text
Enter|2026-11-25 09:30|A Lot|A01|12A345BC|Car
Exit|2026-11-25 11:00|A Lot|A01|12A345BC|Car
```

- `Enter` means that a vehicle entered and occupied a space.
- `Exit` means that the vehicle left and the space became available.
- The timestamp format is `YYYY-MM-DD HH:MM`.

The application reads these records at startup to restore parking occupancy. It also uses them for vehicle searches and the revenue report.

### `fee_per_minut.txt`

This file contains one integer: the current parking fee per minute. The Settings menu overwrites the file when the rate is changed.