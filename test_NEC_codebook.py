# to run: sudo python3 ./test_NEC_codebook.py

import serial
import time

import numpy as np
from numpy import genfromtxt


# functions for sending data to microcontroller

def send2ser(text, sleep):
    # Print the composed message
    print(f"Composed message: {text}")

    # Send packet
    ser.write(text.encode())

    # Get reply within timeout
    reply = ser.readline()
    print(reply.decode() + "\n")
    time.sleep(sleep)

def init(ris_id):
    # initialize message to be sent to microcontroller
    return "AT" + ris_id

def serialize(array):
    out = ''
    for i in range(array.shape[0]):
      for j in range(array.shape[1]):
        out += str(int(array[i,j]))
    return out

# open serial port
# to check serial port on linux: sudo dmesg | grep tty
ser = serial.Serial('/dev/ttyACM0', 115200, 8, timeout=10)

# Prompt the user for the desired configuration
ris_id = input("Enter RIS_ID (e.g., '1'): ")
print("Choose configuration type:")
print("2: Static [+30,0] configuration")
print("3: Reset configuration")
print("4: Sweep configuration")
choice = input("Enter your choice (3/4): ")

# Initialize the message
msg = init(ris_id)

if choice == "3":
    # Initialize the message
    msg = init(ris_id)
    # Config absorption: AT + RIS_ID + R (for reset) + \r\n
    msg += "R\r\n"
    send2ser(msg)

elif choice == '4':
    # import data
    mapping = genfromtxt('mapping.csv', delimiter=',')
    phase_shift = np.load('sw_indexes_codebook_pace33_Nx_16_Ny_16.npy')

    # define range
    start = 1085
    step = 4
    end = 1426

    for i in range(start,end,step):
        if(mapping[i,1] == 15 or mapping[i,1] == 30 or mapping[i,1] == 45):
          print(mapping[i,:])

          # Initialize the message
          msg = init(ris_id)
          msg += "F"
          msg += serialize(phase_shift[:,:,i])
          msg += "\r\n"
          #print(f"Configuration tx: {-txdeg*10}, rx: {rxdeg*10} ")
          send2ser(msg, 20)

else:
    print("Invalid choice. Exiting.")
    exit()
