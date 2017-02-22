import time, struct
binfile = open('M:\\test.bin', 'wb')
start = time.time()
size = 1024*1024
for num in range(size):
    data = struct.pack('i', 0)
    binfile.write(data)
end = time.time()
size = size*4
print("data size %i byte" %size,"or", round(size/1024, 2), "KByte")
end = round(end - start,10)
speed = size/end
print(end, "s")
print("write: ", round((speed/1024)/1024, 3), "Mbyte/sec")
binfile.close()

binfile = open('M:\\test.bin', 'rb')

start = time.time()
s = binfile.read(1)
while s:
    s = binfile.read(4)
end = time.time()
end = round(end - start, 10)
speed = size/end
print(end, "s")
print("read: ", round((speed/1024)/1024, 3), "Mbyte/sec")
binfile.close()