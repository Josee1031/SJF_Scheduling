import socket
import time
import random
import psutil  # To get system processes

def send_jobs_to_cluster(server_ip, server_port):
    processes = [p.info['name'] for p in psutil.process_iter(['name'])]
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((server_ip, server_port))  # Connect to the cluster

            for process in processes:
                cpu_time = random.randint(1, 5)  # Random CPU time (1-5 seconds)
                message = f"{process}:{cpu_time}"  # Format: ProcessName:CPUTime
                print(f"Sending job: {message}")
                
                try:
                    sock.sendall(message.encode())  # Send the job to the cluster
                except BrokenPipeError:
                    print("Error: Connection closed by server. Could not send job.")
                    break  # Stop sending if the connection is broken
                
                time.sleep(random.randint(1, 5))  # Random sleep between job sends
    
    except ConnectionRefusedError:
        print(f"Failed to connect to {server_ip}:{server_port}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python edevice.py <server_ip> <server_port>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    
    send_jobs_to_cluster(server_ip, server_port)
