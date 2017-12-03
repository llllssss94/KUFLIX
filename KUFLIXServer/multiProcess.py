from multiprocessing import Process
import test as t
import os

def info(title):
    print(title)
    print("module name : ", __name__)
    print("parent process : ", os.getppid())
    print("process id : ", os.getpid())

def f(name):
    info("function f")
    print("hello", name)


if __name__ == "__main__":
    t.info("main line")
    for i in range(0, 2):
        p = Process(target = t.f, args = ("bob", ))
        p.start()
        p.join()