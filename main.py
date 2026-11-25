import time
from datetime import datetime
from parking_lot_data import parking_lot
import exit_
import parking_status
import revenue
from utils import normalize_n


# save data
def save_data(action, lot_name, slot_name, v_num, v_typ):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")  # current time
    with open("database.txt", "a") as file:
        file.write(f"\n{action}|{now}|{lot_name}|{slot_name}|{v_num}|{v_typ}")
    return now


# load data
def load_data():
    records = []
    try:
        with open("database.txt", "r") as file:
            for line in file:
                data = line.strip().split("|")
                if len(data) == 6:
                    records.append(data)
    except FileNotFoundError:
        pass
    return records
    # 0-action, 1-time, 2-lot name, 3-slot name, 4-vehicle number, 5-vehicle type


# resote data
def restore_parking_state():
    for record in load_data():
        action, lot_name, slot_name = record[0], record[2], record[3]
        if action == "Enter":
            parking_lot[lot_name][slot_name] = 1
        elif action == "Exit":
            parking_lot[lot_name][slot_name] = 0


# find available slot
def find_available_slot():
    for lot_name, slots in parking_lot.items():
        for slot_name, value in slots.items():
            if value == 0:
                return lot_name, slot_name
    return None  # Parking is FUll


# check status
def is_vehicle_parked(v_number):
    v_number = normalize_n(v_number)
    status = False
    for data in load_data():
        if data[4] == v_number:
            if data[0] == "Enter":
                status = True
            elif data[0] == "Exit":
                status = False
    return status


# search
def search_vehicle(v_number):
    v_number = normalize_n(v_number)
    last = None
    for record in load_data():
        if record[4] == v_number:
            last = record

    if last is None:
        print("\nVehicle not found!\n")
        return

    action, time_, lot_name, slot_name, number, v_type = last
    if action == "Enter":
        status = "Parked"
        time_label = "Entry Time    "
    else:
        status = "Not Parked"
        time_label = "Last Exit Time"

    print(
        "\n-----Vehicle Found-----\n"
        f"Vehicle Number : {number}\n"
        f"Vehicle Type   : {v_type}\n"
        f"Parking Space  : {lot_name} - {slot_name}\n"
        f"{time_label}   : {time_}\n"
        f"Current Status : {status}\n"
    )


# vehicle entry
def vehicle_entry():
    print("----------VEHICLE ENTRY----------")
    v_number = input("Enter vehicle number: ").strip().upper()
    v_number = normalize_n(v_number)
    if v_number == "":
        print("Vehicle number cannot be empty!")
        return
    if is_vehicle_parked(v_number):
        print("This vehicle already parked")
        return
    v_type = input("Enter vehicle type: ").strip()
    if v_type == "":
        print("Vehicle type cannot be empty!")
        return
    # Loading Animation
    print("Checking available spaces", end="")
    for i in range(3):
        time.sleep(0.6)
        print(".", end="")
    print("")

    result = find_available_slot()
    if result is None:
        print("Sorry, parking is full!")
        return

    user_choice = (
        input(
            f"Available: {result[0]} - {result[1]}\n"
            "Press Enter to choose or enter a slot name (e.g. B05): "
        )
        .strip()
        .upper()
    )

    # Enter
    if user_choice == "":
        lot_name, slot_name = result
        parking_lot[lot_name][slot_name] = 1
        save_data("Enter", lot_name, slot_name, v_number, v_type)
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        print(
            "\nVehicle successfully parked!\n"
            "-----------------------------------\n"
            f"Vehicle Number : {v_number}\n"
            f"Vehicle Type   : {v_type}\n"
            f"Parking Space  : {lot_name} - {slot_name}\n"
            f"Entry Time     : {now}\n"
        )
        return

    # Other than Enter
    for lot_name, slots in parking_lot.items():
        if user_choice in slots:
            if slots[user_choice] == 0:
                slots[user_choice] = 1
                save_data("Enter", lot_name, user_choice, v_number, v_type)
                now = datetime.now().strftime("%Y-%m-%d %H:%M")
                print(
                    "\nVehicle successfully parked!\n"
                    "-----------------------------------\n"
                    f"Vehicle Number : {v_number}\n"
                    f"Vehicle Type   : {v_type}\n"
                    f"Parking Space  : {lot_name} - {user_choice}\n"
                    f"Entry Time     : {now}\n"
                )
            else:
                print("This parking slot is already occupied!")
            return

    print("Invalid parking slot!")


# main program
restore_parking_state()
vehicle_exit = exit_.Exit(parking_lot, load_data, save_data)

while True:
    print(
        "     Smart Parking Management \n"
        "1. Vehicle Entry \n"
        "2. Vehicle Exit \n"
        "3. View Parking Status \n"
        "4. Search Vehicle \n"
        "5. Parking Revenue Report \n"
        "6. Settings \n"
        "0. Exit"
    )
    try:
        command = int(input("Select an option: "))
    except ValueError:
        print("Please enter a valid number!")
        continue
    if command == 0:
        print("Thank you for using Smart Parking!")
        break
    elif command == 1:
        vehicle_entry()
    elif command == 2:
        vehicle_exit.run()
    elif command == 3:
        parking_status.run(parking_lot, load_data())
    elif command == 4:
        search = input("Enter vehicle number: ").strip().upper()
        search = normalize_n(search)
        search_vehicle(search)
    elif command == 5:
        revenue.summary(load_data())
    elif command == 6:
        print("----------Settings---------")
        new_rate = int(input("Enter New Hourly Rate: ").strip())
        with open("fee_per_minut.txt", "w") as file:
            file.write(str(new_rate))
        print("Hourly Rate Updated - ", new_rate)
    else:
        print("Invalid option!")
