import socket, sys
import threading
class Peer(threading.Thread):

    def __init__(self, flag='client', host = socket.gethostname(), port=1800, handler = None):
        self.flag = flag
        self.headersize = 10240
        self.host = host
        self.port = port
        self.handler = handler
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if flag != 'client':
            self.sock.bind((self.host, self.port))
        threading.Thread.__init__(self)

    def request(self, data):
        sock = socket.create_connection((self.host, self.port))
        sock.send(data)
        data = sock.recv(self.headersize)
        self.handler(self.sock, data)
        sock.close()
        
    def serve(self):
        self.sock.listen()                 # Now wait for client connection.
        while True:
            try:
                conn, addr = self.sock.accept()     # Establish connection with client.
                conn.send('Thanks for connecting'.encode())
                data = conn.recv(self.headersize)
                self.handler(conn, data)
            except Exception as err:
                return err
                

    def terminate(self):
        self.sock.shutdown(0)

    
    def run(self):
        if self.flag != "client":
            err = self.serve()
            print(err)