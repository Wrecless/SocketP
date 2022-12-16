#threading handling
import threading

def function():
    for i in range(10):
        print(i)

def function2():
    for i in range(10):
        print("function2",i)

def function3():
    for i in range(10):
        print("function3",i)

#t1 = threading.Thread(target=function)
t2 = threading.Thread(target=function2)
t3 = threading.Thread(target=function3)

t1 = threading.Thread(target=function)
t1.start()
t1.join()
print("t1 is done")