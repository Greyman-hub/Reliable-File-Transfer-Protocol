# 📡 Reliable File Transfer Protocol (Custom FTP over UDP)

## 📖 Project Overview

This project implements a **Reliable File Transfer Protocol over UDP**, where a client requests files from a server and receives them reliably despite packet loss.

Since **UDP does not guarantee delivery**, this system implements reliability at the application layer using:

- Sequence numbers  
- Acknowledgments (ACKs)  
- Timeout-based retransmissions  

A **Streamlit dashboard** is also included to visualize real-time transfer statistics such as packet loss, retransmissions, and transfer performance.

---

## 🎯 Objectives

- Build a reliable data transfer system over UDP  
- Simulate core concepts of TCP reliability  
- Implement **Stop-and-Wait ARQ**  
- Simulate packet loss and recovery  
- Visualize performance using a dashboard  

---

## 🏗️ System Architecture

```
Client 1 ─┐
Client 2 ─┼──► Server (Multi-threaded)
Client 3 ─┘
                │
                ▼
        Independent Threads
                │
                ▼
         File Transfer + ARQ
                │
                ▼
         stats.json (per client)
                │
                ▼
        Streamlit Dashboard
```

---

## 👥 Multi-Client Support

The server supports multiple clients simultaneously using **thread-based concurrency**.

Each incoming client request is handled in a separate thread.


### How it works:
- Each client is identified using its IP and port (`IP:PORT`)
- Every client runs independently in its own thread
- File transfers occur concurrently without blocking other clients

### Statistics Handling:
- Each client has separate statistics stored in `stats.json`
- The dashboard displays per-client metrics such as:
  - Packets sent
  - Retransmissions
  - Packet loss
  - Transfer time

This ensures scalable handling of multiple clients and real-time monitoring.

## ⚙️ Features

- UDP-based client-server communication  
- Multi-client support using threading  
- File request system  
- Packetized file transfer (1024 bytes per packet)  
- Sequence numbering for reliability  
- Stop-and-Wait ARQ protocol  
- Timeout + retransmission mechanism  
- Packet loss simulation  
- Real-time statistics tracking  
- Interactive dashboard visualization  

---

## 🧰 Technologies Used

- **Python**  
- Socket Programming  
- **UDP Protocol**  
- **Streamlit** (for dashboard)  
- JSON (for statistics storage)  

---

## 🔄 How the Protocol Works

### 1. File Request
Client sends:

```
REQUEST <filename>
```


---

### 2. Server Response
Server replies:

```
FILE_FOUND
```

or

```
FILE_NOT_FOUND
```


---

### 3. Packetized Transfer
- File is divided into **1024-byte packets**
- Each packet contains:

```
[sequence_number] + data
```


---

### 4. Acknowledgment (ACK)
Client sends:

```
ACK <sequence_number>
```


---

### 5. Timeout & Retransmission
- If ACK is not received → packet is resent  
- Ensures reliable delivery  

---

### 6. Transfer Completion
Server sends:

```
END
```


---

## 📉 Packet Loss Simulation

The server intentionally drops packets:

```python
if random.random() < 0.3:
```

This simulates real network packet loss conditions.

---

# Dashboard

Displays real-time statistics for **multiple clients**, including:

* Packets sent
* Retransmissions
* Packet loss
* Transfer time

Run the dashboard using:

```
streamlit run dashboard.py
```

---

# How to Run

### 1. Start the Server

```
python server.py
```

### 2. Start the Dashboard

```
streamlit run dashboard.py
```

### 3. Run the Client

```
python client.py
```

Enter the filename when prompted.

---

# Conclusion

This project demonstrates how reliability can be implemented on top of UDP using application-layer techniques such as sequence numbers, acknowledgments, and retransmissions. The dashboard enhances understanding by providing real-time visualization of protocol performance.

---