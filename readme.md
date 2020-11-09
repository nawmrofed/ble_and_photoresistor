## BLE and photoresistor 

### target

record photoresistor value and send it to computer, record as csv file.

### installation

```bash
git clone https://github.com/nawmrofed/ble_and_photoresistor.git
pip install pyserial
```

### Toturial

- Arduino part:
  1. Finish arduino side's wiring, then turn on the power.
    - bluetooth module(HC-06)
      - VCC -> 5V
      - GND -> GND
      - TxD -> ~10
      - RxD -> ~11
    - photoresistor  
      - first pin -> A0
      - third pin -> GND
      - fourth pin -> 5V
- Computer part:
  1. For computer side, turn on bluetooth and connect the device **"photoresistor"**.
  2. find out the device's Connect port name.
  3. execute ble.py (python ble.py)
  4. input the device name
  5. specify output file name
  6. press enter to record value
  7. wait for ten seconds, it will record values and dump them into csv.
