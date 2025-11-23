import socket
import threading  
import pickle  
from settings import *
import subprocess
import miniupnpc


server_ip = "192.168.1.250"
port = 5555

# firewall rule to allow incoming connections on the specified port
rule_name = "MyGameServer"

subprocess.run(
    f'netsh advfirewall firewall add rule '
    f'name="{rule_name}" dir=in action=allow protocol=TCP localport={port}',
    shell=True
)

# Set up UPnP port forwarding
upnp = miniupnpc.UPnP()
upnp.discover()
upnp.selectigd()

external_port = 5555
internal_port = 5555

upnp.addportmapping(
    external_port, 'TCP',
    upnp.lanaddr, internal_port,
    'MyGameServer', ''
)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server_ip, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Server started and listening on port:", port)

def handle_client(conn, addr, player_id): 
    print(f"New connection from {addr} as Player {player_id}")
    if player_id == 1:
        starting_pos = player_positions[0]
        color = colors[0]
    else:
        starting_pos = player_positions[1]
        color = colors[1]
    conn.send(pickle.dumps(player_id))  # Send player ID to client

    conn.send(pickle.dumps({"color": color,
                            "position": starting_pos}))  # Send color and starting position to client

    while True:
        try:
            data, _ = conn.recvfrom(1024)
            if not data:
                print(f"Player {player_id} disconnected")
                break
            data = pickle.loads(data)
            # data is expected to be a tuple (x, y)
            # and contains the player's current position
            # we update the global variable layer_positions which contains the positions of both players
            #  and send back the other player's position
            player_positions[player_id - 1] = data  # Update player position
            if player_id == 1:
                other_player_pos = player_positions[1]
                other_player_color = colors[1]
            else:
                other_player_pos = player_positions[0]
                other_player_color = colors[0]

            conn.send(pickle.dumps({"color": other_player_color,
                                    "position": other_player_pos}))  # Send other player's info

        except Exception as e:
            print(f"Error with Player {player_id}: {e}")
            break

    conn.close()

current_player = 1
colors = [WHT, BLU, RED, BLK] # Colors

player_positions = [(100, 100), (W-100-RectW, 100)]  # Initial positions for players

while True:
    conn, addr = s.accept()
    threading.Thread(target=handle_client, args=(conn, addr, current_player)).start()
    current_player = 1 + (current_player % 2)  # Alternate between 1 and 2
