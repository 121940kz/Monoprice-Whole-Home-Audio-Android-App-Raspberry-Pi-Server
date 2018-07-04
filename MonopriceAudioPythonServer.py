# !/usr/bin/env python
import socket
import logging
import serial

#TCP Server (socket) Settings
TCP_IP = '172.16.186.225' #Configure this with YOUR Raspberry Pi IP Address
TCP_PORT = 4999 #Optionally you can set your own port number. 4999 is what the iTach flex uses, if you change this you NEED to change it in the android app settings
BUFFER_SIZE = 16  # Normally 1024, but we want fast response and dont need 1024 bytes

#Socket Settings
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

#Logging settings
logging.basicConfig(format='%(asctime)s %(message)s', filename='/home/pi/MonopriceAudioServer.log')

#We want this loop to run forever, so it will always be ready to accept a connection
while 1:
    try:
        #Wait for a connection to come through from a client (A.K.A the monoprice android app)
        conn, addr = s.accept()

        #print('Connection from address:', addr)

        while 1:

            data = conn.recv(BUFFER_SIZE)

            #If data received is an emtpy string, then break out of this inner loop and wait for another connection
            if not data: break

            #print("received data:", data)

            #WE HAVE THE DATA RECEIVED, NOW SEND IT OVER THE SERIAL CONNECTION
            # Serial Settings - configured just like we would if we had the iTach Flex
            ser = serial.Serial()
            ser.port = '/dev/ttyUSB0'
            ser.baudrate = 9600
            ser.timeout = .1 #this is the read timeout
            ser.writeTimeout = 2
            ser.bytesize = serial.EIGHTBITS
            ser.parity = serial.PARITY_NONE
            ser.stopbits = serial.STOPBITS_ONE
            ser.xonxoff = False #disable software flow control
            ser.rtscts = False #disable hardware RTS/CTS flow control
            ser.dsrdtr = False #disable hardware DSR/DTR flow control
            if(ser.isOpen() == False)
                ser.open()
            ser.flushInput()
            ser.flushOutput()
            ser.write(data)
            response = ser.read(256) #read 256 bytes or until the ser.timeout value is reached (it will always be the timeout)
            #SENDING COMPLETE - SEND BACK DATA RESPONSE THAT WAS RETURNED FROM SERIAL CONNECTION

            # Send data back to the connected client
            conn.send(data)

    except Exception as e:
        #Log the error so we could go back and see what might have happened
        logging.error(e.__doc__)
        logging.error(e.message)

        #Continue with the loop to accept connections if an error occurs
        continue
    finally:
        #Always close the current connection so we can wait for another
        conn.close()
        ser.close()
