# Multiprocessing 2 kitchens, 2 cooker, 2 dishes
# 2 process
import multiprocessing
from multiprocessing import Value # Import Value explicitly
import os
from time import sleep, ctime, time

# Basket of sharing
class Basket:
    def __init__(self, eggs):
        # Use multiprocessing.Value for shared mutable state across processes
        self.eggs = Value('i', eggs) # 'i' for integer, eggs is the initial value
        self.lock = multiprocessing.Lock() # Lock for synchronization

    def use_eggs(self, index):
        with self.lock: # Acquire the lock for critical section
            self.eggs.value -= 1 # Access the actual value using .value
            print(f'{ctime()} Kitchen-{index} : Chef-(index) has lock with eggs remaining ({self.eggs.value})')
        print(f'{ctime()} Kitchen-{index} : Chef-(index) has released lock with eggs remaining ({self.eggs.value})')

def cooking(index, basket):
    cooking_time = time()
    print(f'{ctime()} Kitchen-{index} : Begin cooking...PID ({os.getpid()})')
    sleep(2)
    basket.use_eggs(index) # Call the use_eggs method of the Basket instance
    duration = time() - cooking_time
    print(f'{ctime()} Kitchen-{index} : Cooking done in {duration:0.2f} seconds!')


def kitchen(index, basket): # Pass basket to kitchen function
    cooking(index, basket) # Pass basket to cooking function

if __name__ == "__main__":
    # Begin of main thread
    print(f'{ctime()} Main         : Begin Cooking.')
    start_time = time()

    basket = Basket(50) # Initialize Basket with 50 eggs

    # printing main program process id
    print(f'{ctime()} Main         : ID of main process: ({os.getpid()})')

    # Multi processes
    kitchens = [] # Initialize as a list
    for index in range(2):
        # Pass the basket instance to the target function
        p = multiprocessing.Process(target=kitchen, args=(index, basket))
        kitchens.append(p)
        # starting processes
        p.start()

    for p in kitchens: # Iterate through the list of processes
        # wait until processes are finished
        p.join()

    print(f'{ctime()} Main         : Basket eggs remaining ({basket.eggs.value})') # Access the value of Value object
    duration = time() - start_time
    print(f'{ctime()} Main         : Finished Cooking duration in {duration:0.2f} seconds')