import socket
import threading
import json
import time

class MinecraftServer:
    def __init__(self, host='0.0.0.0', port=25565):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        print(f'Server started on {host}:{port}')
        self.connections = []
        self.players = {}
        self.world_data = {}
        
    def handle_client(self, client_socket, address):
        print(f'Connection from {address} has been established!')
        self.connections.append(client_socket)
        player_id = len(self.players)
        self.players[player_id] = {
            'address': address,
            'socket': client_socket,
            'position': [0, 0, 0],
            'inventory': []
        }
        
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                
                message = json.loads(data.decode('utf-8'))
                print(f'Received from {address}: {message}')
                
                if message.get('type') == 'position_update':
                    self.players[player_id]['position'] = message.get('position')
                    self._broadcast_to_others(player_id, message)
                
                elif message.get('type') == 'block_place':
                    self._broadcast_to_all(message)
                
        except Exception as e:
            print(f'Error from {address}: {e}')
        finally:
            print(f'Connection from {address} has been closed.')
            client_socket.close()
            self.connections.remove(client_socket)
            if player_id in self.players:
                del self.players[player_id]
    
    def _broadcast_to_all(self, message):
        payload = json.dumps(message).encode('utf-8')
        for player_id, player in self.players.items():
            try:
                player['socket'].sendall(payload)
            except:
                pass
    
    def _broadcast_to_others(self, sender_id, message):
        payload = json.dumps(message).encode('utf-8')
        for player_id, player in self.players.items():
            if player_id != sender_id:
                try:
                    player['socket'].sendall(payload)
                except:
                    pass
    
    def start(self):
        while True:
            try:
                client_socket, address = self.server_socket.accept()
                client_handler = threading.Thread(
                    target=self.handle_client, 
                    args=(client_socket, address)
                )
                client_handler.daemon = True
                client_handler.start()
            except KeyboardInterrupt:
                print('Server shutting down...')
                break

if __name__ == '__main__':
    server = MinecraftServer()
    server.start()