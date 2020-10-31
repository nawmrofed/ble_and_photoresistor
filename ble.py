import serial
import time   
import csv

def retrieveData():
    ser.write(b'1')
    data = ser.readline().decode('ascii')
    return data[:-2]

elapsed = 0
#Change your port name COM... and your baudrate
port_name = input("specify your port name? (ex: COM8) ")
ser = serial.Serial(port_name, 9600, timeout = 1) 
while(1):
    data = []
    file_name = input("specify output file name:")
    input("press enter to start sampling...")
    start = time.time()
    elapsed = 0
    while elapsed < 10:
        data.append([(time.time() - start),retrieveData()])
        elapsed = time.time() - start
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['time', 'value'])
        for el in data:
            writer.writerow(el)

