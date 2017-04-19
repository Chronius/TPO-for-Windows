import subprocess, sys

def main():
    with subprocess.Popen("resources\\soft\\glxgear.exe -v", stdin=subprocess.DEVNULL,
                          stdout=subprocess.PIPE, bufsize=1) as f:
        fps = []
        for line in f.stdout:
            out = line.decode('CP866').strip()
            if line != "":
                print(out)
            if "frames" in out:
                frame = out.split(" ") #out[29:32]
                fps.append(float(frame[6]))
            sys.stdout.flush()
        fps_average = (sum(fps)/len(fps))
        return
        if fps_average <= 30:
            exit(1)
        if f.wait() == 0: # err
            print("opengl window err")
            exit(1)
if __name__ == '__main__':
    main()
    exit(0)