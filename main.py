import sys, time
from network.peer import Peer
from util import upnp, crypto
hash = crypto.Crypto()

def encode_payload(data):
    enc_session_key, nonce, tag, ciphertext = hash.encrypt(data)
    return str({
        "enc_session_key": enc_session_key, 
        "nonce": nonce, 
        "tag": tag, 
        "ciphertext": ciphertext
    })

def decode_payload(data):
    import ast
    dic = ast.literal_eval(data.decode())
    text = hash.decrypt(dic)
    print(text)

def serverHandle(conn, payload):
    print(f'server Handle:')
    decode_payload(payload)

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
        client.request(encode_payload(" ".join(msg.split(" ")[2:])).encode())
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