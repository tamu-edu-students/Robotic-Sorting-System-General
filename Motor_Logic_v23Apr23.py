import RPi.GPIO as GPIO # import global input and output library for raspberry pi
import time
GPIO.setmode(GPIO.BCM) # set pins to board pin layout
import threading
import json

databaseArray = [0, 0, 0, 1, 0]
currentBin = 0

def updateCheck(Conveyor_pwm, GA_left_pwm, GA_right_pwm, dc_c, dc_g):
	global databaseArray
	threading.Timer(61.0, updateCheck, [Conveyor_pwm, GA_left_pwm, GA_right_pwm, dc_c, dc_g]).start()
	databaseArray = databaseLoad()
	# print("Updated database array")
	# print(databaseArray)
	motorlogic(Conveyor_pwm, GA_left_pwm, GA_right_pwm, dc_c, dc_g) # variables passed into updatecheck are used in motorlogic

def databaseLoad():
    with open ("subsystem_connection.json", "r") as f:
        subsystem_connection = json.load(f)
    ctype = subsystem_connection["ctype"]
    cutoff1 = subsystem_connection["cutoff1"]
    cutoff2 = subsystem_connection["cutoff2"]
    belt = subsystem_connection["belt"]
    fruit =  subsystem_connection["fruit"]
    array = [ctype, cutoff1, cutoff2, belt, fruit]
    # print(array)
    # time.sleep(10)
    return array
    
def motorlogic(Conveyor_pwm, GA_left_pwm, GA_right_pwm, dc_c, dc_g):
	global currentBin
	global databaseArray
	if(databaseArray[3] == 1): # master on off from database (json) file
		# print("Global current bin: " + str(currentBin))
		
		# ctype is 3 for ML.  1 for good, 2 for bad
		# ctype is 1 for size.  1 for small, 2 for medium, 3 for large
		# ctype is 2 for color.  base it off cutoffs.  bin 1: less than or equal to cutoff 1.  bin 2: b/w cutoffs.  bin 3: greater than cutoff 2
		
		# print(databaseArray)
		
		fruit = databaseArray[4] # value to compare to cutoffs for ctype 1 and 2
		c1 = databaseArray[1] # cutoff 1
		c2 = databaseArray[2] # cutoff 2
		ctype = databaseArray[0]
		
		if (ctype == 1 or ctype == 2): # color or size sorting
			if (c2 > c1):
				if (fruit <= c1):
					nextBin = 0
				elif (fruit > c1 and fruit <= c2):
					nextBin = 1
				elif (fruit > c2):
					nextBin = 2
				else:
					print("Error with cutoffs")
			elif (c1 > c2):
				if (fruit <= c2):
					nextBin = 0
				elif (fruit > c2 and fruit <= c1):
					nextBin = 1
				elif (fruit > c1):
					nextBin = 2
				else:
					print("Error with cutoffs")
		elif (ctype == 3):
			if (fruit == 1):
				nextBin = 0
			elif (fruit == 2):
				nextBin = 1
			else:
				nextBin = 2
		else:
			print("Error with ctype")
			
		# nextBin = databaseArray[4] # grab bin location from database
		# print("Motor_Logic: ")
		print(databaseArray)
		# print("Next bin: " + str(nextBin) + " Current bin: " + str(currentBin)) # Note: cb was removed.  Using global current bin instead
		# GPIO.setup(in1, GPIO.OUT)
		# GPIO.setup(in2, GPIO.OUT)
		# GPIO.setup(in3, GPIO.OUT)
		# GPIO.setup(in4, GPIO.OUT)

		if (nextBin == 0):
			if (currentBin == 1): 
				GA_direction = 'Backward'
				# GPIO.output(in3, False)
				# GA_pwm = GPIO.PWM(in4, f_g)
				GA_right_pwm.start(100)
				time.sleep(0.55) # moves for set amount of seconds
				GA_right_pwm.stop()
				# cb = nextBin # set location to bin it moved to
				currentBin = nextBin
				
				Conveyor_pwm.start(100)
				time.sleep(60)
				Conveyor_pwm.stop()
			elif (currentBin == 2):
				GA_direction = 'Backward'
				# GPIO.output(in3, False)
				# GA_pwm = GPIO.PWM(in4, f_g)
				GA_right_pwm.start(100)
				time.sleep(0.5)
				GA_right_pwm.stop()
				currentBin = nextBin
				
				Conveyor_pwm.start(100)
				time.sleep(60)
				Conveyor_pwm.stop()
			elif (currentBin == 0): 
				# do nothing.  Guiding rails already at correct position
				currentBin = nextBin
				Conveyor_pwm.start(100)
				time.sleep(60)
				Conveyor_pwm.stop()
			else:
				print("ERROR: INVALID CURRENT BIN")
		elif (nextBin == 1):
			if (currentBin == 0):
				GA_direction = 'Forward'
				# GPIO.output(in4, False)
				# GA_pwm = GPIO.PWM(in3, f_g)
				GA_left_pwm.start(100)
				time.sleep(0.25)
				GA_left_pwm.stop()
				currentBin = nextBin
				
				Conveyor_pwm.start(100)
				time.sleep(60)
				Conveyor_pwm.stop()
			elif (currentBin == 2):
				GA_direction = 'Backward'
				# GPIO.output(in3, False)
				# GA_pwm = GPIO.PWM(in4, f_g)
				GA_right_pwm.start(100)
				time.sleep(0.25)
				GA_right_pwm.stop()
				currentBin = nextBin
				
				Conveyor_pwm.start(100)
				time.sleep(60)
				Conveyor_pwm.stop()
			elif (currentBin == 1):
				# do nothing.  Guiding rails already at correct position
				currentBin = nextBin
				Conveyor_pwm.start(100) # why wont this run?
				time.sleep(60)
				Conveyor_pwm.stop()
			else:
				print("ERROR: INVALID CURRENT BIN")
		elif (nextBin == 2):
			if (currentBin == 0): 
				GA_direction = 'Forward'
				# GPIO.output(in4, False)
				# GA_pwm = GPIO.PWM(in3, f_g)
				GA_left_pwm.start(100)
				time.sleep(0.5)
				GA_left_pwm.stop()
				currentBin = nextBin
				
				Conveyor_pwm.start(100)
				time.sleep(60)
				Conveyor_pwm.stop()
			elif (currentBin == 1):
				GA_direction = 'Forward'
				# GPIO.output(in4, False)
				#GA_left_pwm = GPIO.PWM(in3, f_g)
				GA_left_pwm.start(100)
				time.sleep(0.25)
				GA_left_pwm.stop()
				currentBin = nextBin
				
				Conveyor_pwm.start(100)
				time.sleep(60)
				Conveyor_pwm.stop()
			elif (currentBin == 2):
				# do nothing.  Guiding rails already at correct position
				currentBin = nextBin
				Conveyor_pwm.start(100)
				time.sleep(60)
				Conveyor_pwm.stop()
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
	
	Conveyor_pwm = GPIO.PWM(input_2, Conveyor_frequency) # had to setup PWM object before function because it did not like reinstantiating every time it looped
	GA_left_pwm = GPIO.PWM(input_3, GA_frequency)
	GA_right_pwm = GPIO.PWM(input_4, GA_frequency)
	updateCheck(Conveyor_pwm, GA_left_pwm, GA_right_pwm, Conveyor_duty_cycle, GA_duty_cycle)
	GPIO.cleanup()

if __name__ == "__main__":
    main()
