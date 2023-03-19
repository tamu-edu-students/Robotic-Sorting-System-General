import RPi.GPIO as GPIO # import global input and output library for raspberry pi
import time
GPIO.setmode(GPIO.BCM) # set pins to board pin layout
import threading
import json

databaseArray = []

def updateCheck():
    threading.Timer(5.0, updateCheck).start()
    databaseArray = databaseLoad()

def databaseLoad():
    with open ("subsystem_connection.json", "r") as f:
        subsystem_connection = json.load(f)
    ctype = subsystem_connection["ctype"]
    cutoff1 = subsystem_connection["cutoff1"]
    cutoff2 = subsystem_connection["cutoff2"]
    belt = subsystem_connection["belt"]
    fruit =  subsystem_connection["fruit"]
    array = [ctype, cutoff1, cutoff2, belt, fruit]
    return array

# connveyor belt inputs
input_1 = 12 # Raspberry Pi 4 PWM0, pin 12
input_2 = 18 # PWM0 pin 18 

GPIO.setup(input_1, GPIO.OUT) # setup pin 12 as output
GPIO.setup(input_2, GPIO.OUT) # setup pin 18 as output
# guiding arm inputs
input_3 = 13 # PWM1, pin 13
input_4 = 19 # PWM1, pin 19

GPIO.setup(input_3, GPIO.OUT) # setup pin 13 as output
GPIO.setup(input_4, GPIO.OUT) # setup pin 19 as output

# conveyor belt values will be constant
Conveyor_direction = 'Forward' # assumed to always move forward
Conveyor_duty_cycle = 80 # duty cycle value of 0-100 set here and will remain constant
Conveyor_frequency = 30000 # value must be between 20k and 100k hertz
Conveyor_pwm = GPIO.PWM(input_1, Conveyor_frequency) # frequency of input 1 will be assigned to pin 'input 1'

# guiding arm values will depend on what bin the fruit needs to go to
GA_direction = 'Forward' # input('Forward or Backward: ') # setup as if inputting by keyboard for now
GA_duty_cycle = 80 # input("Duty cycle: ")
GA_frequency = 30000 # input("Freq. b/w 20k and 100k: ")

currentBin = 1 # set initial position to 1 (middle...0 is left and 2 is right)

# ----------------------------------------------------------------------------------------------------------------
while(databaseArray[3] == 1): # master on off from database (json) file
    nextBin = databaseArray[4] # grab bin location from database

    if (nextBin == 0):
        if (currentBin == 1): 
            GA_direction = 'Backward'
            GPIO.output(input_3, False)
            GA_pwm = GPIO.PWM(input_4, GA_frequency)
            GA_pwm.start(GA_duty_cycle)
            time.sleep(5) # moves for 5 seconds
            GA_pwm.stop()
            currentBin = nextBin # set location to bin it moved to
        elif (currentBin == 2):
            GA_direction = 'Backward'
            GPIO.output(input_3, False)
            GA_pwm = GPIO.PWM(input_4, GA_frequency)
            GA_pwm.start(GA_duty_cycle)
            time.sleep(10) # moves for 10 seconds
            GA_pwm.stop()
            currentBin = nextBin
        elif (currentBin == 0): 
            # do nothing.  Guiding rails already at correct position
            currentBin = nextBin
        else:
            print("ERROR: INVALID CURRENT BIN")
    elif (nextBin == 1):
        if (currentBin == 0):
            GA_direction = 'Forward'
            GPIO.output(input_4, False)
            GA_pwm = GPIO.PWM(input_3, GA_frequency)
            GA_pwm.start(GA_duty_cycle)
            time.sleep(5) # moves for 5 seconds
            GA_pwm.stop()
            currentBin = nextBin
        elif (currentBin == 2):
            GA_direction = 'Backward'
            GPIO.output(input_3, False)
            GA_pwm = GPIO.PWM(input_4, GA_frequency)
            GA_pwm.start(GA_duty_cycle)
            time.sleep(5) # moves for 5 seconds
            GA_pwm.stop()
            currentBin = nextBin
        elif (currentBin == 1):
            # do nothing.  Guiding rails already at correct position
            currentBin = nextBin
        else:
            print("ERROR: INVALID CURRENT BIN")
    elif (nextBin == 2):
        if (currentBin == 0): 
            GA_direction = 'Forward'
            GPIO.output(input_4, False)
            GA_pwm = GPIO.PWM(input_3, GA_frequency)
            GA_pwm.start(GA_duty_cycle)
            time.sleep(5) # moves for 5 seconds
            GA_pwm.stop()
            currentBin = nextBin
        elif (currentBin == 1):
            GA_direction = 'Forward'
            GPIO.output(input_4, False)
            GA_pwm = GPIO.PWM(input_3, GA_frequency)
            GA_pwm.start(GA_duty_cycle)
            time.sleep(5) # moves for 10 seconds
            GA_pwm.stop()
        elif (currentBin == 2):
            # do nothing.  Guiding rails already at correct position
            currentBin = nextBin
        else:
            print("ERROR: INVALID CURRENT BIN")
    else:
        print("ERROR: Invalid bin input")
