import threading, subprocess

dir_iperf = "resources\soft\iperf\\"
cmd = "iperf3.exe -c 127.0.0.1 -t 1 -P4"

def start_process(command, ignore = False):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if not ignore:
            if (p.wait()):
                    print(command," complited with an error!")
                    exit(1)
    res = [x.decode("CP866") for x in p.stdout.readlines()] #correct output on windwos
    return  res

MAX_SPEED = 0.8
str = dir_iperf + cmd
res_list = []

with subprocess.Popen(str, stdout=subprocess.PIPE) as f:
    for x in f.stdout.readlines():
        #print(x.decode("CP866"))
        if b"SUM" in x[1:5]:
            print(x.decode("CP866")[38:43] + "Gbits/sec")
            res_list.append(float(x[38:43]))

average = sum(res_list) / len(res_list)
if  average < MAX_SPEED:
    print("Failed test")
else:
    print("Test OK, average speed = ", average)