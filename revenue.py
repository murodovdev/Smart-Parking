from datetime import datetime

def summary(data):
    fee_per_minut = 0
    with open("fee_per_minut.txt", "r") as file:
        fee_per_minut = int(file.read())
    save_transactions = []
    currently_parked = 0

    for n, record in enumerate(data):
        action, time, lot_name, slot_name, v_number, v_type = record

        if action == "Enter":
            for i in data[n + 1 :]:
                if i[4] == v_number and i[0] == "Exit":
                    start = datetime.strptime(time, "%Y-%m-%d %H:%M")
                    end = datetime.strptime(i[1], "%Y-%m-%d %H:%M")
                    minut = int((end - start).total_seconds() // 60)
                    save_transactions.append(minut * fee_per_minut)
                    break

    currently_parked = len(data) - (len(save_transactions) * 2)
    revenue = sum(save_transactions)
    
    print(
        f"Completed trips  : {len(save_transactions)}\n"
        f"Total revenue    : {revenue:,} won\n"
        f"Currently parked : {currently_parked} vehicle(s)")
