import threading
import Motor_Logic, detect, timer_clr_sz_snr, spi_12_mean, timer_img_cap
# import utility.py # uncomment if needed
# import lemon_defect_v5.tflite # uncomment if needed

threading.active_count()
# try:
	# Thread.exit()
	# Thread(target=timer_img_cap.py).start() # run file in thread.  takes image for color and size code
	# Thread(target=timer_clr_sz_snr.py).start() # color and size determination
	# Thread(target=spi_12_mean.py).start() # weight sensor code
	# Thread(target=detect.py).start() # ML code. Quality determination
	# Thread(target=Motor_Logic.py).start() # PWM motor logic code
	# threading.Thread.start_new_thread(timer_img_cap, ("Thread-1"))
	# Thread.start_new_thread(timer_clr_sz_snr)
	# threading.enumerate() # check to make sure if threads are running
# except:
	# print("Error")
	# threading.Thread.exit()
