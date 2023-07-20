from multiprocessing import Process
import subprocess


if __name__== "__main__":

    services: list = ['a', 'b', 'c', 'd', 'e', 'f']
    procs: list = []
    
    for s in services:
        procs.append(
            Process(target=subprocess.call,args=(["python3", f"src/service_{s}/separate_run.py"],))
        )

    for p in procs:
        p.start()
