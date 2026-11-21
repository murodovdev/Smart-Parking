import time
from datetime import datetime
from parking_lot_data import parking_lot
import exit_


# save data
def save_data(action, lot_name, slot_name, v_num, v_typ):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")  # current time
    with open("database.txt", "a") as file:
        file.write(f"{action}|{now}|{lot_name}|{slot_name}|{v_num}|{v_typ}\n")


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


def is_vehicle_parked(v_number):
    status = False
    for data in load_data():
        if data[4] == v_number:
            if data[0] == "Enter":
                status = True
            elif data[0] == "Exit":
                status = False
    return status


# vehicle entry
def vehicle_entry():
    print("----------VEHICLE ENTRY----------")
    v_number = input("Enter vehicle number: ").strip().upper()
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
        print(f"Successfully parked at {lot_name} - {slot_name}")
        return

    # Other than Enter
    for lot_name, slots in parking_lot.items():
        if user_choice in slots:
            if slots[user_choice] == 0:
                slots[user_choice] = 1
                save_data("Enter", lot_name, user_choice, v_number, v_type)
                print(f"Successfully parked at {lot_name} - {user_choice}")
            else:
                print("This parking slot is already occupied!")
            return

    print("Invalid parking slot!")


# main program
restore_parking_state()

while True:
    print(
        "     Smart Parking Management \n"
        "1. Vehicle Entry \n"
        "2. Vehicle Exit \n"
        "3. View Parking Status \n"
        "4. Search Vehicle \n"
        "5. View Available Space \n"
        "6. View Parking History \n"
        "7. Parking Revenue Report \n"
        "8. Manage Parking Space \n"
        "9. Settings \n"
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
        print
    else:
        print("Invalid option!")
