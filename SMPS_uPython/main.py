#Imports
import machine          
from machine import Pin
from machine import PWM 
from time import sleep #for time delay
import network # for Wifi connection
import time
motion = True

#Declaring Pins
ir1=Pin(23,Pin.IN)  #1st IR Sensor Pin 23 for Entry Gate

ir2=Pin(26,Pin.IN)   #2nd IR Sensor Pin 26 for 1st Floor 1st Slot
ir3=Pin(27,Pin.IN)   #3rd IR Sensor PIN 27 for 1st Floor 2nd Slot
ir4=Pin(5,Pin.IN)    #4th IR Sensor PIN 05 for 2nd Floor 1st Slot
ir5=Pin(4,Pin.IN)    #5th IR Sensor PIN 04 for 2nd Floor 2nd Slot

ir6=Pin(19,Pin.IN)  #6th IR Sensor Pin 23 for Exit Gate
    
s1=Pin(22)         #1st Servo PIN 22 for Entry Gate
s2=Pin(18)         #1st Servo PIN 18 for Exit  Gate


#Servo Configuration
servo1 = machine.PWM(s1,90)	# We are calling machine lib for PWM
                            #function where we declare a degree and this PWM function will
                            #make sure it rotates for certain time that is in a predefined code
servo2 = machine.PWM(s2,90) #Initially it is set at 90 degrees

#Wifi Configuration
def wlan_connect(ssid,pwd):
    wlan = network.WLAN(network.STA_IF)
    if not wlan.active() or not wlan.isconnected():
        wlan.active(True)
        wlan.connect(ssid,pwd)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
wlan_connect('Krishna Vardhan', '123456789') #SSID Name, SSID Password
        
#Firebase Configuration
import ufirebase as firebase
firebase.setURL("https://smart-car-parking-system-5f623-default-rtdb.firebaseio.com/") #Google Realtime Firebase URL
        
firebase.put("SCPS", {"Slot1":  "Vacant",
                      "Slot2":  "Vacant",
                      "Slot21": "Vacant",
                      "Slot22": "Vacant"}, bg=0)
               
l={"Slot1":1,"Slot2":1,"Slot21":1,"Slot22":1} #Dictionary

while(True): #Infinite loop
    #Configuration of Entry Gate
    if(ir1.value()!=1): #If ir value is 0, the vehicle is present at entry gate
        print("Vehicle present at Entry Gate")
        servo1.duty(5)
        #sleep for 2 seconds
        time.sleep(2)
        #closing the gate
        servo1.duty(90)

    #Configuration for Slot 1 - 1st Floor
    x1=ir2.value()
    if(l["Slot1"]!= (x1)):
        if(x1==0):
            print("Vehicle present at Slot 1")
            firebase.put("SCPS", {"Slot1": "Occupied"}, bg=0)
        else:
            print("Vehicle not present at Slot1")
            firebase.put("SCPS", {"Slot1": "Vacant"}, bg=0)
        l["Slot1"]=x1
    
    #Configuration for Slot 2 - 1st Floor
    x2=ir3.value()
    if(l["Slot2"]!= (x2)):
        if(x2==0):
            print("Vehicle present at Slot2")
            firebase.put("SCPS", {"Slot2": "Occupied"}, bg=0)
        else:
            print("Vehicle not present at Slot 2")
            firebase.put("SCPS", {"Slot2": "Vacant"}, bg=0)
        l["Slot2"]=x2
        
    #Configuration for Slot 2 - 1st Floor
    x3=ir4.value()
    if(l["Slot21"]!= (x3)):
        if(x3==0):
            print("Vehicle present at Slot21")
            firebase.put("SCPS", {"Slot21": "Occupied"}, bg=0)
        else:
            print("Vehicle not present at Slot 21")
            firebase.put("SCPS", {"Slot21": "Vacant"}, bg=0)
    l["Slot21"]=x3
        
    #Configuration for Slot 2 - 1st Floor
    x4=ir5.value()
    if(l["Slot22"]!= (x4)):
        if(x4==0):
            print("Vehicle present at Slot22")
            firebase.put("SCPS", {"Slot22": "Occupied"}, bg=0)
        else:
            print("Vehicle not present at Slot 22")
            firebase.put("SCPS", {"Slot22": "Vacant"}, bg=0)
    l["Slot22"]=x4
    #Configuration of Exit Gate
    if(ir6.value()!=1):
        print("Vehicle present at Exit Gate")
        servo2.duty(220)
        #sleep for 2 seconds
        time.sleep(2)
        #closing the gate
        servo2.duty(150)
        
