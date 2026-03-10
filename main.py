import argparse
import json
from datetime import datetime

allowed_args = ['--description', '--amount', '--id']
time_format = "%m/%d/%Y, %H:%M:%S"

class TrackerCLI:

    def __init__(self, args):
        self.expenses_data = {}
        self.query = args.query
        self.description = args.description
        self.amount = args.amount
        self.id = args.id

        try:
            with open("expense_tracker_data.json", "r") as data:
                self.expenses_data = json.load(data)
        except FileNotFoundError:
            self.save()

    def process(self):
        if self.query == "add": self.add()

    def save(self):
        with open("expense_tracker_data.json", "w") as data:
            json.dump(self.expenses_data, data, indent=4)

    def get_id(self):
        if not self.expenses_data:
            current_id = 0
        else:
            current_id = int(max(self.expenses_data.keys()))

        return str(current_id + 1)

    def add(self):
        current_id = self.get_id()
        self.expenses_data[current_id] = {
            "description" : self.description,
            "amount" : self.amount,
            "date" : datetime.now().strftime(time_format),
        }
        self.save()

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('query')
    for i in allowed_args:
        parser.add_argument(i)

    args = parser.parse_args()

    cli = TrackerCLI(args)
    cli.process()


if __name__ == "__main__":
    main()