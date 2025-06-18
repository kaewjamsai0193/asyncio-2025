# Multiprocessing 2 kitchens, 2 cooker, 2 dishes
# Share resources
import multiprocessing
import os
from time import sleep, ctime, time

# Basket of sharing
class Basket:
    def __init__(self):
        self.eggs = 50
        self.lock = multiprocessing.Lock()

    def use_eggs(self, index):
        with self.lock: # Acquire the lock before accessing shared resource
            self.eggs -= 1
            print(f'{ctime()} Kitchen-{index} : Chef-{index} has lock with eggs remaining ({self.eggs})')
            # Simulate some work while holding the lock
            # sleep(0.01) # Small sleep to show lock effectiveness

        print(f'{ctime()} Kitchen-{index} : Chef-{index} has released lock with eggs remaining ({self.eggs})')


# chef cooking
def cooking(index, basket):
    # chef use eggs for cooking
    basket.use_eggs(index)
    sleep(2) # This sleep is outside the lock, which is good for parallelism

# Kitchen cooking
def kitchen(index, share_eggs):
    print(f'{ctime()} Kitchen-{index} : Begin cooking...PID ({os.getpid()})')
    cooking_time = time()
    cooking(index, share_eggs) # Pass the basket object
    duration = time() - cooking_time
    print(f'{ctime()} Kitchen-{index} : Cooking done in {duration:0.2f}s!')

if __name__ == "__main__":
    # Begin of main thread
    print(f'{ctime()} Main         : Start Cooking...PID ({os.getpid()})')
    start_time = time()

    basket = Basket() # Initialize Basket instance

    # Multi processes
    kitchens = list()
    for index in range(2): # Range was 2 in the image, assuming this is correct
        p = multiprocessing.Process(target=kitchen, args=(index, basket)) # Pass basket to the process
        kitchens.append(p)
        # starting processes
        p.start()

    for index, p in enumerate(kitchens):
        # wait until processes are finished
        p.join()

    print(f'{ctime()} Main         : Basket eggs remaining ({basket.eggs})') # Corrected: Access basket.eggs
    duration = time() - start_time
    print(f'{ctime()} Main         : Finished Cooking duration in {duration:0.2f} seconds')