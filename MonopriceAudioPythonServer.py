#!/usr/bin/env python
import socket
import logging
import serial
import sys
import threading

#TCP Server (socket) Settings
TCP_IP = '0.0.0.0' #Listen on all Raspberry Pi IP Addresses.
TCP_PORT = 4999 #Optionally you can set your own port number. 4999 is what the iTach flex uses, if you change this you NEED to change it in the android app settings
BUFFER_SIZE = 16  # Normally 1024, but we want fast response and dont need 1024 bytes

# Initialize Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((TCP_IP, TCP_PORT))
server_socket.listen(5)  # Allows up to 5 simultaneous connections in the backlog

# Serial Settings - configured just like we would if we had the iTach Flex
ser = serial.Serial()
ser.port = '/dev/ttyUSB0'
ser.baudrate = 9600
ser.timeout = .2 #this is the read timeout
ser.writeTimeout = 2
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.xonxoff = False #disable software flow control
ser.rtscts = False #disable hardware RTS/CTS flow control
ser.dsrdtr = False #disable hardware DSR/DTR flow control

#Logging settings
#logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/MonopriceAudioServer.log')

# Create a lock for the serial port
serial_lock = threading.Lock()

# Function to handle client connections
def handle_client(conn, addr):
    #print(f'Connection from address: {addr}')
    
    # Set a timeout for idle clients
    conn.settimeout(86400)  # Timeout after 86400 seconds (1 day) of inactivity

    try:
        while True:
            try:
                data = conn.recv(BUFFER_SIZE)
                if not data: 
                    break

                print("Received data:", data)

                # Ensure safe access to the serial port
                with serial_lock:
                    if not ser.is_open:
                        ser.open()

                    ser.flushInput()
                    ser.flushOutput()
                    ser.write(data)
                    response = ser.read(256)  # Read up to 256 bytes or until timeout

                # Send the serial response back to the client
                conn.send(response)

            except socket.timeout:
                print(f"Client at {addr} timed out due to inactivity.")
                break

    except Exception as e:
#       logging.error("Exception occurred", exc_info=True)
        print("Error:", str(e))

    finally:
        conn.close()
        print(f"Connection closed for {addr}")

# Main loop to accept multiple connections
try:
    while True:
        conn, addr = server_socket.accept()
        # Create a new thread for each client connection
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.daemon = True  # Daemon threads exit when the main program exits
        client_thread.start()

except KeyboardInterrupt:
    print("Exiting...")
    sys.exit(0)

finally:
    server_socket.close()
    if ser.is_open:
        ser.close()
