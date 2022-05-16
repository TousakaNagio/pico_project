import machine
from time import sleep
import _thread

def core0_thread():
    print("start core0")
    global counter
    counter = 0
    output = 0
    while True:
        output = counter+1
        print("core0: ",output)
        sleep(3)


def core1_thread():
    print("start core1")
    global counter
    counter = 0
    while True:
        counter += 1
        print("core1:",counter)
        sleep(1)
 

second_thread = _thread.start_new_thread(core1_thread, ())
core0_thread()


