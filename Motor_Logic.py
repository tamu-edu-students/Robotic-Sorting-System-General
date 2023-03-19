import RPi.GPIO as GPIO # import global input and output library for raspberry pi
import time
GPIO.setmode(GPIO.BCM) # set pins to board pin layout
import threading
import json

databaseArray = [0, 0, 0, 1, 0]
currentBin = 1

def updateCheck(in1, in2, in3, in4, dc_c, f_c, dc_g, f_g):
    threading.Timer(15.0, updateCheck, [in1, in2, in3, in4, dc_c, f_c, dc_g, f_g]).start()
    databaseArray = databaseLoad()
    print("Updated database array")
    print(databaseArray)
    motorlogic(in1, in2, in3, in4, dc_c, f_c, dc_g, f_g, databaseArray) # variables passed into updatecheck are used in motorlogic

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
    
def motorlogic(in1, in2, in3, in4, dc_c, f_c, dc_g, f_g, databaseArray):
	if(databaseArray[3] == 1): # master on off from database (json) file
		global currentBin
		# print("Global current bin: " + str(currentBin))
		nextBin = databaseArray[4] # grab bin location from database
		# print(databaseArray)
		# print("Next bin: " + str(nextBin) + " Current bin: " + str(cb)) # Note: cb was removed.  Using global current bin instead
		GPIO.setup(in1, GPIO.OUT)
		GPIO.setup(in2, GPIO.OUT)
		GPIO.setup(in3, GPIO.OUT)
		GPIO.setup(in4, GPIO.OUT)
		Conveyor_pwm = GPIO.PWM(in2, f_c)

		if (nextBin == 0):
			if (currentBin == 1): 
				GA_direction = 'Backward'
				GPIO.output(in3, False)
				GA_pwm = GPIO.PWM(in4, f_g)
				GA_pwm.start(dc_g)
				time.sleep(1) # moves for set amount of seconds
				GA_pwm.stop()
				# cb = nextBin # set location to bin it moved to
				currentBin = nextBin
				
				Conveyor_pwm.start(dc_c)
				time.sleep(5)
				Conveyor_pwm.stop()
			elif (currentBin == 2):
				GA_direction = 'Backward'
				GPIO.output(in3, False)
				GA_pwm = GPIO.PWM(in4, f_g)
				GA_pwm.start(dc_g)
				time.sleep(2)
				GA_pwm.stop()
				currentBin = nextBin
				
				Conveyor_pwm.start(dc_c)
				time.sleep(5)
				Conveyor_pwm.stop()
			elif (currentBin == 0): 
				# do nothing.  Guiding rails already at correct position
				currentBin = nextBin
			else:
				print("ERROR: INVALID CURRENT BIN")
		elif (nextBin == 1):
			if (currentBin == 0):
				GA_direction = 'Forward'
				GPIO.output(in4, False)
				GA_pwm = GPIO.PWM(in3, f_g)
				GA_pwm.start(dc_g)
				time.sleep(1)
				GA_pwm.stop()
				currentBin = nextBin
				
				Conveyor_pwm.start(dc_c)
				time.sleep(5)
				Conveyor_pwm.stop()
			elif (currentBin == 2):
				GA_direction = 'Backward'
				GPIO.output(in3, False)
				GA_pwm = GPIO.PWM(in4, f_g)
				GA_pwm.start(dc_g)
				time.sleep(2)
				GA_pwm.stop()
				currentBin = nextBin
				
				Conveyor_pwm.start(dc_c)
				time.sleep(5)
				Conveyor_pwm.stop()
			elif (currentBin == 1):
				# do nothing.  Guiding rails already at correct position
				currentBin = nextBin
			else:
				print("ERROR: INVALID CURRENT BIN")
		elif (nextBin == 2):
			if (currentBin == 0): 
				GA_direction = 'Forward'
				GPIO.output(in4, False)
				GA_pwm = GPIO.PWM(in3, f_g)
				GA_pwm.start(dc_g)
				time.sleep(1)
				GA_pwm.stop()
				currentBin = nextBin
				
				Conveyor_pwm.start(dc_c)
				time.sleep(5)
				Conveyor_pwm.stop()
			elif (currentBin == 1):
				GA_direction = 'Forward'
				GPIO.output(in4, False)
				GA_pwm = GPIO.PWM(in3, f_g)
				GA_pwm.start(dc_g)
				time.sleep(2)
				GA_pwm.stop()
				currentBin = nextBin
				
				Conveyor_pwm.start(dc_c)
				time.sleep(5)
				Conveyor_pwm.stop()
			elif (currentBin == 2):
				# do nothing.  Guiding rails already at correct position
				currentBin = nextBin
			else:
				print("ERROR: INVALID CURRENT BIN")
		else:
			print("ERROR: Invalid bin input")

def main():
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
	# Conveyor_direction = 'Backward'
	Conveyor_duty_cycle = 100 # duty cycle value of 0-100 set here and will remain constant
	Conveyor_frequency = 100000 # value must be between 20k and 100k hertz
	# Conveyor_pwm = GPIO.PWM(input_2, Conveyor_frequency) # frequency of input 1 will be assigned to pin 'input 1'

	# guiding arm values will depend on what bin the fruit needs to go to
	# GA_direction = 'Forward' # input('Forward or Backward: ') # setup as if inputting by keyboard for now
	GA_duty_cycle = 100 # input("Duty cycle: ")
	GA_frequency = 100000 # input("Freq. b/w 20k and 100k: ")
	
	# Note: don't need to input direction.  Just used to check if code is operating correctly

	# global currentBin # set initial position to 1 (middle...0 is left and 2 is right)
	# cb = 1

	updateCheck(input_1, input_2, input_3, input_4, Conveyor_duty_cycle, Conveyor_frequency, GA_duty_cycle, GA_frequency)

if __name__ == "__main__":
    main()
