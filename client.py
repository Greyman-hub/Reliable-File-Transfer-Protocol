import socket
import os

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ("192.168.31.57", 9090)

filename = input("Enter file name: ")

received_file = "received_" + filename

offset = 0
if os.path.exists(received_file):
    offset = os.path.getsize(received_file)

request = f"REQUEST {filename} {offset}"
client.sendto(request.encode(), server_address)

data, _ = client.recvfrom(1024)
response = data.decode()

if response == "FILE_FOUND":

    print("Receiving file...")

    received = set()

    with open(received_file, "ab") as f:

        while True:
            packet, _ = client.recvfrom(2048)

            if packet.decode(errors="ignore") == "END":
                print("File transfer complete")
                break

            seq = int.from_bytes(packet[:4], 'big')

            if seq not in received:
                print("Received packet", seq)
                f.write(packet[4:])
                received.add(seq)

            client.sendto(f"ACK {seq}".encode(), server_address)

else:
    print("File not found")