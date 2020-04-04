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
runRoad = 1


chapter = 0

global textJson
textJson = {}

global dialogueJson
dialogueJson = {}
global availableDialogues
availableDialogues = {}

global pleace

global commands
global commandsCalls
global activCommandsCalls

##Loads

def loadCommandCallsList():
    global commandsCalls
    global activCommandsCalls
    commandsCalls = {}
    activCommandsCalls = {}
    for i in commands:
        for ii in i["calls"]:
            commandsCalls[ii] = i["func"]
            if(i.get("act")) :
                activCommandsCalls[ii] = i["func"]
    return(0)

def loadDialoguesJson():
    global dialogueJson
    dialogueJson = {}
    for x in os.listdir("data/dialogues/"):
        dialogueJson.update( J.load(codecs.open('data/dialogues/'+str(x), 'r', 'utf-8-sig')) )
    return(0)

def loadPleace():
    global pleace
    global availableDialogues
    data = J.load(codecs.open('data/pleaces/'+str(chapter)+'.json', 'r', 'utf-8-sig'))
    pleace = data

    say(data.get("startDes"))

    for i in commands:
        if(i["name"] in data["commands"] or i["name"] in ["help","exit"]):
            i["act"] = True
        else:
            i["act"] = False
    availableDialogues = data.get("dialogues")
    if(availableDialogues == None):
        availableDialogues = {}
    return(0)



##Commands
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

def cTalk(args):
    if(len(args) == 1):
        say("Zapomniałeś chyba podać imienia rozmuwcy.")
        return(0)

    global availableDialogues
    print(args[1] in availableDialogues)
    print(availableDialogues)
    print(args[1])
    if(args[1] in availableDialogues):
        dialogue(availableDialogues[ str( args[1] ) ])
    else:
        say("Nie ma tutaj kogoś takiego jak \"{}\".".format(args[1]))
    return(0)

def cLook(args):
    say(des)
    return(0)

def cHelp(args):
    if(0 == (len(args) > 1 and args[1] == "wszystkie")):
        say("&0Poniżej wyświetlone komendy są jedynie na tę chwilę możliwymi do wykonania komendami. Jeżeli za to chcesz poznać je wszystki wpisz \"pomoc wszystkie\" w lini poleceń.&7 ")
    global commands
    for i in commands:
        if(i.get("act") or ( len(args) > 1 and args[1] == "wszystkie" )):
            say( "{}   {}".format(i.get("sample"), i.get("des")) )


    return(0)

def cExit(args):
    exit()
    return(0)


commands =[
    {"name":"drink",
    "calls":["napij","Napij"],
    "func":None
    },
    {"name":"",
    "calls":[],
    "func":None
    },
    {"name":"",
    "calls":[],
    "func":None
    },
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
    {"name":"",
    "calls":[],
    "func":None
    },
    {"name":"help",
    "sample":"pomoc",
    "des":"pokazuje wszyskie dostępne komendy",
    "calls":["pomoc","Pomoc","pomocy","Pomocy","?"],
    "func":cHelp
    },
    {"name":"exit",
    "sample":"wyjdz",
    "des":"wyłancza grę bez zapisywania jej",
    "calls":["wyjdz", "wyjście", "Wyjdz", "Wyjście", "zamknij", "Zamknij", "wyjscie", "Wyjscie"],
    "func":cExit
    }
]

commandsCalls = {}
activCommandsCalls = {}

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

    if(col[0] in commandsCalls):
        if(col[0] in activCommandsCalls):
            commandsCalls[col[0]](col)
        else:
            say(textJson["noActiveCommandUse"])
    else:
        say(R.choice(textJson["errorCommandMessageList"]).format(co))
