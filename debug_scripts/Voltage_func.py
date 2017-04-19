import subprocess

import subprocess
dir_tool = "resources\\soft\\"
#dir_tool = ".\\"

V12_MIN = 8.5
V12_MAX = 20

V5_MIN = 4.75
V5_MAX = 5.25

V3_MIN = 3.0
V3_MAX = 3.6

VBAT_MIN = 3.3
VBAT_MAX = 3.8

def get_temp_description(name, temp):

    key_temp = {"3V3": (temp <= V3_MAX) and (temp >= V3_MIN),
                "VBAT": (temp <= VBAT_MAX) and (temp >= VBAT_MIN),
                "5V": (temp <= V5_MAX) and (temp >= V5_MIN),
                "12V": (temp <= V12_MAX) and (temp >= V12_MIN),}
    return key_temp[name]


def voltage_info():
    volt_type = {1: "VCORE", 2: "1V8", 3: "2V5", 4: "3V3", 5: "VBAT", 6: "5V", 7: "5VSB", 8: "12V", 9: "AC"}
    sens_count = 0
    count_err = 0
    with subprocess.Popen(dir_tool + "ktool32.exe volt GetVoltageSensorCount ",
                          stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, bufsize=1) as process:
        output = ""
        for line in process.stdout.readlines():  # b'\n'-separated lines
            if b"count" in line:
                sens_count = int(line[22:26].decode('CP866'))
        for i in range(sens_count):
            with subprocess.Popen(dir_tool + "ktool32.exe volt GetVoltageSensorInfo " + str(i),
                                  stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, bufsize=1) as process:
                for line in process.stdout.readlines():
                    if b"name" in line:
                        output = line.decode("CP1251")[6:].strip()
                        print("name", output)
            with subprocess.Popen(dir_tool + "ktool32.exe volt GetVoltageSensorValue " + str(i),
                                  stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, bufsize=1) as process:
                for line in process.stdout.readlines():
                    if b"value" in line:
                        sens_value = float(line[14:21])
                        sens_value /= 1000
                        print("Value = ", sens_value, "V")
                        if get_temp_description(output, sens_value):
                            print("Test PASSED")
                            print("---------------------------------------")
                        else:
                            count_err += 1
                            print("Test FAILED")
                            print("---------------------------------------")
        output = None
    if count_err != 0:
        exit(1)

if __name__ == '__main__':
    voltage_info()
