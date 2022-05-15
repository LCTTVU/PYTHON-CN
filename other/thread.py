import threading
t1 = threading.Thread(target=print, args=("Hello", "World"))
t2 = threading.Thread(target=print, args=("Hello2", "World2"))
t1.start()
t2.start()
t1.join(10)
t2.join(10)
