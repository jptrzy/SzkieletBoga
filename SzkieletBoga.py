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

def say(x, col=cons.FOREGROUND_GREEN):
    cons.set_text_attr(col | default_bg | cons.FOREGROUND_INTENSITY)
    print(str(x))
    cons.set_text_attr(default_colors)

def ERROR(x):
    say(x, cons.FOREGROUND_RED)

global run
run = 1

ti = 0
day = 0

global dialogueJson
dialogueJson = {}

global des
global dialogues
des = ""
dialogues = {}

##Loads

def loadDialoguesJson():
    global dialogueJson
    dialogueJson = {}
    for x in os.listdir("data/dialogues/"):
        dialogueJson.update( J.load(codecs.open('data/dialogues/'+str(x), 'r', 'utf-8-sig')) )

def loadRoad():
    global des
    global dialogues
    data = J.load(codecs.open('data/road/'+str(day)+'.json', 'r', 'utf-8-sig'))
    des = data["des"]
    dialogues = data["dialogues"]

##Commands

def lookAroudn(args):
    say(des)
    return(0)

def dialogue(id):
    global run
    global dialogueJson
    try:
        data = dialogueJson[str(id)]
    except:
        ERROR("ID {} not found in {}".format(id, dialogueJson))
        return(1)
    for i in data['messages']:
        say(i)
        if(data['messages'][-1] != i):
            say(data['messages'][-1])
            say(i)
            inp()
    for i, ii in enumerate(data['responses']):
        say( "{} {}".format(i+1, ii["text"]) )

    while(run):
        i = inp()
        try:
            i = int(i)-1
            if(i >= 0 and len(data['responses']) > i):
                ##say(data['responses'][i]['text'])
                if(data['responses'][i].get("com") == None or data['responses'][i]['com'] == "exit"):
                    say(data['responses'][i]['var'])
                    return(0)
                elif(data['responses'][i]['com'] == "dia"):
                    dialogue(data['responses'][i]['var'])
                    return(0)
                else:
                    print("Nie znana komenda {}".format(data['responses'][i]['com']))
                    return(0)

        except:
            say( "{} to nie jest liczba. Podaj liczbę w przedziale od 1 do {}".format(i, len(data['responses']) ) )





    return(0)

def cDialogue(args):
    if(len(args)):
        say("Zapomniałeś chyba podać imienia rozmuwcy.")
        return(0)

    global dialogues
    if(args[1] in dialogues):
        dialogue(dialogues[ str( args[1] ) ])
    return(0)

commands ={
"rozejrzyj":lookAroudn,
"rozmawiaj":cDialogue
}

##LOADING JSONS

data = J.load(codecs.open('data/errorCommands.json', 'r', 'utf-8-sig'))
errorCommandsList = data["texts"]

'''
for i in range(0x0000, 0x0008):
    say(i,
    default_colors & i
    )
'''

loadDialoguesJson()

loadRoad()

while(run):
    ##Road Segment

    say("[{} dzień ]".format(day + 1, ["przed południem", "południe", "po południu"][ti]))

    co = inp()
    col = co.split()

    if(col[0] in commands):
        commands[col[0]](col)
    else:
        say(R.choice(errorCommandsList).format(co))

    ##Rest Segment

    ##Dream Segment

    ##Dawn Segment
