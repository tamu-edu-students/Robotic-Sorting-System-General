import cv2
import numpy as np
import time
import json

num_sec = 5
#this program will determine the height, width, and color of the fruit
#this program will update the JSON file periodically
address = "/home/lifeofpi/BLEProject/subsystem_connection.json"

with open(address, "r") as f:      # read the json file   ##note, you have to change this address when working with the raspi
  variables = json.load(f)

error_message = "check for noise(dust, uneven lighting), the position of the fruit are not on the edge of the frame, there is only one fruit current within the frame"

while(True):
    image_bgr = cv2.imread('intg_test.jpg')
    #image_bgr = cv2.imread('/home/lifeofpi/ECEN_403/Cropped_real_lemon.jpg')
    #image_bgr = cv2.imread('/home/lifeofpi/ECEN_403/Cropped_lemon.jpg')
    gray_squ = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    gray_squ = cv2.fastNlMeansDenoising(gray_squ,None,10,7,21)
    kernel = np.ones((5,5),np.uint8)
    ret,thresh1 = cv2.threshold(gray_squ,140,255,cv2.THRESH_BINARY)
    thresh1 = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)

    ##oh no shiny spot on the conveyor belt
    result1 = cv2.bitwise_and(image_bgr, image_bgr, mask=thresh1)
    hsv_frame = cv2.cvtColor(result1, cv2.COLOR_BGR2HSV)
    low = np.array([0, 72, 0])
    high = np.array([179, 255, 255])
    mask = cv2.inRange(hsv_frame, low, high)
    #result1 = cv2.bitwise_and(image_bgr, image_bgr, mask=mask)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(150,150))
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    #result1 = cv2.bitwise_and(image_bgr, image_bgr, mask=closing)
    thresh1 = cv2.bitwise_and(thresh1, thresh1, mask=closing)
    #cv2.imshow("is there an item", thresh1)

    ##### fix this bug, where there is no fruit on the screen, there will be an error
    contours,hierarchy = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)   
    num_obj = len(contours)                          ###<------determines the number of fruits on the frame
    print("the nummber of object in the frame is ", num_obj)
    if num_obj != 0:
        obj_present = True
    else:
        obj_present = False
        
#####

    
    r = len(thresh1)
    c = len(thresh1[0])
    print(r)
    foundTop = False
    foundBottom = False
    foundLeft = False
    foundRight = False

    

    i = 0                                 #find top
    top = None
    while (foundTop == 0) and (i < r):
        arr = thresh1[i]
        is_all_zero = np.all((arr == 0))
        if is_all_zero:
            foundTop = False
            i = i + 1
        else:
            foundTop = True
            top = i

    #print("test")

    

    i = r - 1                            #find bottom
    bottom = None
    while (foundBottom == 0) and (i >= 0):
        arr = thresh1[i]
        is_all_zero = np.all((arr == 0))
        if is_all_zero:
            foundBottom = False
            i = i - 1
        else: 
            foundBottom = True
            bottom = i
    i = 0
    left = None                           #find left
    while (foundLeft == 0) and (i < c):
        arr = thresh1[:,i]
        is_all_zero = np.all((arr == 0))
        if is_all_zero:
            foundLeft = False
            i = i + 1
        else:
            foundLeft = True
            left = i
    i = c - 1
    right = None                                   #find right
    while (foundRight == 0) and (i >= 0):
        arr = thresh1[:,i]
        is_all_zero = np.all((arr == 0))
        if is_all_zero:
            foundLeft = False
            i = i - 1
        else:
            foundRight = True
            right = i

    crop_img = image_bgr[top:bottom, left:right]
    crop_hsv_frame = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
    crop_mask = thresh1[top:bottom, left:right]

    #if weird output, uncomment
    #cv2.imshow("cropped mask",crop_mask)
    #cv2.rectangle(image_bgr,(left,top),(right,bottom),(10,255,10),3)      #add a rectangle around the object
    #cv2.imshow("square_img",image_bgr)

    collect_hue = np.array([])

    i = 0
    j = 0
    
    ##a quick and dirty way to fix this but
    if obj_present:
        print("run the while loop")
        while i < (bottom - top):
            j = 0
            while j < (right - left):
                if crop_mask[i,j] == 255:
                    pixel = crop_hsv_frame[i, j]     ##you may able to simplify this
                    hue_value = pixel[0]
                    collect_hue = np.append(collect_hue, hue_value)
                j = j + 1
            i = i + 1
        col_median = np.median(collect_hue)
        color = "undefine"
        if col_median < 5:
            color = "RED"
            clr_num = 1
        elif col_median < 22:
            color = "ORANGE"
            clr_num = 2
        elif col_median < 33:
            color = "YELLOW"
            clr_num = 3
        elif col_median < 78:
            color = "GREEN"
            clr_num = 4
        elif col_median < 131:
            color = "BLUE"
            clr_num = 5
        elif col_median < 167:
            color = "VIOLET"
            clr_num = 6
        else:
            color = "RED"
            clr_num = 1

        print(color)
        pix_p_inch = 74.39758060582346                     ######note: change this after calibrating again
            #find the size of the object
        height_p = (bottom - top)
        #print("height by pixels: ", height_p)
        width_p = (right - left)
       #print("width by pixels: ", width_p)
        height = (bottom - top)/pix_p_inch
        print("height by inch: ", height)
        width = (right - left)/pix_p_inch
        print("width by inch: ", width)
        sensor_error = False    ##mostly false, may change because of the position of the object
        
    else:
        print("don't run the while loop")
        height = 0
        width = 0
        height_p = 0
        width_p = 0
        col_median = 0
        sensor_error = True
######before
        """
    while i < (bottom - top):
        j = 0
        while j < (right - left):
            if crop_mask[i,j] == 255:
                pixel = crop_hsv_frame[i, j]     ##you may able to simplify this
                hue_value = pixel[0] 
                collect_hue = np.append(collect_hue, hue_value)
            j = j + 1
        i = i + 1

    col_median = np.median(collect_hue)

    color = "undefine"
    if col_median < 5:
        color = "RED"
        clr_num = 1
    elif col_median < 22:
        color = "ORANGE"
        clr_num = 2
    elif col_median < 33:
        color = "YELLOW"
        clr_num = 3
    elif col_median < 78:
        color = "GREEN"
        clr_num = 4
    elif col_median < 131:
        color = "BLUE"
        clr_num = 5
    elif col_median < 167:
        color = "VIOLET"
        clr_num = 6
    else:
        color = "RED"
        clr_num = 1

    print(color)

    pix_p_inch = 74.39758060582346                     ######note: change this after calibrating again

    #find the size of the object
    height_p = (bottom - top)
    #print("height by pixels: ", height_p)
    width_p = (right - left)
    #print("width by pixels: ", width_p)
    height = (bottom - top)/pix_p_inch
    print("height by inch: ", height)
    width = (right - left)/pix_p_inch
    print("width by inch: ", width)
"""
    ###################################error message implemention

    #contours,hierarchy = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)   
    #num_obj = len(contours)                          ###<------determines the number of fruits on the frame
    print("number of stuff on the belt is:", num_obj)
    if sensor_error == True:
        print("ok, there is no object on the frame")
    elif top < 1 or bottom < 1 or left < 1 or right < 1:
        sensor_error = True
        print("the sensor error is", sensor_error)
        print(error_message)
    elif top > r-3 or bottom > r-3 or left > c-3 or right > c-3:
        sensor_error = True
        print("the sensor error is", sensor_error)
        print(error_message)
    ###check if the mulitple fruits or noise present, rememember this system is for lemon, lime, apples, but not big fruit, so if the width or height is more than
    elif width > 6 or height > 6:  ## 6 inches, there is probalby some weird stuff on the frame
        sensor_error = True
        print(error_message)
    elif num_obj == 0:
        sensor_error = True
        print("seem like there is no object on the frame")
    elif num_obj > 1:
        sensor_error = True
        print(error_message)
    else:
        print("seem like there is no error")



#####JSON implemending
    sort_num = variables["ctype"]
    fruit_reading = variables["fruit"]
   

    largest = height
    if height < width:
        largest = width
    

    #color outupt to the JSON file
    if sort_num == 2 and sensor_error == False:
        print("import color :", clr_num)
        fruit_reading = clr_num
        variables["fruit"] = fruit_reading
        with open(address, "w") as f:      # write back to the json file, 
            json.dump(variables, f)

    #size output to the JSON
    if sort_num == 1 and sensor_error == False:
        print("import size :", largest)
        #set the size tier
        #1 is small, 2 is medium, 3 is large
        small_t = variables["cutoff1"]
        big_t = variables["cutoff2"]
        if largest <= small_t:
            size_tier = 1
            print("size tier 1 ", small_t)
        elif small_t < largest and largest <= big_t:
            size_tier = 2
            print("size tier 2")
        else:
            size_tier = 3
            print("size tier 3")
        fruit_reading = size_tier
        variables["fruit"] = fruit_reading
        with open(address, "w") as f:      # write back to the json file
            json.dump(variables, f)


    #sensor error to the JSON
    if sensor_error == True:
        fruit_reading = 255
        print("there is an error, so fruit is set to 255")
        variables["fruit"] = fruit_reading
        with open(address, "w") as f:      # write back to the json file
            json.dump(variables, f)


 


    #may want to comment this out
    #if sort_num == 3:
     #   print("machine learning error")
    
    








    time.sleep(num_sec)

