import time
import thingspeak
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import json
import requests
# import Dummy_Driver_code
channel_id=1423651
write_key=''
read_key=''

TRIG1 = 23
ECHO1 = 24

TRIG2= 20
ECHO2=21


TRIG3=25
ECHO3=8

RED_LED=27
BLUE_LED=17

GPIO.setup(ECHO1,GPIO.IN)
GPIO.setup(TRIG1,GPIO.OUT)

GPIO.setup(ECHO2,GPIO.IN)
GPIO.setup(TRIG2,GPIO.OUT)

GPIO.setup(ECHO3,GPIO.IN)
GPIO.setup(TRIG3,GPIO.OUT)

GPIO.setup(27,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)


GPIO.output(27,GPIO.LOW)
GPIO.output(17,GPIO.LOW)
end=0
start=0
flag1=0 
flag2=0
flag3=0


# url='http://localhost:9000/saveSlot'
url='https://webhook.site/d58c0df6-6934-4e51-ba72-56769751751b'
print("Started")
# occupiedSlot= []
# unoccupiedSlot= []

def pingy1():
    GPIO.output(TRIG1, False)
    
    time.sleep(2)
    GPIO.output(TRIG1, True)
    time.sleep(0.00001)
    GPIO.output(TRIG1, False)
    pulse_start = 0
    pulse_end = 0
    while GPIO.input(ECHO1)==0:
        pulse_start = time.time()
    while GPIO.input(ECHO1)==1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance1 = pulse_duration * 17150
    distance1 = round(distance1, 2)
    print ("Distance1:",distance1,"cm")
    return distance1
    

    
 
     
print ("Reading Distance1 \n")

def pingy2():
    GPIO.output(TRIG2,False)
    
    time.sleep(2)
    GPIO.output(TRIG2,True)
    time.sleep(0.00001)
    GPIO.output(TRIG2,False)
    while GPIO.input(ECHO2)==0:
        pulse_start=time.time()
    while  GPIO.input(ECHO2)==1:
        pulse_end=time.time()
    pulse_duration=pulse_end-pulse_start
    distance2=pulse_duration *17150
    distance2=round(distance2,2)
    print("Distance2:",distance2,"cm")
    return distance2
print("Reading Distance2 \n")

def pingy3():
    GPIO.output(TRIG3, False)
    
    time.sleep(2)
    GPIO.output(TRIG3, True)
    time.sleep(0.00001)
    GPIO.output(TRIG3, False)
    while GPIO.input(ECHO3)==0:
        pulse_start = time.time()
    while GPIO.input(ECHO3)==1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance3 = pulse_duration * 17150
    distance3 = round(distance3, 2)
    print ("Distance3:",distance3,"cm")
    return distance3
print ("Reading Distance3 \n")
# message=""
 

def sensor():
    while True:
        dist1=pingy1()
        try:
            if(dist1 < 10 and flag1==0):
                GPIO.output(27,GPIO.HIGH)
                        
                GPIO.output(17,GPIO.LOW)
                
                # occupiedSlot.append(1002)
                # time.sleep(2)
                flag1=1
                # occupiedSlot.append(1001) 
                message="1"
                return message
            elif (dist1 > 10 and flag1==1):
                # print("unoccupiedslot")
                GPIO.output(27,GPIO.LOW)
                
                GPIO.output(17,GPIO.HIGH)
                
            #     # time.sleep(2)
                flag1=0
                count +=1
                message="0"

                return message
            # print(message)
            # unoccupiedSlot.append(1001)        
        except KeyboardInterrupt:
            GPIO.cleanup()


def measure(channel):
    
        status=sensor()
        # status=message
        response=channel.update({'field1':status})
        read=channel.get({})
        print("Read",read)
    



if __name__ == "__main__":

    channel = thingspeak.Channel(id=channel_id,api_key=write_key)         
    while True:
        measure(channel)
        time.sleep(15)
            # free account has an api limit of 15sec

            