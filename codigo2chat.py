from multiprocessing.connection import Client
from random import random
from time import sleep

from multiprocessing.connection import Listener
from multiprocessing import Process
import sys

def client_listener(info):
    print(f"Openning listener at {info}")
    cl = Listener(address=(info['address'],info['port']),authkey=info['authkey'])
    print ('.............client listener starting')
    print ('.............accepting conexions')
    while True:
        conn = cl.accept()
        print('.............conncetion accepted from', cl.last_accepted)
        m = conn.recv()
        print('.............messagereceived from server', m)
        
def main(server_address, info):
    print ('trying to connect')
    with Client(address=(server_address, 6000), authkey=b'secret password server') as conn:
        cl = Process(target=client_listener, args=(info,))
        cl.start
        conn.send(info)
        connected = True
        while connected:
            value = input("Send message ('quit' quit connection)?")
            print ("connection continued...")
            conn.send(value)
            connected = value!='quit'
        cl.terminate()
    print ("end client")
    
if __name__ == '__main__':
    server_address = '127.0.0.1'
    client_address = '127.0.0.1'
    client_port = 6001
    
    if len(sys.argv) > 1:
        client_port = int(sys.argv[1])
    if len(sys.argv) > 2:
        client_address = sys.argv[2]
    if len(sys.argv) > 3:
        server_address = sys.argv[3]
    info = {
            'address' : client_address,
            'port' : client_port,
            'authkey' : b'secret client server'
            }
    main(server_address, info)