import socket
import threading
import time
from threading import Semaphore, Lock

# Shared resources
job_queue = []  # List that holds the jobs (process, CPU time)
queue_lock = Lock()  # To synchronize access to the queue
job_available = Semaphore(0)  # Semaphore to block consumers when no jobs are available

class Producer(threading.Thread):
    """Head node that receives jobs from the embedded device and adds them to the queue."""

    def __init__(self, server_port):
        super().__init__()
        self.server_port = server_port

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(('0.0.0.0', self.server_port))
            server_socket.listen()
            print(f"Producer (head node) listening on port {self.server_port}")

            while True:
                conn, addr = server_socket.accept()  # Accept a connection from the embedded device
                print(f"Connected by {addr}")
                with conn:
                    try:
                        while True:
                            data = conn.recv(1024)  # Receive job data
                            if not data:
                                print("No more data received. Closing connection.")
                                break  # Exit if no more data is received
                            self.process_job(data.decode())

                    except Exception as e:
                        print(f"Error in receiving data: {e}")
                    finally:
                        conn.close()  # Ensure the connection is closed properly

    def process_job(self, job_message):
        """Extracts the job details and adds it to the shared queue."""
        global job_queue
        process, cpu_time = job_message.split(':')
        cpu_time = int(cpu_time)

        with queue_lock:
            job_queue.append((process, cpu_time))
            job_queue.sort(key=lambda x: x[1])  # SJF: Sort by CPU time
            print(f"Job added: {process} with CPU time {cpu_time}")

        job_available.release()  # Notify a consumer that a job is available


class Consumer(threading.Thread):
    """Compute node that consumes jobs from the queue and executes them."""
    
    def __init__(self, consumer_id):
        super().__init__()
        self.consumer_id = consumer_id

    def run(self):
        while True:
            job_available.acquire()  # Block until a job is available in the queue

            with queue_lock:
                process, cpu_time = job_queue.pop(0)  # Get the job with the shortest CPU time

            print(f"Consumer {self.consumer_id} is executing {process} for {cpu_time} seconds.")
            time.sleep(cpu_time)  # Simulate job execution
            print(f"Consumer {self.consumer_id} finished executing {process}.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python cluster.py <server_port>")
        sys.exit(1)

    server_port = int(sys.argv[1])

    # Create and start the producer (head node) thread
    producer = Producer(server_port)
    producer.start()

    # Create and start two consumer threads
    consumers = [Consumer(1), Consumer(2)]
    for consumer in consumers:
        consumer.start()

    # Prevent the main thread from exiting
    producer.join()
    for consumer in consumers:
        consumer.join()
