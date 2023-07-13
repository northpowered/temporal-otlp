from multiprocessing import Process
import subprocess


if __name__=="__main__":        

    services: list = ['b', 'c', 'd', 'e', 'f']
    procs: list = []
    
    for s in services:
        procs.append(
            Process(target=subprocess.call,args=(["python3", f"service_{s}/separate_run.py"],))
        )

    for p in procs:
        p.start()
