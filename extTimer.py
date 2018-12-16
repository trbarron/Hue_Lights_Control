import pygame, pygame.midi, pprint, math, lightpack, sys, time, colorsys, csv, threading, pyowm
from phue import Bridge
import pandas as pd
from scapy.all import *

################################


def extWakeupTimer(hunk_of_data):
    t = 'wakeup_time.csv' #point it towards CSV
    time_thing = pd.read_csv(t)
    data,lights,input_id,colored_lights,lightpack,bnw_lights,light,lp,MACs = hunk_of_data

    while True:
        now = time.strftime("%H:%M")
        if len(time_thing[time_thing.wakeup_time==str(now)]) > 0:

            #Connect to weather service
            owm = pyowm.OWM('insert_API_key_here')
            #Get weather for where you live for the next day
            fc = owm.daily_forecast("Somerville, MA, USA")
            f = fc.get_forecast()
            for weather in f: j = weather.get_weather_code()
            print(j)
        
            line = data[data.id==str(j)]

            print(line)
            #Set colored lights
            for cl in colored_lights:
                    R = int(line[cl + ' R'])
                    G = int(line[cl + ' G'])
                    B = int(line[cl + ' B'])
                    R, G, B = [x/255.0 for x in [R, G, B]]
                    [hue, bri, sat] = colorsys.rgb_to_hls(float(R),float(G),float(B))
                    light[cl].on = True
                    light[cl].hue = int(hue*65535)
                    light[cl].brightness = int(bri*254)
                    light[cl].saturation = int(sat*254)
                
            #Set bnw lights
            for bnw in bnw_lights:
                    bri = line[bnw + ' bri']
                    light[bnw].on = True
                    light[bnw].bri = bri

            #Set lightpacks
            for cl in lightpack:
                    R = int(line[cl + ' R'])
                    G = int(line[cl + ' G'])
                    B = int(line[cl + ' B'])
                    lp.setColourToAll((R, G, B))
        time.sleep(60)
