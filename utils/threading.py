from threading import Thread

def run_in_thread(target, *args):
    thread = Thread(target=target, args=args)
    thread.start()
