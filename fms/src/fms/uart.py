#!/usr/bin/env python

import time 
import serial
import random

class Uart:

    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.serial_port = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
        )
        self.serial_port.flush()
        self.serial_port.reset_input_buffer()
        self.serial_port.reset_output_buffer()
        self.queue = []


    def sendData(self, data):
        try:
            self.serial_port.write(data.encode())
            return 
        except Exception as e:
            return(e) 

    # def receiveData(self, length: int):
    #     if self.serial_port.inWaiting() > 0:
    #         data = self.serial_port.read(length)
    #         print(data)

    def receiveData(self):
        if self.serial_port.inWaiting() > 0:
            data = self.serial_port.readline()
            print(data)


# uart1 = Uart('/dev/ttyACM0', 9600)

# # Simple test case for activating and deactivating EBS relay 
# for i in range(20):
#     # num = random.randint(1,180)
#     # msg = f'STR - {num}\r'

#     # Trigger EBS relay
#     if (i%2):
#         msg = "EBS1\r"
#     # Deactivate relay
#     else:
#         msg = "EBS0\r"   
#     uart1.sendData(msg) 
#     # uart1.receiveData(len(msg)-1)
#     time.sleep(0.03)
#     # uart1.receiveData()
#     # time.sleep(0.1)    
      

# # uart.receiveData(100)
