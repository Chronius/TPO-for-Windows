import subprocess

dir_iperf = "resources\\soft\\iperf\\"
#dir_iperf = "C:\develop\TPO_Debug\\resources\\soft\\iperf\\"

cmd = "iperf3.exe -c 127.0.0.1 -t 1 -P4"

def main():
    MAX_SPEED = 0.8
    str_cmd = dir_iperf + cmd
    res_list = []

    try:
        f = subprocess.Popen(str_cmd, stdout=subprocess.PIPE, bufsize=1)
        for x in f.stdout.readlines():
            print(x.decode("CP1251").strip())
            if b"SUM" in x[1:5]:
                #print(x.decode("CP866")[38:43] + "Gbits/sec")
                res_list.append(float(x[38:43]))
    except:
        print("Run iperf and try again")
    print()
    try:
        average = sum(res_list) / len(res_list)
        for res in res_list:
            print("sum speed =", res, "Gbits/sec")
        if average < MAX_SPEED:
            print("Failed test")
        else:
            print("\nTest OK, average speed = ", average, "Gbits/sec")
    except ZeroDivisionError:
        print("Test failed")
        print("result list =", res_list)
        print(len(res_list))


if __name__ == '__main__':
        main()