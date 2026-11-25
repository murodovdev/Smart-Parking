from datetime import datetime
from utils import normalize_n
class Exit:
    fee_per_minut = 5000

    def __init__(self, parking_lot, load_data, save_data):
        self.parking_lot = parking_lot
        self.load_data = load_data
        self.save_data = save_data

    def find_vehicle(self, v_number):
        v_number = normalize_n(v_number)
        status = None
        for data in self.load_data():
            if data[4] == v_number:
                if data[0] == "Enter":
                    status = data
                else:
                    status = None
        return status

    def calculate_minut(self, entry_time, exit_time):
        start = datetime.strptime(entry_time, "%Y-%m-%d %H:%M")
        end = datetime.strptime(exit_time, "%Y-%m-%d %H:%M")
        minut = int((end - start).total_seconds() // 60)
        return minut

    def run(self):
        print("-----------Vehicle Exit----------")
        v_number = input("Enter Vehicle NUmber: ").strip().upper()
        v_number=normalize_n(v_number)
        if v_number == "":
            print("Enter something!!")
            return
        found = self.find_vehicle(v_number)
        if found is None:
            print("This Vehicle is not in the parking")
            return
        (
            entry_time,
            lot_name,
            slot_name,
            v_type,
        ) = found[1], found[2], found[3], found[5]
        exit_time = self.save_data("Exit", lot_name, slot_name, v_number, v_type)
        self.parking_lot[lot_name][slot_name] = 0

        minuts = self.calculate_minut(entry_time, exit_time)
        fee = minuts * self.fee_per_minut
        print(
            "\nVehicle successfully exited!\n"
            "-----------------------------------\n"
            f"Vehicle Number : {v_number}\n"
            f"Vehicle Type   : {v_type}\n"
            f"Parking Space  : {lot_name} - {slot_name}\n"
            f"Entry Time     : {entry_time}\n"
            f"Exit Time      : {exit_time}\n"
            f"Duration       : {minuts} minute(s)\n"
            f"Total Fee      : {fee:,} won\n"
        )
