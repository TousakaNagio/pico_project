import machine
from time import sleep
import _thread

def core0_thread():
    global run_core1
    global counter
    
    print("start core0")
    counter = 0
    output = 0
    while True:
        output = counter+1
        print("core0: ",output)
        run_core1=True
        sleep(3)


def core1_thread():
    global run_core1
    global counter
    
    while not run_core1:
        pass
    
    print("start core1")
    counter = 0
    while True:
        counter += 1
        print("core1:",counter)
        sleep(1)
 

run_core1=False 
second_thread = _thread.start_new_thread(core1_thread, ())
core0_thread()
