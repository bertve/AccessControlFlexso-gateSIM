#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#    Copyright 2014,2018 Mario Gomez <mario.gomez@teubi.co>
#
#    This file is part of MFRC522-Python
#    MFRC522-Python is a simple Python implementation for
#    the MFRC522 NFC Card Reader for the Raspberry Pi.
#
#    MFRC522-Python is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MFRC522-Python is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with MFRC522-Python.  If not, see <http://www.gnu.org/licenses/>.
#

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
from colored import fore, back,style

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

signal.signal(signal.SIGINT, end_read)

MIFAREReader = MFRC522.MFRC522()

# Welcome message
print (fore.WHITE + back.GREEN + style.BOLD)
print " _______________________________ "
print "|                               |"
print "|  Welcome to GATESIMBIRT v1.0  |"
print "|_______________________________|"                        
print "|             _____             |"
print "|            |\    |            |"
print "|            | \   |            |"
print "|            |  |  |            |"
print "|            | \|  |            |"
print "|            \  |__|            |"
print "|             \ |               |"
print "|              \|               |"
print "|                               |"
print "|     Press Ctrl-C to stop.     |"
print "|_______________________________|"
print (style.RESET)

while continue_reading:
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    if status == MIFAREReader.MI_OK:
        print "     ----Card detected----     "
    
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    if status == MIFAREReader.MI_OK:

        print ("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])+','+str(uid[4]))  
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)
        
        #Your Card UID
        my_uid = [74,222,187,18,61]
        

        #Configure GREEN LED Output Pin
        GREEN_LED = 18
        GPIO.setup(GREEN_LED, GPIO.OUT)
        GPIO.output(GREEN_LED, GPIO.LOW)
        
        #configure RED LED Output Pin
        RED_LED = 16
        GPIO.setup(RED_LED, GPIO.OUT)
        GPIO.output(RED_LED, GPIO.LOW)
        
        if uid == my_uid:
            print(fore.WHITE + back.GREEN )
            print "        ~ Access Granted ~        "
            
            GPIO.output(GREEN_LED, GPIO.HIGH) 
            print " +            GREEN LED           " 

            time.sleep(5)
            
            GPIO.output(GREEN_LED, GPIO.LOW)
            print " -            GREEN LED           "
            print (style.RESET)
            
        else:
            print(fore.WHITE + back.RED)
            print("Access Denied, YOU SHALL NOT PASS!")
            
            GPIO.output(RED_LED, GPIO.HIGH) 
            print " +           RED LED              " 

            time.sleep(5)
            
            GPIO.output(RED_LED, GPIO.LOW)
            print " -           RED LED              "
            print(style.RESET)
            
        print ""
        
##        # Authenticate
##        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
##
##        # Check if authenticated
##        if status == MIFAREReader.MI_OK:
##            MIFAREReader.MFRC522_Read(8)
##            MIFAREReader.MFRC522_StopCrypto1()
##        else:
##            print "Authentication error"

