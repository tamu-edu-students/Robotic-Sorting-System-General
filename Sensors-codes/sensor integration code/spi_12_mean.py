import spidev
import RPi.GPIO as GPIO
import time
import os
import numpy as np
import math

spi = spidev.SpiDev()
spi.open(0,0)
#spi.mode = 0b00
spi.max_speed_hz=1000000


import json
address = "/home/lifeofpi/BLEProject/subsystem_connection.json"
with open(address, "r") as f:      # read the json file
 variables = json.load(f)

#from digtial to analog
def covDtoA(dig_val):
    volt = (dig_val*3.3)/4095
    return volt

#output pounds
# def convPounds(dig_val):

ch0 = 0
datalist1 =[0,0,0,0,0,0,0,0,0,0,0,0]
datalist2 =[0,0,0,0,0,0,0,0,0,0,0,0]
datalist3 =[0,0,0,0,0,0,0,0,0,0,0,0]

def adddata(datalist, input):
    i = len(datalist)-2
    while i >= 0:
        datalist[i+1] = datalist[i]
        i = i-1
    datalist[0] = input
    return datalist
i = 0

while True:
    #read output from the load cell
    
    ####### for the first load cell connected to channel 3
    rec_data3 = spi.xfer2([6,128,0])
    load_cell_val3 = ((rec_data3[1]&15) << 8) + rec_data3[2]
    
    
    ####### for the second load cell connected to channel 1
    rec_data1 = spi.xfer2([6,0,0])
    load_cell_val1 = ((rec_data1[1]&15) << 8) + rec_data1[2]
    
    ####### for the third load cell connected to channel 2
    rec_data2 = spi.xfer2([6,64,0])
    load_cell_val2 = ((rec_data2[1]&15) << 8) + rec_data2[2]
    
    #load_cell_volt = covDtoA(load_cell_val)
    datalist1 = adddata(datalist1, load_cell_val1)
    #avg_list = np.mean(datalist)
    datalist2 = adddata(datalist2, load_cell_val2)
    datalist3 = adddata(datalist3, load_cell_val3)
    
    avg_list1 = np.mean(datalist1)
    avg_list2 = np.mean(datalist2)
    avg_list3 = np.mean(datalist3)
    new_val1 = math.floor(avg_list1/16)
    new_val2 = math.floor(avg_list2/16)
    new_val3 = math.floor(avg_list3/16)



    #print output
    print("load cell1 ADC output: ", load_cell_val1 )
    print("list of prev 12 data: ", datalist1)
   # print("test load cell Volt: ", load_cell_volt,"V")
    print("the mean of the list1: ", avg_list1)
    
    #print("load cell2 ADC output: ", load_cell_val2 )
    print("list of prev 12 data: ", datalist2)
    print("the mean of the list2: ", avg_list2)
    
    #print("load cell3 ADC output: ", load_cell_val3 )
    print("list of prev 12 data: ", datalist3)
    print("the mean of the list3: ", avg_list3)
    print("new val 1 ", new_val1)
    print("new val 2 ", new_val2)
    print("new val 3 ", new_val3)
    
    variables["weight1"] = new_val1
    variables["weight2"] = new_val2
    variables["weight3"] = new_val3
    
    if i > 13:
        with open(address, "w") as f:      # write back to the json file
            json.dump(variables, f)
        i = 0
        print("json file updated")
    else:
        i = i + 1
        print("i = ", i)
    
    
    #with open(address, "w") as f:      # write back to the json file
     #   json.dump(variables, f)


    #pause
    
    time.sleep(1)