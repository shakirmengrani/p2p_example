import sys, time
from network.peer import Peer
from util import upnp, pack
from protos import header_pb2

message_pack = pack.Pack(header_pb2.Chunk())

def serverHandle(conn, payload):
    print(f'server Handle:')
    print(message_pack.unpack(payload))
    
    # decode_payload(payload)

def clientHandle(sock, payload):
    print(f'client Handle:')
    print(payload)

PORT = int(sys.argv[1])
server = Peer(flag="server", port=PORT, handler=serverHandle)
client = Peer(flag="client", port=PORT, handler=clientHandle)

def action(msg):
    s = time.time()
    if msg == "start advertising":
        try:
            print("Opening port...")
            print("Success:", upnp.ask_to_open_port(PORT, "xxHackxx", protos=["TCP", "UDP"]))
            print("Done in", time.time() - s)
        except:
            print("Your router may have disabled / blocked UPnP service")
    elif msg == "stop advertising":
        try:
            print("Closing port...")
            print("Success:", upnp.ask_to_close_port(PORT, "xxHackxx", protos=["TCP", "UDP"]))
            print("Done in", time.time() - s)
        except:
            print("Your router may have disabled / blocked UPnP service")
    elif "send message" in msg: 
        client.request(message_pack.pack(" ".join(msg.split(" ")[2:])))
    elif msg == "quit":
        server.terminate()
        print("bye bye")
        exit(0)

if "__main__" == __name__:
    server.start() 
    time.sleep(1)
    while True:
        msg = input("xxHackxx: >")
        action(msg)