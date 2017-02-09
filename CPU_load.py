import multiprocessing as mp
import time
import wmi

def cpu_info(timeout):
    start = time.time()
    while time.time() - start < timeout:
        sensor_cpu = []
        w = wmi.WMI(namespace="root\OpenHardwareMonitor")

        temperature_info = w.Sensor()
        for sensor in temperature_info:
            if sensor.SensorType == 'Temperature' and 'Core' in sensor.Name:
                temp = {"Sensor": sensor.Name, "Temperature": sensor.Value, "Load": 0}
                sensor_cpu.append(temp)
            if sensor.SensorType == 'Load' and 'Core' in sensor.Name:
                for x in sensor_cpu:
                    if x['Sensor'] == sensor.Name:
                        x["Load"] = round(sensor.Value, 2)

        sensor_cpu = '\n'.join(str(v) for v in sensor_cpu)
        print(sensor_cpu)
        print("time =",round((time.time() - start), 3), "s")
        time.sleep(5)

#to replace the function of calculation of pi
def foo(x):
    while True:
        print("Thread go", x)
        time.sleep(1)

def main():
    print("Please enter test duration in 's'")
    TIMEOUT = int(input())
    if not TIMEOUT >= 5 or not TIMEOUT <= 120  :
        print("Test duration incorrect\nset default time")
        TIMEOUT = 5
    print("*********************Start CPU load test*********************")
    p = mp.Pool()
    p.map_async(foo, range(2))
    p2 = mp.Process(cpu_info(TIMEOUT))

if __name__ == '__main__':
        main()
        print("\t*********************End test*********************")
