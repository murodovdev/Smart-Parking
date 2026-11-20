import time

print(
    "     Smart Parking Managment \n"
    "1. Vehical Entry \n"
    "2. Vehical Exit \n"
    "3. View Parking Status \n"
    "4. Search Vehicle \n"
    "5. View Available Spaace \n"
    "6. View Parking History \n"
    "7. Parking Revenue Report \n"
    "8. Manage Parking Space \n"
    "9. Setting \n"
    "0. Exit"
)

parking_lot = {
    "A Lot": {
        "A01": 0,
        "A02": 0,
        "A03": 0,
        "A04": 0,
        "A05": 0,
        "A06": 0,
        "A07": 0,
        "A08": 0,
        "A09": 0,
        "A10": 0,
    },
    "B Lot": {
        "B01": 0,
        "B02": 0,
        "B03": 0,
        "B04": 0,
        "B05": 0,
        "B06": 0,
        "B07": 0,
        "B08": 0,
        "B09": 0,
        "B10": 0,
    },
    "C Lot": {
        "C01": 0,
        "C02": 0,
        "C03": 0,
        "C04": 0,
        "C05": 0,
        "C06": 0,
        "C07": 0,
        "C08": 0,
        "C09": 0,
        "C10": 0,
    },
}

command = int(input("Select an option: "))

if command == 1:
    print("----------VEHICLE ENTRY----------")
    v_number = input("Enter vehicle number: ")
    v_type = input("Enter vehicle type: ")

    print("Checking available spaces", end="")
    for i in range(1):
        time.sleep(1)
        print(".", end="")
    print("")

    def find_available_slot():
        for lot_name, slots in parking_lot.items():
            for slot_name, value in slots.items():
                if value == 0:
                    return lot_name, slot_name


result = find_available_slot()
user_choice = (
    input(
        f"Available: {result[0]} - {result[1]}\n"
        "Press Enter to choose or enter a slot name (e.g. B05): "
    )
    .strip()
    .upper()
)

if user_choice == "":
    lot_name, slot_name = result
    parking_lot[lot_name][slot_name] = 1
    print(f"Successfully parked at {lot_name} - {slot_name}")
else:
    found = False
    for lot_name, slots in parking_lot.items():
        if user_choice in slots:
            found = True
            if slots[user_choice] == 0:
                slots[user_choice] = 1
                print(f"Successfully parked at {lot_name} - {user_choice}")
            else:
                print("This parking slot is already occupied!")
            break
    if not found:
        print("Invalid parking slot!")


print(parking_lot)
