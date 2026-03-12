import pytest
import subprocess
import json

def load():
    try:
        with open("../expense_tracker_data.json", "r") as data:
            return json.load(data)
    except FileNotFoundError:
        with open("../expense_tracker_data.json", "w") as data:
            json.dump({}, data)
        return {}
    except json.decoder.JSONDecodeError:
        return None

def run_command(command):
    command = "python3 main.py " + command
    subprocess.run(
        command,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        shell=True,
        universal_newlines=True
    )

def get_data(command):
    run_command(command)
    data = load()
    if "delete" not in command:
        assert data is not None
    return data

def clear():
   run_command("clear")

def test_add():
    data = get_data("add --description 'clothes' --amount 20")
    assert len(data) == 1
    clear()

def test_update():
    run_command("add --description 'clothes' --amount 20")

    data = get_data("update --id 1 --description 'clothes' --amount 20")
    assert data["1"]["description"] == "clothes" and data["1"]["amount"] == 20

    data = get_data("update --id 1 --description 'food'")
    assert data["1"]["description"] == "food"

    data = get_data("update --id 1 --amount 40")
    assert data["1"]["amount"] == 40

    clear()

def test_delete():
    run_command("add --description 'clothes' --amount 20")

    data = get_data("delete --id 1")
    print(data.get("1"))
    assert data.get("1") is None

    clear()


if __name__ == "__main__":
    test_delete()

