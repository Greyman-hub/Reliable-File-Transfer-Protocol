import socket
import os
import threading
import json
import time
import random

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("0.0.0.0", 9090))

print("Server started on port 9090...")

stats_file = "stats.json"
lock = threading.Lock()

def load_stats():
    try:
        if os.path.exists(stats_file) and os.path.getsize(stats_file) > 0:
            with open(stats_file, "r") as f:
                return json.load(f)
    except json.JSONDecodeError:
        pass
    return {}

def save_stats(data):
    temp_file = stats_file + ".tmp"
    with open(temp_file, "w") as f:
        json.dump(data, f, indent=4)
    os.replace(temp_file, stats_file)


def handle_client(message, addr):

    client_id = f"{addr[0]}:{addr[1]}"

    if not message.startswith("REQUEST"):
        return

    parts = message.split()
    filename = parts[1]
    offset = int(parts[2]) if len(parts) > 2 else 0

    if not os.path.exists(filename):
        server.sendto("FILE_NOT_FOUND".encode(), addr)
        return

    server.sendto("FILE_FOUND".encode(), addr)
    print(f"{client_id} requested {filename}")

    stats = {
        "filename": filename,
        "packets_sent": 0,
        "retransmissions": 0,
        "packet_loss": 0,
        "transfer_time": 0
    }

    start_time = time.time()

    with open(filename, "rb") as f:

        f.seek(offset)
        seq = offset // 1024

        while True:
            chunk = f.read(1024)
            if not chunk:
                break

            packet = seq.to_bytes(4, 'big') + chunk

            print(f"[{client_id}] Sending packet {seq}")

            if random.random() < 0.1:
                print(f"[{client_id}] Packet {seq} lost")
                stats["packet_loss"] += 1
            else:
                server.sendto(packet, addr)
                stats["packets_sent"] += 1

            server.settimeout(2)

            while True:
                try:
                    ack, ack_addr = server.recvfrom(1024)

                    if ack_addr != addr:
                        continue  

                    ack_seq = int(ack.decode().split()[1])

                    if ack_seq == seq:
                        print(f"[{client_id}] ACK {seq}")
                        server.settimeout(None) 
                        break

                except socket.timeout:
                    print(f"[{client_id}] Resending packet {seq}")
                    server.sendto(packet, addr)
                    stats["retransmissions"] += 1

            seq += 1

    server.sendto("END".encode(), addr)

    stats["transfer_time"] = round(time.time() - start_time, 2)

    with lock:
        all_stats = load_stats()
        all_stats[client_id] = stats
        save_stats(all_stats)

    server.settimeout(None)

    print(f"Transfer complete for {client_id}")

while True:
    try:
        data, addr = server.recvfrom(1024)
        message = data.decode()

        threading.Thread(target=handle_client, args=(message, addr)).start()

    except socket.timeout:
        continue 

    except Exception as e:
        print("Server error:", e)