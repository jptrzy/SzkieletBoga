#!/usr/bin/python
#-*- coding: utf-8 -*-

import tkinter

import random as R
import json as J

from graphic import *


run = 1

commands = {"say":"sas"}

#LOADING JSONS

jfile = open('data/errorCommands.json', 'r')
data = J.load(jfile)
errorCommandsLenght = data["lenght"]
errorCommandsList = data["texts"]

while(run):

    ##Pobieramy komende od gracza
    co = inp()
    col = co.split()

    if(col[0] in commands):
        say(commands[col[0]])
        say(col)
    else:
        say(R.choice(errorCommandsList).format(co))
