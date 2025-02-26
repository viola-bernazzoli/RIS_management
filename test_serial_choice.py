# to run: sudo python3 ./test_serial_choice.py

import serial

# 51, -102, 154, 0 , -154, 51, -51, 154, 0, -154, 51, -51, 154, 0, -154, 102
# from -45, to 30

# 154, -51, 154, -51 , -102, -102, 51, -154, 0, 154, -51, 102, -102, 51, -154, 51
# 5252337415263747525233741526374752523374152637475252337415263747525233741526374752523374152637475252337415263747525233741526374752523374152637475252337415263747525233741526374752523374152637475252337415263747525233741526374752523374152637475252337415263747
# from -45 to 10

# open serial port
# to check serial port on linux: sudo dmesg | grep tty
ser = serial.Serial('/dev/ttyACM0', 115200, 8, timeout=10)

# Prompt the user for the desired configuration
ris_id = input("Enter RIS_ID (e.g. 1): ")
print("Choose configuration type:")
print("1: One element configuration")
print("2: All elements same configuration")
print("3: Full configuration chosen")
print("4: Reset configuration")
choice = input("Enter your choice (1/2/3/4): ")

# Initialize the message
msg = "AT" + ris_id


if choice == "1":
    # Config one element: AT + RIS_ID + S (for set) + ROW + COLUMN + PHASE_SHIFT (1->8) + \r\n
    row = input("Enter ROW (e.g., '03'): ")
    column = input("Enter COLUMN (e.g., '07'): ")
    phase_shift = input("Enter PHASE_SHIFT [1->8]: ")
    if len(row) < 2:
        row = "0" + row
    if len(column) < 2:
        column = "0" + column
    msg += "S" + row + column + phase_shift + "\r\n"

elif choice == "2":
    # Config whole RIS: AT + RIS_ID + F (for full) + 256 * PHASE_SHIFT (1->8) + \r\n
    phase_shift = input("Enter PHASE_SHIFT (1->8): ")
    msg += "F"
    for i in range(256):
        msg += phase_shift
    msg += "\r\n"

elif choice == '3':
    # Config
    phase_shift = input("Enter your configuration: ")
    msg += "F"
    msg += phase_shift
    msg += "\r\n"

elif choice == "4":
    # Config absorption: AT + RIS_ID + R (for reset) + \r\n
    msg += "R\r\n"

else:
    print("Invalid choice. Exiting.")
    exit()

# Print the composed message
print(f"Composed message: {msg}")

# Send packet
ser.write(msg.encode())

# Get reply within timeout
reply = ser.readline()
print(reply.decode() + "\n")
