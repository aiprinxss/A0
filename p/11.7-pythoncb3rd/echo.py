from multiprocessing.connection import Client
c = Client(('localhost', 25000), authkey=b'1110')
c.send('hello')
c.recv()
c.send(42)
c.recv()
c.send([1, 2, 3, 4, 5])
c.recv()
