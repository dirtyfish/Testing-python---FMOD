# -*- coding: utf-8 -*-
# vispy: testskip
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Vispy Development Team.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
"""Display a live webcam feed. Require OpenCV (Python 2 only).
"""

try:
    import cv2
except Exception:
    raise ImportError("You need OpenCV for this example.")

import numpy as np
from vispy import app
from vispy import gloo

from moviepy.editor import *






import random
from ctypes import *
import time

PLATFORM_SUFFIX = "64" if sizeof(c_voidp) == 8 else ""
VERSION = 0x00011000 #CHANGE THIS TO MATCH CORRECT VERSION!!!
BANK_FILES = [ "Master Bank.bank", "Master Bank.strings.bank", "Weapons.bank","Vehicles.bank","UI_Menu.bank","Surround_Ambience.bank","Music.bank"]

studio_dll = None
studio_sys = None
time=1
clip=VideoFileClip('bikes.wmv');

def check_result(r):
    if r != 0:
        print("ERROR: Got FMOD_RESULT {0}".format(r))


def studio_init():
    print("Initializing FMOD Studio");
    global studio_dll
    global studio_sys
    studio_dll = WinDLL("fmodstudioL" + PLATFORM_SUFFIX)

    lowlevel_dll = WinDLL("fmodL" + PLATFORM_SUFFIX)
    # Write debug log to file
    
    check_result(lowlevel_dll.FMOD_Debug_Initialize(0x00000002, 1, 0, "log.txt".encode('ascii')))
    # Create studio system
    studio_sys = c_voidp()
    check_result(studio_dll.FMOD_Studio_System_Create(byref(studio_sys), VERSION))
    # Call System init
    #print ("ok")
    check_result(studio_dll.FMOD_Studio_System_Initialize(studio_sys, 256, 0, 0, c_voidp()))
    # Load banks

    for bankname in BANK_FILES:
        print("Loading bank: " + bankname)
        bank = c_voidp()
        check_result(studio_dll.FMOD_Studio_System_LoadBankFile(studio_sys, bankname.encode('ascii'), 0, byref(bank)))



def play_sound(soundname,time=0):
    print("Playing sound: " + soundname)
    event_desc = c_voidp()
    check_result(studio_dll.FMOD_Studio_System_GetEvent(studio_sys, soundname.encode('ascii'), byref(event_desc)))
    event_inst = c_voidp()
    check_result(studio_dll.FMOD_Studio_EventDescription_CreateInstance(event_desc, byref(event_inst)))
    check_result(studio_dll.FMOD_Studio_EventInstance_SetVolume(event_inst, c_float(0.75+.2*random.random())))


    check_result(studio_dll.FMOD_Studio_EventInstance_SetPitch(event_inst,c_float(.9+.2*random.random())))
    check_result(studio_dll.FMOD_Studio_EventInstance_SetReverbLevel( event_inst, c_int(3),c_float(1.8)))

    check_result(studio_dll.FMOD_Studio_EventInstance_SetTimelinePosition(event_inst,c_int(time)));

    check_result(studio_dll.FMOD_Studio_EventInstance_Start(event_inst))
    check_result(studio_dll.FMOD_Studio_EventInstance_Release(event_inst))
      




vertex = """
    attribute vec2 position;
    attribute vec2 texcoord;
    varying vec2 v_texcoord;
    void main()
    {
        gl_Position = vec4(position, 0.0, 1.0);
        v_texcoord = texcoord;
    }
"""

fragment = """
    uniform sampler2D texture;

    uniform sampler2D texture2;
    uniform sampler2D texture3;
    varying vec2 v_texcoord;

    

    void main()
    {
        vec2 uv=v_texcoord-.5;
        gl_FragColor.b= .5-.5*(sqrt(uv.x*uv.x+uv.y*uv.y)); //background blue

        //gl_FragColor.r= 55.*(.5-(sqrt(uv.x*uv.x+uv.y*uv.y))); //background red
        
        
        if ((v_texcoord.y>0.875)&&(v_texcoord.x<0.125))
        {gl_FragColor = float(v_texcoord.y>0.875)*float(v_texcoord.x<0.125)*texture2D(texture, fract(v_texcoord*8.));   //cam pic
        gl_FragColor =gl_FragColor.bgra;}

         if ((v_texcoord.y<0.125)&&(v_texcoord.x<0.125))
        gl_FragColor = float(v_texcoord.y<0.125)*float(v_texcoord.x<0.125)*texture2D(texture3, fract(v_texcoord*8.));   //rand pic

        if(1>0)
        {if (v_texcoord.y>0.875)if (v_texcoord.x>0.125)//blue area
         gl_FragColor= vec4(0,0,0,1);   

         if (v_texcoord.y<0.125)if (v_texcoord.x>0.125)//blue area
         gl_FragColor= vec4(0,0,0,1);    }

        
        //gl_FragColor+=vec4(v_texcoord,0,0);
    }
"""


class Canvas(app.Canvas):
    def __init__(self):
        app.Canvas.__init__(self, size=(1280, 960), keys='interactive')
        self.program = gloo.Program(vertex, fragment, count=4)
        self.program['position'] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]
        self.program['texcoord'] = [(1, 1), (1, 0), (0, 1), (0, 0)]
        self.program['texture2'] = rtex=(1024*np.random.rand(480, 640, 3)).astype(np.uint8)#random texture
        
        self.program['texture3']=clip.get_frame(6);
        self.program['texture'] = np.zeros((480, 640, 3)).astype(np.uint8)#free space for cam texture

        #print (self.program['texture2'])
        #print (self.program['texture'])
        #print (rtex)

        width, height = self.physical_size
        gloo.set_viewport(0, 0, width, height)

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception("There's no available camera.")
        self._timer = app.Timer('auto', connect=self.on_timer, start=True)
        
        self.show()

    def on_resize(self, event):
        width, height = event.physical_size
        gloo.set_viewport(0, 0, width, height)

     
        play_sound("event:/UI/Cancel",0)
        check_result(studio_dll.FMOD_Studio_System_Update(studio_sys))

    

    def on_draw(self, event):
        gloo.clear('black')
        _, im = self.cap.read()
        global time
        time+=.01
        self.program['texture3']=clip.get_frame(time%4);
        self.program['texture'][...] = im
        self.program.draw('triangle_strip')

        #self.program['texture2'] = rtex=(1024*np.random.rand(480, 640, 3)).astype(np.uint8)#random texture
       
        check_result(studio_dll.FMOD_Studio_System_Update(studio_sys))
        
    def on_timer(self, event):
        self.update()
     
   
studio_init()     
c = Canvas()
play_sound("event:/Ambience/Country",33000)
app.run()
c.cap.release()
#play_sound("event:/Music/Music")
#tick_update(5)
#play_sound("event:/Explosions/Single Explosion")
#tick_update()