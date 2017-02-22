import subprocess

dir_iperf = "resources\\soft\\iperf\\"
cmd = "iperf3.exe -c 127.0.0.1 -t 1 -P4"

def main():
    MAX_SPEED = 0.8
    str = dir_iperf + cmd
    res_list = []

    with subprocess.Popen(str, stdout=subprocess.PIPE) as f:
        for x in f.stdout.readlines():
            #print(x)
            if b"SUM" in x[1:5]:
                print(x.decode("CP866")[38:43] + "Gbits/sec")
                res_list.append(float(x[38:43]))

    try:
        average = sum(res_list) / len(res_list)

        if average < MAX_SPEED:
            print("Failed test")
        else:
            print("Test OK, average speed = ", average)
    except ZeroDivisionError:
        print("run iperf")


if __name__ == '__main__':
        main()