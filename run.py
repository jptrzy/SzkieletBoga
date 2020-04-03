#!/usr/bin/python
#-*- coding: utf-8 -*-
import random as R
import color_console as cons
import json as J
import os
import time
import codecs
import sys

default_colors = cons.get_text_attr()
default_bg = default_colors & 0x0070
default_fg = default_colors & 0x0007

def inp():
    return(input())

def say(x):
    cons.set_text_attr(cons.FOREGROUND_GREEN | default_bg |
                     cons.FOREGROUND_INTENSITY)
    print(x)
    cons.set_text_attr(default_colors)

run = 1

day = 0

global dialogueJson
dialogueJson = {}

global des
global dialogues
des = ""
dialogues = []

##Loads

def loadDialoguesJson():
    global dialogueJson
    dialogueJson = {}
    for x in os.listdir("data/dialogues/"):
        print(x)
        dialogueJson.update( J.load(codecs.open('data/dialogues/'+str(x), 'r', 'utf-8-sig')) )
    print(dialogueJson)


def loadRoad():
    global des
    global dialogues
    data = J.load(codecs.open('data/road/'+str(day)+'.json', 'r', 'utf-8-sig'))
    des = data["des"]
    print(des)
    dialogues = data["dialogues"]

##Commands

def lookAroudn(args):
    say(des)
    return(0)

def dialogue(id):
    data = dialogueJson





    return(0)

def cDialogue(args):
    return(0)

commands ={
"rozejrzyj":lookAroudn,
"rozmawiaj":cDialogue
}

##LOADING JSONS

data = J.load(codecs.open('data/errorCommands.json', 'r', 'utf-8-sig'))
errorCommandsList = data["texts"]




dialogue(1001)

loadDialoguesJson()

loadRoad()

while(run):
    ##Road Segment

    co = inp()
    col = co.split()

    if(col[0] in commands):
        print(0)
        commands[col[0]](col)
    else:
        say(R.choice(errorCommandsList).format(co))

    ##Rest Segment

    ##Dream Segment

    ##Dawn Segment
