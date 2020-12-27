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
    - photoresistor  
      - first pin -> A0
      - third pin -> GND
      - fourth pin -> 5V

- Raspberrypi pi

  - Connect to Rpi:

      ```bash
      ssh pi@192.168.1.10
      ```

  - run the program:

      ```bash
      cd  ~/Documents
      python3 master.py
      ```

  - copy file from Rpi to your computer:

    ```bash
    scp pi@192.168.1.10:[src file path] [dst file path]
    ```

  - shut down Rpi (please shut down Rpi before turn off power)
  
      ```bash
      sudo halt
      ```
  <!-- test emoji ! -->
