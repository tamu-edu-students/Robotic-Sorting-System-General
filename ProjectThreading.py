from threading import Thread, enumerate
import Motor_Logic.py, detect.py, timer_clr_sz_snr.py, spi_12_mean.py, timer_img_cap.py
# import utility.py # uncomment if needed
# import lemon_defect_v5.tflite # uncomment if needed

Thread(target=timer_img_cap.py).start() # takes image for color and size code
Thread(target=timer_clr_sz_snr.py).start() # color and size code
Thread(target=spi_12_mean.py).start() # run weight sensor code
Thread(target=detect.py).start() # run object detection code in a thread.  Uses utility.py
Thread(target=Motor_Logic.py).start() # run motor logic code in a thread
enumerate() # check to make sure all the threads are running