import time

time1 = time.time()

print("time1",time1)
time.sleep(.005);
time2 = time.time()
print("time2",time2)

print("diff", (time2 - time1))
