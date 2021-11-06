import time

import hid

def select_device():
    devices_list = hid.enumerate()
    for i, device in enumerate(devices_list):
        print(f"{i} - {device['product_string']}")

    while True:
        print("\nPlease select a device.")
        device_id = input("Id of the selected device:")
        try:
            selected_device = devices_list[int(device_id)]
        except Exception:
            print("Invalid input")
        else:
            print(f"Device selected: {selected_device['product_string']}")
            break

    gamepad = hid.device()
    gamepad.open(selected_device["vendor_id"], selected_device["product_id"])
    gamepad.set_nonblocking(True)

    return gamepad


def read_device(gamepad, numeric_positions=None):
    if numeric_positions is None:
        # positions of the joystick axis
        numeric_positions = (0, 1, 2, 3, 4, 9, 10)

    numbers = []
    for position, number in enumerate(gamepad.read(64)):
        if position in numeric_positions:
            numbers.append(number)
        else:
            numbers.append(bin(number)[2:].rjust(8, "0"))

    return numbers


def print_row(gamepad):
    numbers = read_device(gamepad)
    print("|", end="")
    for num in numbers:
        s_num = str(num).center(12)
        print(s_num, end="|")
    print("")


def continues_print(gamepad):
    while True:
        print_row(gamepad)
        time.sleep(1)


def main():
    gamepad = select_device()
    continues_print(gamepad)

if __name__ == "__main__":
    main()
