import multiprocessing as mp
import time, sys
import wmi
from decimal import *
from math import factorial
from multiprocessing import Pool

TEMP_MAX = 80
def setpriority(pid=None, priority=1):
    """ Set The Priority of a Windows Process.  Priority is a value between 0-5 where
        2 is normal priority.  Default sets the priority of the current
        python process but can take any valid process ID. """

    import win32api, win32process, win32con

    priorityclasses = [win32process.IDLE_PRIORITY_CLASS,
                       win32process.BELOW_NORMAL_PRIORITY_CLASS,
                       win32process.NORMAL_PRIORITY_CLASS,
                       win32process.ABOVE_NORMAL_PRIORITY_CLASS,
                       win32process.HIGH_PRIORITY_CLASS,
                       win32process.REALTIME_PRIORITY_CLASS]
    if pid == None:
        pid = win32api.GetCurrentProcessId()
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
    win32process.SetPriorityClass(handle, priorityclasses[priority])


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
            print(key, "Temperature: ", temp[key], "Load: ", round(load[key], 2), "%")
            if temp[key] >= TEMP_MAX:
                print("!!! High temperature on", key, "!!!")
                exit(1)
        print("----------------------")
        print("time passed =", round((time.time() - start), 3), "s")
        print("---------------------------------------")
        sys.stdout.flush()
        time.sleep(2)


def chudnovsky(x):
    print("Thread go", x, "\n")
    setpriority(priority=0)
    n = 5000
    pi = Decimal(0)
    k = 0
    while k < n:
        pi += (Decimal(-1)**k)*(Decimal(factorial(6*k))/((factorial(k)**3)*(factorial(3*k)))* (13591409+545140134*k)/(640320**(3*k)))
        k += 1
    pi = pi * Decimal(10005).sqrt()/4270934400
    pi = pi**(-1)
    print(pi)
    sys.stdout.flush()
    return pi


def main():

    timeout = 60
    p = mp.Pool()
    p2 = mp.Process(target=cpu_info, args=(timeout,))

    p2.start()
    res = p.map_async(chudnovsky, range(mp.cpu_count()))
    p2.join()
    while p2.is_alive():
        pass
    if p2.exitcode == 1:        
        print("")
        exit(1)

if __name__ == '__main__':
        main()
        print("\tSuccess end test\n".upper())
        sys.stdout.flush()
