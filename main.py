#! /usr/bin/env python

import serial
import io
import time

#Import the function that will output the image
import image_generator


#Launch the 30*30 scan once synced
def scan():
    #Change the /dev/ttyACM0 according to your tty device
    #It could be /dev/ttyUSB0 for a arduino mini
    #This is with an arduino mega
    usbSerial = serial.Serial('/dev/ttyACM0', 115200)
    result = []
    print 'Syncing the arduino... You may need to reset it'
    tmp = usbSerial.readline()
    while tmp != 'Parsing:\n':
        tmp = usbSerial.readline()
    print 'launching the scan!'
    usbSerial.write('IMG')
    for x in range (0, 30):
        line = []
        for y in range (0, 30):
            tmp = usbSerial.readline()
            print int(tmp)
            line.append(int(tmp))
        result.append(line)
    print 'Done scanning!'
    #Create the output.pgm file of the image
    image_generator.save_to_pgm(result)




#Will be launched only if we execute this file
if __name__ == '__main__':
    print 'Pres s to scan, anything else to launch tests'
    ch = raw_input()
    if ch == 's':
        print 'Perfoming complete scan'
        scan()
    else:
        #Testing stuff for debuging serial communication
        usbSerial = serial.Serial('/dev/ttyACM0', 115200)
        #usbIo = io.TextIOWrapper(io.BufferedRWPair(usbSerial, usbSerial))
        print "Testing the program"
        while True:
            the_line = usbSerial.readline()
            print "la ligne  est:"
            print '--' + the_line + '--'

            if the_line == 'Parsing:\n':
                print "Arduino found, scanning"
                for i in range(0,10):
                    print "Sending move order:"
                    usbSerial.write("MOVE")
                    print usbSerial.readline() #"Moving, give horizontal move"

                    print "Sending h move value:"
                    move = i * 10 + 10
                    usbSerial.write(str(move))
                    print usbSerial.readline() # "the move number, starting at 10

                    print "Sending v move value:"
                    usbSerial.write('40')
                    print usbSerial.readline()#the h move number, alway 40

                    print "Receiving 2 confirmation:"
                    #print usbSerial.readline() # "Moved" confirmation
                    print usbSerial.readline() # "Parsing:"

                    #time.sleep(0.2)
                    print "Sending scan command:"
                    usbSerial.write("SCAN")
                    print usbSerial.readline() # Print the distance
                    print "One scan move completed, printing confirmation"
                    print usbSerial.readline()
