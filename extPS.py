import pygame, pygame.midi, pprint, math, lightpack, sys, time, colorsys, csv, threading, time
from phue import Bridge
import pandas as pd
from scapy.all import *

def extPadSniffer(hunk_of_data):
    data,lights,input_id,colored_lights,lightpack,bnw_lights,light,lp,MACs,lightpack_enabled = hunk_of_data
    print("\nextPadSniffer start")
    i = pygame.midi.Input(input_id)
    toggle = False
    toggle_time = 0
    
    while True:
        if i.poll():
            midi_events = i.read(1)
            key = midi_events[0][0][1]
            value = midi_events[0][0][2]
            line = data[data.id==str(key)]

            print("Key: ",key)
            
            #Set colored lights
            for cl in colored_lights:            
                    R = int(line[cl + ' R'])
                    G = int(line[cl + ' G'])
                    B = int(line[cl + ' B'])
                    R, G, B = [x/255.0 for x in [R, G, B]]
                    [hue, bri, sat] = colorsys.rgb_to_hls(float(R),float(G),float(B))
                    if R + G + B == 0: light[cl].on = False
                    else:
                        light[cl].on = True
                        light[cl].hue = int(hue*65535)
                        light[cl].brightness = int(bri*254)
                        light[cl].saturation = int(sat*254)               
                
            #Set bnw lights
            for bnw in bnw_lights:
                    bri = int(line[bnw + ' bri'])
                    if bri == 0: light[bnw].on = False
                    else:
                        light[bnw].on = True
                        light[bnw].bri = bri

            #Set lightpacks
            if lightpack_enabled:
                for cl in lightpack:
                        R = int(line[cl + ' R'])
                        G = int(line[cl + ' G'])
                        B = int(line[cl + ' B'])
                        print(R,G,B)

                        print("lightpack")
                        lp.setBrightness(int((R + G + B)*100 / (254*3)))
                        lp.setColourToAll((R, G, B))
    

            if key < 50 and time.time() - toggle_time > 2:
                toggle = not toggle
                print("Toggle: ",toggle)
                toggle_time = time.time()
                
        if toggle:
            
            delt_time = time.time() - toggle_time

            if delt_time > int(line['transition time']):
                toggle_time = time.time()
                
                if (str(key+1000) in data.id.unique()):
                    key += 1000
                else:
                    key = key%1000
                    
                line = data[data.id==str(key)]

                print("Key: ",key)
                
                for cl in colored_lights:
                        R = int(line[cl + ' R'])
                        G = int(line[cl + ' G'])
                        B = int(line[cl + ' B'])
                        R, G, B = [x/255.0 for x in [R, G, B]]
                        [hue, bri, sat] = colorsys.rgb_to_hls(float(R),float(G),float(B))

                        if R + G + B == 0: light[cl].on = False
                        else:
                            light[cl].on = True
                            light[cl].transitiontime = int(line['transition time'])
                            light[cl].hue = int(hue*65535)
                            light[cl].brightness = int(bri*254)
                            light[cl].saturation = int(sat*254)
