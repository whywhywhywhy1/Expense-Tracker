import json
from datetime import datetime
from tabulate import tabulate

time_format = "%H:%M:%S"

class TrackerCLI:
    def __init__(self, args):
        self.expenses_data = self.load()

        args_dict = vars(args)
        self.command = args_dict.get("command")
        self.description = args_dict.get("description")
        self.amount = args_dict.get("amount")
        self.id = args_dict.get("id")
        self.month = args_dict.get("month")

    def load(self):
        try:
            with open("../expense_tracker_data.json", "r") as data:
                return json.load(data)
        except FileNotFoundError:
            with open("../expense_tracker_data.json", "w") as data:
                json.dump({}, data)
            return {}
        except json.decoder.JSONDecodeError:
            return None

    def process(self):
        if self.expenses_data is None:
            print("The data is corrupted. Use clear command to delete all data")
            return

        if self.command == "add": self.add()
        if self.command == "list": self.list()
        if self.command == "update": self.update()
        if self.command == "delete": self.delete()
        if self.command == "summary": self.summary()
        if self.command == "clear": self.clear()

    def save(self):
        with open("../expense_tracker_data.json", "w") as data:
            json.dump(self.expenses_data, data, indent=4)

    def clear(self):
        self.expenses_data = {}
        self.save()

    def get_next_id(self):
        if not self.expenses_data:
            return "1"
        return str(max(int(k) for k in self.expenses_data.keys()) + 1)

    def add(self):
        current_id = self.get_next_id()
        self.expenses_data[current_id] = {
            "description" : self.description,
            "amount" : self.amount,
            "date" : {
                "year": datetime.now().year,
                "month": datetime.now().month,
                "day" : datetime.now().day,
            }
        }
        self.save()

    def update(self):
        try:
            if self.description is not None:
                self.expenses_data[self.id]["description"] = self.description
            if self.amount is not None:
                self.expenses_data[self.id]["amount"] = self.amount
            self.save()
        except KeyError:
            print(f"No data with index {self.id}")

    def delete(self):
        try:
            self.expenses_data.pop(self.id)
            self.save()
        except KeyError:
            print(f"No data with index {self.id}")

    def get_date(self, id):
        dt = self.expenses_data[id]["date"]
        return f"{dt["year"]}-{dt["month"]}-{dt["day"]}"

    def list(self):
        table = []
        expenses_attributes = ["ID" , "Description", "Spend", "Date"]
        for i in self.expenses_data.keys():
            table.append([
                self.expenses_data[i]["description"],
                self.expenses_data[i]["amount"],
                self.get_date(i),
            ])
            table[-1].insert(0, i)
        print(tabulate(table, headers=expenses_attributes))

    def summary(self):
        all_expenses = 0
        for dt in self.expenses_data.values():
            if dt["date"]["month"] == self.month or self.month is None:
                all_expenses += dt["amount"]
        print(all_expenses)