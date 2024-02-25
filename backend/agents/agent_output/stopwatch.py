# filename: stopwatch.py
import time
start_time = time.time()
time.sleep(5)
end_time = time.time()
print("Elapsed time: {} seconds".format(end_time - start_time))
exit()