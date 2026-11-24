def run(parking_lot, load_data):
    print("\n----------PARKING STATUS----------\n")
    for lots, slots in parking_lot.items():
        print(f"{lots} - ", end="")
        for slot_name, value in slots.items():
            print(f"{slot_name}", end="")
            print("[X]" if value == 1 else "[ ]", end=" ")
        print("")
        print("")
