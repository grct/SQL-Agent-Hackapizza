import threading

from src.settings import vn

sem = threading.Semaphore()

def fun(query):
    sem.acquire()
    res = vn.ask(query)
    sem.release()
    return res

