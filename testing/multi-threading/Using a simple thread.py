import threading
import time

def sleeper():
    print("Hi, I'm a Thread. Going to sleep for 5 sec.")
    time.sleep(5)
    print("I'm up from my nap")

t = threading.Thread(target=sleeper)
t.start()


print("This")
print("Is")
print("Doing")
print("Stuff")
print("While")
print("It's")
print("On")
print("A")
print("time.sleep")



