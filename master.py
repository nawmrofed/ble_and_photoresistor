import serial
import time   
import csv
import signal
import sys
import json 
import os



Parameters = {
    'SampleCycle' : 10,
    'SampleTime' : 5,
    'PortName' : '/dev/ttyUSB0',
    'OutputFile' : 'test.csv'
}

def print_Banner():
    print('''
 ____  _           _                      _     _             
|  _ \| |__   ___ | |_ ___  _ __ ___  ___(_)___| |_ ___  _ __ 
| |_) | '_ \ / _ \| __/ _ \| '__/ _ \/ __| / __| __/ _ \| '__|
|  __/| | | | (_) | || (_) | | |  __/\__ \ \__ \ || (_) | |   
|_|   |_| |_|\___/ \__\___/|_|  \___||___/_|___/\__\___/|_|   
                                                              
 ____                        _           
|  _ \ ___  ___ ___  _ __ __| | ___ _ __ 
| |_) / _ \/ __/ _ \| '__/ _` |/ _ \ '__|
|  _ <  __/ (_| (_) | | | (_| |  __/ |   
|_| \_\___|\___\___/|_|  \__,_|\___|_|      
''')

def print_Setting_Panel():
    print('''
+----------- SETTING MODE ------------+
| Press '1' to set Serial Port        |
| Press '2' to set Output File Name   |
| Press '3' to set Sample cycle (ms)  |
| Press '4' to set Sample Time (s)    |
| Press Enter to return               |
+-------------------------------------+
''')

def print_Sampling_info(sc, st, port, f):
    print(f'''
+----------- SAMPLING MODE -----------+
  Serial Port      : {port}           
  Output File Name : {f}
  Sample cycle (ms): {sc}             
  Sample Time (s)  : {st}
+-------------------------------------+
+------------- OPERATION -------------+
| Press Enter to sample               |
| Press 's' to set parameters         |
| Press 'Ctrl + c' to quit            |
+-------------------------------------+
    ''')

def signal_handler(sig, frame):
    print('\nquit...')
    sys.exit(0)

def setting():
    global Parameters
    paras = ''
    while(1):
        print_Setting_Panel()
        mode = input('choice:')
        if mode == '1':
            _sp = input("New Serial Port :")
            Parameters['PortName'] = _sp
        elif mode == '2':
            _of = input('New Output File Name :')
            Parameters['OutputFile'] = _of
        elif mode == '3':
            _sc = input("New Sample Cycle :")
            if not _sc.isnumeric():
                print('ERROR: Not Number !!')
            elif not (int(_sc) >= 1 and int(_sc) <= (Parameters['SampleTime'] * 1000)) :
                x = Parameters['SampleTime'] * 1000
                print(f'ERROR: cycle should smaller than {x}(ms) and bigger than 1(ms) !!')
            else:
                Parameters['SampleCycle'] = int(_sc)
        elif mode == '4':
            _st = input("New Sample Time :")
            if not _st.isnumeric():
                print('ERROR: Not Number !!')
            elif not (int(_st) > 0) :
                print(f'ERROR: Sample Time should bigger than 0(s) !!')
            else:
                Parameters['SampleTime'] = int(_st)
        elif mode == '':
            return
        else:
            print('Invalid Command !!')
        with open('parameters','w') as f:
                json.dump(Parameters, f)
    
def sampling(sc, st, pt, f):
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout = 1)
    data = []
    print('pinging...')
    time.sleep(2)
    ser.write(b'S')
    while True:
        ack =ser.readline().decode('ascii')[:-2]
        if ack == 'S':
            break 
    print('preparing...')
    time.sleep(2)
    print('sampling...')
    ser.write(b'1')
    Start_Time = time.time()
    pre_time = Start_Time
    tmp = Start_Time
    while(tmp - Start_Time < st):
        tmp = time.time()
        if (tmp - pre_time) * (10**3) >= sc:   
            pre_time = tmp
            val = ser.readline().decode('ascii')[:-2] 
            data.append([tmp - Start_Time, val])
    ser.write(b'2')
    with open(f, 'w', newline='') as csvfile:
        print('dump data into ' + f + '...')
        writer = csv.writer(csvfile)
        writer.writerow(['time', 'value'])
        for el in data[1:]:
            writer.writerow(el)
        print('DONE')


if __name__ == '__main__':
    print_Banner()
    signal.signal(signal.SIGINT, signal_handler)
    if os.path.isfile('./parameters'):
        with open('parameters','r') as f:
            Parameters = json.load(f)
    while(1):
        print_Sampling_info(Parameters['SampleCycle'], Parameters['SampleTime'], Parameters['PortName'], Parameters['OutputFile'])
        mode = input("choice:")
        if mode == 's':
            setting()
        elif mode == '':
            sampling(Parameters['SampleCycle'], Parameters['SampleTime'], Parameters['PortName'],Parameters['OutputFile'])