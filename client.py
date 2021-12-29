import socket
import time
import struct
import getch
import string
import random
import _thread as thread

def main():
    bufferSize = 1024
    group_names = ['Turing','Bellman','Euclid','Pythagoras','Archimedes','Thales','Aristotle','Hipparchus','Antiphon','Newton','Einstein']
    # Create a UDP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM , socket.IPPROTO_UDP)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        time.sleep(2)
        client.bind(("", 13117))
    except:
        pass

    print(u"\u001B[33mClient started, listening for offer requests...\u001B[35m")
    t_end = time.time() + 10  
    while t_end > time.time(): # run for 10 second
        print("waiting for first mesg")
        # Waiting for the first message
        first_massage, addr  = client.recvfrom(bufferSize)
        print("received first mesg")
        print(first_massage)
        # Unpacked the received message
        try:
            unpacked_message = struct.unpack('Ibh', first_massage)
            print(unpacked_message)
      
            # If the message type is 2, and the cookie is correct (the decimal value of 0xabcddcba)
            if unpacked_message[1] == 2 and unpacked_message[0] == 2882395322:  
                # The port the clients will connect to in TCP connection
                tcp_port = unpacked_message[2]  
                print(unpacked_message)
                print("“Received offer from " + addr[0] + ", attempting to connect...")
                # try:
                #group_name = random.choice(group_names) # find random group name
                # Create the socket and connect to the TCP port received from the broadcast
                ClientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                print("why like this")
                ClientSock.connect((addr[0], tcp_port))
                # Create the client's name
                client_name = 'Bob Kahn' +"\n" 
                print(client_name)
                # Send the name
                ClientSock.send(client_name.encode())
                # except:
                #     break
                try:
                    print("waiting for start message")
                    # Waiting for the start message
                    start_message = ClientSock.recv(bufferSize).decode()
                    if start_message != "":
                        print(start_message)
                        # Catch the client's input
                        answer = getch.getch()
                        coded_answer = answer.decode('ASCII')
                        # Send the answer to the server
                        ClientSock.send(coded_answer.encode()) 
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
    while True:
        # Client go back to waiting for offer messages
        massage = client.recvfrom(bufferSize) 

if __name__ == '__main__':
    main()
