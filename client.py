
import socket
import time
import struct
import getch
import string
import random
import _thread as thread
import signal

max_time = 10

def stop_s(signum,frame):
    raise OSError()
signal.signal(signal.SIGALRM, stop_s)


def main():
    bufferSize = 1024
    # Create a UDP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM , socket.IPPROTO_UDP)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    while True:

        try:
            time.sleep(2)
            client.bind(("", 14444))
        except:
            pass
        print(u"\u001B[33mClient started, listening for offer requests...\u001B[35m")
        t_end = time.time() + 10  
        while t_end > time.time(): # run for 10 second
            # Waiting for the first message
            first_massage, addr  = client.recvfrom(bufferSize)
            # Unpacked the received message
            try:
                unpacked_message = struct.unpack('Ibh', first_massage)
                # If the message type is 2, and the cookie is correct (the decimal value of 0xabcddcba)
                if unpacked_message[1] == 2 and unpacked_message[0] == 2882395322:  
                    # The port the clients will connect to in TCP connection
                    tcp_port = unpacked_message[2]  
                    print("“Received offer from " + addr[0] + ", attempting to connect...")
                    # Create the socket and connect to the TCP port received from the broadcast
                    ClientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                    ClientSock.connect((addr[0], tcp_port))
                    # Create the client's name
                    client_name = 'Bob Kahn' +"\n" 
                    # Send the name
                    ClientSock.send(client_name.encode())
                    try:
                        # Waiting for the start message
                        start_message = ClientSock.recv(bufferSize).decode()
                        if start_message != "":
                            print(start_message)
                            # Catch the client's input
                            try:
                                signal.alarm(max_time)
                                answer = getch.getch()
                                signal.alarm(0)
                                # Send the answer to the server
                                ClientSock.send(answer.encode()) 
                            except:
                                pass
                            # Waiting for the final message from the server
                            final_message = ClientSock.recv(bufferSize).decode()  
                            if final_message != "":
                                print(final_message)
                    except:
                        break
            except:
                print("Unpack Failed")
                continue
            

        print("Server disconnected, listening for offer requests...")

if __name__ == '__main__':
    main()
