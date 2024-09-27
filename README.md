# Shortest Job First Scheduling Simulation

This project simulates a **Shortest Job First (SJF) Scheduling Algorithm** in a distributed system consisting of an embedded device (producer) and a central computer cluster (server). The embedded device generates jobs that are too computationally heavy to be processed locally and sends them to the central cluster. The cluster schedules the jobs using the SJF algorithm, ensuring that jobs with the shortest execution time are processed first.

## Program Overview

### Components:
1. **Embedded Device (`edevice.py`)**: 
   - The producer node (embedded device) simulates job generation by sending process names and their corresponding CPU times (randomly generated) to the central cluster via TCP sockets.
   - There are two approaches:
     - **Regular Approach**: After sending each job, the embedded device sleeps for a random amount of time (1-5 seconds) before sending the next job.
     - **Bonus Approach**: Instead of sleeping, the embedded device waits for an acknowledgment from the cluster before sending the next job.
   
2. **Cluster (`cluster.py`)**: 
   - The server node (cluster) accepts jobs sent from the embedded device and queues them for execution. 
   - It uses two consumer threads to process the jobs based on the Shortest Job First (SJF) algorithm.
   - In the bonus implementation, the cluster also sends an acknowledgment back to the embedded device after receiving and queuing each job.

### Key Features:
- **Threads**: The cluster uses multiple threads (one for the producer and two for consumers) to handle job scheduling and execution concurrently.
- **Semaphores and Locks**: Semaphores are used to block the consumer threads when no jobs are available. A mutex (lock) is used to protect the shared job queue.
- **TCP Sockets**: TCP is used for communication between the embedded device and the cluster.

---

## How to Use the Program

### Prerequisites:
- **Python 3.x**
- **psutil** (for `edevice.py`) to gather system processes.

To install `psutil`:
```bash
pip install psutil
```

### Regular Implementation (Using Sleep):

1. **Run the Cluster Server (Cluster Node)**:
   - Open a terminal and navigate to the directory where `cluster.py` is located.
   - Run the cluster server using the following command:
   ```bash
   python3 cluster.py <server_port>
   ```
   - Replace `<server_port>` with an available port number (e.g., `65432`).
   - Example:
   ```bash
   python3 cluster.py 65432
   ```

2. **Run the Embedded Device (Producer Node)**:
   - Open a separate terminal and navigate to the directory where `edevice.py` is located.
   - Run the embedded device using the following command:
   ```bash
   python3 edevice.py <server_ip> <server_port>
   ```
   - Replace `<server_ip>` with the IP address of the machine running the cluster server. If the cluster is running on the same machine, use `127.0.0.1` (localhost).
   - Replace `<server_port>` with the port number used when running `cluster.py`.
   - Example:
   ```bash
   python3 edevice.py 127.0.0.1 65432
   ```

3. **Behavior**:
   - The embedded device sends jobs (processes with random CPU times) to the cluster server.
   - After sending each job, the embedded device sleeps for a random time between 1 and 5 seconds before sending the next job.
   - The cluster server schedules the jobs using the SJF algorithm and processes them with two consumer threads.

---

### Bonus Implementation (With Acknowledgment):

In the bonus implementation, the embedded device waits for an acknowledgment from the cluster after sending each job, rather than using a random sleep.

1. **Run the Cluster Server (Cluster Node)**:
   - Open a terminal and run the cluster server as described above:
   ```bash
   python3 cluster.py <server_port>
   ```

2. **Run the Embedded Device (Producer Node)**:
   - Run the embedded device with the same command:
   ```bash
   python3 edevice.py <server_ip> <server_port>
   ```

3. **Behavior**:
   - The embedded device sends jobs to the cluster and **waits for a response** from the cluster before sending the next job.
   - The cluster sends an acknowledgment back to the embedded device after each job is received and queued.

---

### Example Output

#### Cluster Server Output (Regular or Bonus Implementation):
```
Producer (head node) listening on port 65432
Connected by ('127.0.0.1', random_port)
Job added: top with CPU time 3
Job added: ls with CPU time 1
Consumer 1 is executing ls for 1 seconds.
Consumer 2 is executing top for 3 seconds.
Consumer 1 finished executing ls.
Consumer 2 finished executing top.
```

#### Embedded Device Output (Regular or Bonus Implementation):
```
Sending job: top:3
Sending job: ls:1
Sending job: cut:5
```

In the bonus version, you will also see acknowledgment messages:
```
Received acknowledgment: Job received
```

---

### Conclusion:
- The **regular implementation** uses `sleep()` to introduce random delays between job sends.
- The **bonus implementation** ensures more synchronization between the embedded device and the cluster, where the producer waits for an acknowledgment from the server before sending the next job.

---