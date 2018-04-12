
###
##import sys
##print(sys.version)
##
##import pip
##installed_packages = pip.get_installed_distributions()
##installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
     #for i in installed_packages])
#print(installed_packages_list)
import random
from ctypes import *
import time

PLATFORM_SUFFIX = "64" if sizeof(c_voidp) == 8 else ""
VERSION = 0x00011000 #CHANGE THIS TO MATCH CORRECT VERSION!!!
BANK_FILES = [ "Master Bank.bank", "Master Bank.strings.bank", "Weapons.bank","Vehicles.bank","UI_Menu.bank","Surround_Ambience.bank","Music.bank"]

studio_dll = None
studio_sys = None

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


def tick_update(x):
    print("Updating...")
    for loop in range(0, x):
        check_result(studio_dll.FMOD_Studio_System_Update(studio_sys))
        time.sleep(0.050)

studio_init()
play_sound("event:/Ambience/Country",35000)
#play_sound("event:/Music/Music")
#tick_update(5)
play_sound("event:/Explosions/Single Explosion")
tick_update(20)
play_sound("event:/Explosions/Single Explosion")
tick_update(10)
play_sound("event:/Explosions/Single Explosion")
tick_update(20)
play_sound("event:/Weapons/Single-Shot Random")
tick_update(20)
play_sound("event:/Weapons/Single-Shot Random")
tick_update(20)
play_sound("event:/Weapons/Full Auto Loop")
tick_update(10)
play_sound("event:/Explosions/Single Explosion")
tick_update(50)

#import os
#os.system('python')

