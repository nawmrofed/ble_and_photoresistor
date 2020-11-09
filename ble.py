import serial
import time   
import csv
import signal
import sys

def signal_handler(sig, frame):
    print('\nquit...')
    sys.exit(0)
            
#Change your port name COM... and your baudrate
port_name = input("specify your port name? (ex: COM8) ")
ser = serial.Serial(port_name, 9600, timeout = 1) 
signal.signal(signal.SIGINT, signal_handler)
while(1):
    data = []
    file_name = input("specify output file name:")
    sample_rate = input("sample cycle ?(8 millis to 100 millis):")
    if not sample_rate.isnumeric():
        print("number please !")
        continue
    sample_rate = int(sample_rate)
    if sample_rate > 100 or sample_rate < 8:
        print("invalid range !")
        continue
    ser.write(bytes(str(sample_rate), 'ascii'))
    while True:
        ack =ser.readline().decode('ascii')[:-2]
        if  ack.isnumeric() and int(ack) == sample_rate:
            break
    ser.write(b'S')
    while True:
        ack =ser.readline().decode('ascii')[:-2]
        if ack == 'S':
            break 
    print('sampling ' + str(2500 // sample_rate) + ' points... wait for seconds...')
    time.sleep(5)
    for i in range(0, 2500 // sample_rate):
        ser.write(b'1')
        val = ''
        while not val.isnumeric():
            val = ser.readline().decode('ascii')[:-2]
        data.append([i*sample_rate, val])
    with open(file_name, 'w', newline='') as csvfile:
        print('dump data into ' + file_name + '...')
        writer = csv.writer(csvfile)
        writer.writerow(['time', 'value'])
        for el in data:
            writer.writerow(el)
        print('DONE')

