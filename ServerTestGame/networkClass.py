import socket
import pickle

class Network:
    def __init__(self, server_ip, server_port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (server_ip, server_port)
        self.id = self.connect()

    # Send data to server and receive response
    # The data parameter is expected to be a tuple (x, y) representing player position
    # The method returns the other player's position as a tuple (x, y)
    def send(self, data):
        try:
            self.client.sendto(pickle.dumps(data), self.server_address)
            response, _ = self.client.recvfrom(1024)
            return pickle.loads(response)
        except Exception as e:
            print(f"Network error: {e}")
            return None
        
    def resive(self):
        try:
            response = self.client.recv(1024)
            return pickle.loads(response)
        except Exception as e:
            print(f"Receive error: {e}")
            return None
        
    def connect(self):
        try:
            self.client.connect(self.server_address)
            return pickle.loads(self.client.recv(1024))
        except Exception as e:
            print(f"Connection error: {e}")
            return None
        


