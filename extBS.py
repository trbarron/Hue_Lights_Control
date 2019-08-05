import pygame, pygame.midi, pprint, math, lightpack, sys, time, colorsys, csv, threading
from phue import Bridge
import pandas as pd
from scapy.all import *

################################

def extButtonSniffer(hunk_of_data):
    data,lights,input_id,colored_lights,lightpack,bnw_lights,light,lp,MACs,lightpack_enabled = hunk_of_data
    time_called = 0
    filter_list = "ether host " + MACs[0]
    for i in range(1,len(MACs)):
        filter_list += "or ether host " + MACs[i]
    print(filter_list)
    
    while True:
        c = sniff(count=1,filter=filter_list)
        print(c)
        if MACs.count(c[0].src):
            
            diff = time.time() - time_called
            thresh = 10

            if diff > thresh:

                #turn lights the opposite of what most of them are (most are off, turn them all on)

                sum_lights = 0
                for cl in colored_lights: sum_lights += light[cl].on
                for bnw in bnw_lights: sum_lights += light[bnw].on

                result = not (sum_lights / (len(colored_lights)+len(bnw_lights)) > 0.5)
                
                for cl in colored_lights: light[cl].on = result
                for bnw in bnw_lights: light[bnw].on = result

                time_called = time.time()
