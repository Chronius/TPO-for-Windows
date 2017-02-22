import multiprocessing as mp
import time
import wmi
from decimal import *
from math import factorial


def cpu_info(timeout):
    start = time.time()
    while time.time() - start < timeout:
        w = wmi.WMI(namespace="root\OpenHardwareMonitor")
        temp = {}
        load = {}
        temperature_info = w.Sensor()
        for sensor in temperature_info:
            if sensor.SensorType == 'Temperature' and 'CPU Core ' in sensor.Name:
                temp.update({sensor.Name: sensor.Value})

            if sensor.SensorType == 'Load' and 'CPU Core' in sensor.Name:
                load.update({sensor.Name: sensor.Value})

        for key in temp.keys():
            print(key, "Temperature: ", temp[key], "Load: ", round(load[key], 2))
        print("time =",round((time.time() - start), 3), "s")
        time.sleep(2)


def chudnovsky(x):
    print("Thread go", x)
    n = 100
    pi = Decimal(0)
    k = 0
    while k < n:
        pi += (Decimal(-1)**k)*(Decimal(factorial(6*k))/((factorial(k)**3)*(factorial(3*k)))* (13591409+545140134*k)/(640320**(3*k)))
        k += 1
    pi = pi * Decimal(10005).sqrt()/4270934400
    pi = pi**(-1)
    print(pi)
    return pi


def main():
    print("Please enter test duration in 's'")
    TIMEOUT = int(input())
    if not TIMEOUT >= 5 or not TIMEOUT <= 120  :
        print("Test duration incorrect\nset default time")
        TIMEOUT = 5
    print("*********************Start CPU load test*********************")
    p = mp.Pool()
    p.map_async(chudnovsky, range(4))
    p2 = mp.Process(cpu_info(TIMEOUT))

if __name__ == '__main__':
        main()
        print("\t*********************End test*********************")
