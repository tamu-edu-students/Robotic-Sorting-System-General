import RPi.GPIO as GPIO # import global input and output library for raspberry pi
import time
GPIO.setmode(GPIO.BCM) # set pins to board pin layout

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
Conveyor_direction = 'Backward' # assumed to always move forward
Conveyor_duty_cycle = 0 # duty cycle value of 0-100 set here and will remain constant
Conveyor_frequency = 100000 # value must be between 20k and 100k hertz
Conveyor_pwm = GPIO.PWM(input_2, Conveyor_frequency) # frequency of input 1 will be assigned to pin 'input 1'

# guiding arm values will depend on what bin the fruit needs to go to
# cases will be added for each bin
GA_direction = 'Forward' # input('Forward or Backward: ') # setup as if inputting by keyboard for now
                                              # in the future will be setup for input from sensors
                                              # for all values
GA_duty_cycle = 100 # input("Duty cycle: ")
GA_frequency = 100000 # input("Freq. b/w 20k and 100k: ")
# GA_pwm = 0
if (GA_direction == 'Forward'):
    print("Guiding Arm set to FORWARD at a duty cycle of "+ str(GA_duty_cycle) + " percent and a frequency of "+ str(GA_frequency))
    # print statement to check direction and other values
    GPIO.output(input_4, False)
    GA_pwm = GPIO.PWM(input_3, GA_frequency)
elif (GA_direction == 'Backward'):
    print('Guiding Arm set to BACKWARD at a duty cycle of '+ str(GA_duty_cycle) + ' percent and a frequency of '+ str(GA_frequency))
    # Check set to backward
    GPIO.output(input_3, False)
    GA_pwm = GPIO.PWM(input_4, GA_frequency)
else:
    # if it receives an incorrect input then the current program stops and resets all
    print('ERROR: incorrect direction inputed')
    GA_pwm.stop()
    GPIO.cleanup()

# following code is for testing purposes
try:
    # while True: # set up different cases for each bin in the future
        print('Trying BELT START')
        Conveyor_pwm.start(Conveyor_duty_cycle)
        print('CONVEYOR BELT STARTED')
        GA_pwm.start(GA_duty_cycle)
        print('GUIDING BELT STARTED')
        time.sleep(60) # sleep for one minute
        # print('Slept for one second')
        GA_pwm.stop()
        Conveyor_pwm.stop()
        GPIO.cleanup()
except KeyboardInterrupt(): # good for testing but will not be used in final code
        GA_pwm.stop()
        # sleep()
        Conveyor_pwm.stop()
        GPIO.cleanup()
