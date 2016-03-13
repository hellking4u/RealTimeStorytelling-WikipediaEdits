"""
decrement.py

The code is taken from Mike's repository, since it does exactly what's required here,
there is minimal/no editing to the code required.

the original file can be found here : https://github.com/mikedewar/RealTimeStorytelling/blob/master/4/forget.py
"""
import redis
import time
import numpy as np

conn = redis.Redis(db=3)

forgetting_rate = 0.3

while True:

    keys = conn.keys("*")

    for key in keys:

        pipe = conn.pipeline()
        with conn.pipeline() as pipe:
            while True:
                try:
                    pipe.watch(key)
                    d = pipe.get(key)
                    count = int(d)
                    if count > 1:
                        to_remove = np.random.poisson(count * forgetting_rate)
                        print key, count, count-to_remove
                        pipe.set(key,count-to_remove)
                    pipe.execute()
                    break
                except redis.WatchError:
                    print "interrupted!"
                    continue
    time.sleep(10)
