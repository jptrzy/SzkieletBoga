#!/usr/bin/python
#-*- coding: utf-8 -*-
import random as R
from graphic import *
import json as J
import os
import time
import codecs
import sys

global run
run = 1


chapter = 2

global textJson
textJson = {}

global dialogueJson
dialogueJson = {}
global availableDialogues
availableDialogues = {}

global pleace

global commands
global allCommands
global commandsCalls

global VARIBLES
VARIBLES = {}
VARIBLES = {"trueForm": 1}

##Loads

def loadCommandCallsList():
    global allCommands
    global pleace
    global commands
    allCommands = commands.copy()
    allCommands += pleace.get("commands")
    global commandsCalls
    commandsCalls = {}
    for i in allCommands:
        for ii in i["calls"]:
            if(i.get("exec") != None):
                commandsCalls[ii] = i.get("exec")
            else:
                commandsCalls[ii] = i["func"]
    return(0)

def loadDialoguesJson():
    global dialogueJson
    dialogueJson = {}
    for x in os.listdir("data/dialogues/"):
        dialogueJson.update( J.load(codecs.open('data/dialogues/'+str(x), 'r', 'utf-8-sig')) )
    return(0)

def loadAvailableDialogues():
    global pleace
    global availableDialogues
    availableDialogues = pleace.get("dialogues")
    if(availableDialogues == None):
        availableDialogues = {}
    return(0)

def loadPleace():
    global pleace
    global VARIBLES
    data = J.load(codecs.open('data/pleaces/'+str(chapter)+'.json', 'r', 'utf-8-sig'))
    pleace = data
    if(pleace.get("exec") != None):
        exec(pleace.get("exec"))
    say(data.get("startDes"))


    loadAvailableDialogues()
    return(0)



##Commands
def nChapter():
    global chapter
    chapter += 1
    loadDialoguesJson()
    loadPleace()
    loadCommandCallsList()

def dialogue(id):
    global run
    global dialogueJson
    global VARIBLES
    try:
        data = dialogueJson[str(id)]
    except:
        ERROR("ID {} not found in {}".format(id, dialogueJson))
        return(1)

    say(data['messages'])

    res = []

    for i in data['responses']:
        if(i.get("if") == None):
            res.append(i)
        else:
            exec("global x\nx = ( {} )".format(i["if"]))
            if(x):
                res.append(i)

    for i, ii in enumerate(res):
        say( "{} {}".format(i+1, ii["text"]) )

    while(run):
        i = inp()
        try:
            i = int(i)-1
            if(i >= 0 and len(res) > i):
                try:
                    d = dialogue
                    if(res[i].get("exec") != None):
                        exec(res[i].get("exec"))
                    else:
                        WAR("Nie ma ustawionej zmiennej exec")
                    return(0)
                except:
                    ERROR("Error 303")
                    return(1)
            else:
                say("Podaj liczbę w przedziale od 1 do {}".format(i, len(res) ) )
        except:
            say( "{} to nie jest liczba. Podaj liczbę w przedziale od 1 do {}".format(i, len(res) ) )
    return(0)

def cTalk(args):
    if(len(args) == 1):
        say("Zapomniałeś chyba podać imienia rozmuwcy.")
        return(0)

    global availableDialogues
    if(args[1] in availableDialogues):

        dialogue(availableDialogues[ str( args[1] ) ])
    else:
        say("Nie ma tutaj kogoś takiego jak \"{}\".".format(args[1]))
    return(0)

def cLook(args):
    say(pleace["des"])
    return(0)

def cHelp(args):
    global allCommands
    for i in allCommands:
        say( "{}{}{}".format(i.get("sample"), " &6-&7 ", i.get("des")) )


    return(0)

def cExit(args):
    exit()
    return(0)


commands =[
    {"name":"talk",
    "sample":"rozmawiaj &2<&7osoba&2>&7",
    "des":"służy do rozmawiania z kimś",
    "calls":["rozmawiaj", "Rozmawiaj", "porozmawiaj", "Porozmawiaj"],
    "func":cTalk
    },
    {"name":"look",
    "sample":"rozejrzyj",
    "des":"pozwola tobie zobaczyć gdzie jesteś oraz co widzisz",
    "calls":["rozejrzyj","Rozejrzyj"],
    "func":cLook
    },
    {"name":"help",
    "sample":"pomoc",
    "des":"pokazuje wszyskie dostępne komendy",
    "calls":["pomoc","Pomoc","pomocy","Pomocy","?"],
    "func":cHelp
    },
    {"name":"exit",
    "sample":"wyłącz",
    "des":"wyłancza grę bez zapisywania jej",
    "calls":["wyłącz", "Wyłącz", "wylacz", "Wylacz", "exit", "Exit"],
    "func":cExit
    }
]

allCommands = []

commandsCalls = {}
##LOADING Text JSONS
textJson = J.load(codecs.open('data/text/Pl.json', 'r', 'utf-8-sig'))

say(textJson["introduction"])

loadDialoguesJson()
loadPleace()
loadCommandCallsList()
while(run):
    say("&2[&7Rozdział &6{}&2]&7".format(chapter))

    co = inp()
    col = co.split()


    if( len(col) > 0 and col[0] in commandsCalls):
        if(type(commandsCalls[col[0]]) == str):
            args = col
            exec(commandsCalls[col[0]])
        else:
            commandsCalls[col[0]](col)

    else:
        say(R.choice(textJson["errorCommandMessageList"]).format(co))
