import multiprocessing as mp
import time
import wmi

Drive_Type = {"Unknown": 0, "No Root Directory": 1, "Local Disk": 2,
              "Network Drive": 3, "Compact Disc": 4, "RAM Disk": 5}


class hw_info():
    def __init__(self):
        self.w = wmi.WMI()

    def disk_info(self):
        #w = wmi.WMI(namespace="root\OpenHardwareMonitor")
        for disk in self.w.Win32_DiskDrive():
            print("Name =", disk.Name)
            print("Model =", disk.Model)
            print("MediaType =", disk.MediaType)
            size = (int(disk.Size)/pow(1024,3))
            print("Size =", round(size, 2), "Gbyte")
            print("InterfaceType =", disk.InterfaceType, "\n")

    def com_info(self):
        for port in self.w.Win32_SerialPort():
            print("Name =", port.Name)
            print("ProviderType =", port.ProviderType)
            print("MaxBaudRate =", port.MaxBaudRate)
            print("Status =", port.Status, "\n")

    def ram_info(self):
        for dev in self.w.Win32_PhysicalMemory():
            print("Name =", dev.Name)
            print("Manufacturer =", dev.Manufacturer)
            size = int(dev.Capacity)/pow(1024, 3)
            print("Capacity =", size, "Gbyte")
            print("DeviceLocator =", dev.DeviceLocator)
            print("SerialNumber =", dev.SerialNumber)

    def usb_info(self):
        for sens in self.w.CIM_USBDevice():
            print(sens.Name)

        for hub in self.w.Win32_USBController():
            print("this is hub", hub.Name)

    def gpu_info(self):
        for gpu in self.w.Win32_VideoController():
            print("Name =", gpu.Name)
            print("Height =", gpu.CurrentVerticalResolution)
            print("Width =", gpu.CurrentHorizontalResolution)

    def voltage_info(self):
        for v in self.w.Win32_VoltageProbe():
            print(v)

    def temp_info(self):
        for temp in self.w.Win32_Processor ():
            print(temp)
            print(temp.CurrentVoltage)

    def cpu_info(self):
        for cpu in self.w.Win32_Processor():
            print(cpu.Name)
            print("NumberOfCores =", cpu.NumberOfCores)
            print("CurrentClockSpeed =", cpu.CurrentClockSpeed)

    def pci_info(self):
        for f in self.w.Win32_PnPEntity():
            if "PCI" in f.PNPDeviceID and not "Стандартный" in f.Name:
                print(f.Name)

    def display_info(self):
        for d in self.w.Win32_DesktopMonitor():
            print("Name =", d.Name)
            print("DeviceID =", d.DeviceID)
            print("ScreenHeight =", d.ScreenHeight)
            print("ScreenWidth =", d.ScreenWidth)

    def foo(self):
        print("this is foo")

def main():
    hw = hw_info()

    #hw.gpu_info()
    #hw.voltage_info()
    #hw.cpu_info()
    #hw.usb_info()
    #hw.disk_info()
    #hw.com_info()
    #hw.ram_info()
    #hw.temp_info()
    #eval('hw.pci_info()')
    #hw.foo()

    list = [arg for arg in dir(hw) if (callable(getattr(hw, arg))
                                      and not arg.startswith('_'))]
    for i in list:
        print(i.upper())
        #eval('hw.'+ i +'()')
        print("\n")
    #print("\n".join([arg for arg in dir(hw) if (callable(getattr(hw, arg))
    #                                  and not arg.startswith('_'))]))
if __name__ == '__main__':
    main()