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

chapter = 0

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
        print(x)
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

        i = int(i)-1
        if(i >= 0 and len(res) > i):

            d = dialogue
            if(res[i].get("exec") != None):
                exec(res[i].get("exec"))
            else:
                WAR("Nie ma ustawionej zmiennej exec")
            return(0)

        else:
            say("Podaj liczbę w przedziale od 1 do {}".format(i, len(res) ) )

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
    "des":"pozwala tobie zobaczyć gdzie jesteś oraz co widzisz",
    "calls":["rozejrzyj","Rozejrzyj"],
    "func":cLook
    },
    {"name":"help",
    "sample":"pomoc",
    "des":"pokazuje wszystkie dostępne komendy",
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

    if(chapter == 1):
        dialogue("05092020")


    say("&2[&7Rozdział &6{}&2]&7 {}".format(chapter, VARIBLES["angryMonster"]))

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

say("Przed snem wszyscy gromadzą się na polanie, aby godnie odprawić Bertholda na tamten świat. Nawet Kurt stoi w milczącym kręgu, patrzącym jak Heinz wskrzesza ogień i jak płomienie powoli ogarniają cały stos, a na koniec ciało twego przyjaciela. Szkoda, że nie będzie mu dane dotrzeć do Jerrathu. Niestety, żadne z was nie jest w stanie teraz nic na to poradzić. Jedyne co możecie zrobić to przespać tu jeszcze jedną noc, zanim ruszycie w dalszą drogę, żeby być chociaż wypoczętymi. Tym bardziej, że wasz aktualny nastrój wcale by nie sprzyjał wędrówce.")
say("I tak oto wszyscy pogrążają się w błogim śnie. Wszyscy prócz ciebie. Tym razem jednak nie budzisz się dla rekreacji. Budzisz się dla zbawienia. Bynajmniej nie siebie, bo i tak nie wierzysz w istoty wyższe. Chodzi o zbawienie innych. I na pewno nie przed piekłem w innym świecie, ale przed piekłem na ziemi, jakie niedługo może urządzić doskonale znany ci potwór…")
if(VARIBLES["diaAlfrida"]==4004):
    say("Widzisz, że Alfrida już jest na nogach. Oboje oglądacie na otwór z wystającą drabiną. Kapłanka kiwa głową. Nie ma co zwlekać. Razem, bardzo ostrożnie podchodzicie do drewnianych szczebli.")
else:
    say("Powoli, z nie ma co ukrywać, duszą na ramieniu podchodzisz do otworu z wystającą drabiną.")
if(3 <= VARIBLES["angryMonster"]):
    say("Niestety, twoje przeczucia się spełniły. Potwór znowu się pojawił. W dodatku tym razem nie zwraca na ciebie żadnej uwagi. Próbujesz przemówić mu do rozsądku, zastraszyć go. Żaden dźwięk nie dobywa się z twych ust. W końcu rzucasz się na niego. On cię bez trudu rzuca o ścianę domku. Kiedy się podnosisz widzisz jak ze smakiem pożera kolejne części ciała Alfridy. A ty nie możesz nic zrobić. Możesz tylko patrzeć jak dokonuje się coś, czemu chciałeś zapobiec. A i tak ci się nie udało.")
    say("Następnego ranka wszyscy są w jeszcze podlejszych nastrojach. Szczególnie Kurt, który znów zaszył się za chatką. Tym razem jednak nie ma co zwlekać. Celina zarządza, że trzeba natychmiast spalić ciało i ruszyć w dalszą drogę, aby oddalić się od nieznanej bestii. Ty jednak wiesz, że jeśli nic nie zaradzisz, reszta i tak zginie, a wraz z nią i ty.")
elif(2 == VARIBLES["angryMonster"]):
    x = " udało ci się uspokoić potwora i zmusić do tego aby się wycofał. "
    if(VARIBLES["diaAlfrida"]==4004):
        x = "Przez otwór w podłodze doskonale widać potwora, próbującego się wdrapać po drabinie. Na szczęście, dzięki kapłance, która rzuciła krótkotrwały urok" + x
        x+="Aż do świtu ty razem z Alfridą czuwacie nad Kurtem"
    else:
        x = "Przez otwór w podłodze doskonale widać potwora, próbującego się wdrapać po drabinie. Na szczęście, dzięki bliższemu poznaniu tego, kto krył się pod tą potworną postacią" + x
        x+="Aż do świtu czuwacie nad Kurtem"

    say(x)
    say("Niestety, paser czuje równie słabo co poprzedniego dnia rano. Cóż, przynajmniej udało się bez przeszkód ruszyć w dalszą drogę, w stronę Jerrathu. Wiecie/Wiesz jednak, że problem został tylko odwleczony. Prędzej czy później trzeba będzie go rozwiązać na dobre. Ważne jednak, że tym razem nikt nie zginął i idziecie ramię w ramię, całą drużyną. A w drużynie, jak wiadomo, zawsze raźniej. Cóż, podobno...")
elif(1 == VARIBLES["angryMonster"]):

    if(VARIBLES["diaAlfrida"]!=4004 and VARIBLES["diaKurt"]==5004 and VARIBLES["kurtPast"] == False):
        say("Przez dziurę w podłodze nie widać niczego, tedy ostrożnie schodzisz na dół. Natomiast to, co tam widzisz… jest tak niewiarygodne, że aż przecierasz oczy. Zamiast iść prosto na ciebie, z rządzą mordu w oczach, siedzący na posłaniu Kurta stwór… miota się. Jakby chciał coś wyrzucić ze swej głowy, ale nie mógł. A może to Kurt próbuje pozbyć się raz na zawsze bestii, która przejmuje go co noc? Cóż, niestety jedyne, co jesteś w stanie zrobić to usiąść obok niego, aby nie czuł się sam w walce o własny rozum. Nawet ci się zdaje, że coś to pomogło, po po paru godzinach pasma magii się rozpraszają, a Kurt zasypia jak zabity. Na wszelki wypadak postanawiasz przy nim czuwać, aż do świtu.")
        say("Rankiem oczywiście nikt nie zginął. Ba, nawet paser wstał w dziwnie wesołym nastroju. Już nie kryje się za chatką i solidarnie pomaga innym w przygotowaniach do wędrówki. Niestety, nawet na chłopski rozum doskonale wiesz, że problem nie został rozwiązany. Przynajmniej nie do końca. Będziesz musiał jeszcze się postarać, aby Kurt na dobre odzyskał spokój ducha. Ale, przynajmniej na ten moment, nikt nie musi się obawiać o swe zdrowie i życie.")
    elif(VARIBLES["diaAlfrida"]==4004 and VARIBLES["diaKurt"]==5001 and VARIBLES["kurtPast"]):
        say("Przez otwór w podłodze doskonale widać potwora, próbującego się wdrapać po drabinie. Akolitka Młotodzierżcy jednym słowem rzuca urok bestię, dając ci cenną minutę. Na szczęście wiesz, jak ją wykorzystać. Przypominając sobie wszystko, czego się o pasterze dowiedziałeś poprzedniego dnia próbujesz mu przypomnieć kim tak naprawdę jest, a także pocieszyć go. Zaznaczyć, że nie jest sam i wokół są ludzie, którzy w razie potrzeby mogą mu pomóc, choćby tylko wysłuchując tego, co ten ma na duszy. I o dziwo, twoja gadka przynosi efekty. Stwór zaczyna się miotac po podłodzę, jakby chciał coś wyrzucić ze swej głowy, potem zaczyna się rozpadać na pasma dzikiem magii, które natychmiast znikają, a Kurt, odzyskawszy swą postać… zasypia w miejscu, gdzie była bestia. Oboje uznajecie, że najrozsądniej będzie czuwać nad nim na wypadek, gdyby znowu jego talent nad nim zapanował.")
        say("Rankiem natomiast, oczywiście nikt nie zginął. Ba, nawet paser wstał w dziwnie wesołym nastroju. Już nie kryje się za chatką i solidarnie pomaga innym w przygotowaniach do wędrówki. Niestety, Alfrida wyjaśniła ci na boku, że problem nie został rozwiązany. Przynajmniej nie do końca. Będziecie musiał jeszcze się postarać, aby Kurt na dobre odzyskał spokój ducha. Ale, przynajmniej na ten moment, nikt nie musi się obawiać o swe zdrowie i życie.")
    else:
        say("Opcje 3 w Wkurzenie 1 oto zmienne")
        print(VARIBLES["diaAlfrida"])
        print(VARIBLES["diaKurt"])
        print(VARIBLES["kurtPast"])


elif(0 >= VARIBLES["angryMonster"]):
    if(VARIBLES["diaAlfrida"]==4004):
        say("Jednak nie możesz uwierzyć w to, co się dzieje. Zamiast iść prosto na stronę któregoś z was, z rządzą mordu w oczach, siedzący na posłaniu Kurta stwór… miota się. Jakby chciał coś wyrzucić ze swej głowy, ale nie mógł. A może to Kurt próbuje pozbyć się raz na zawsze bestii, która przejmuje go co noc? Wiesz jedno - jedynym podmiotem, który umrze tej nocy będzie przeszłość pasera. A tym, co wróci na jego miejsce będzie odzyskany spokój ducha. Nie masz co do tego żadnych wątpliwości. Z resztą, jak miałbyś je mieć, skoro towarzyszy ci Alfrida, która wyleczyła już nie jedną duszę. I tak oto, od słowa do słowa, od wyznania do wyznania, od łzy do łzy, dzika magia zaczyna znikać, mieszczanin się uspokaja, aż w końcu zapada w kojący sen, zmęczony wrażeniami tej nocy. Aż do świtu ty razem z Alfridą czuwacie nad Kurtem, na wszelki wypadek.")
        say("Nazajutrz Kurt oznajmia, że dawno nie czuł się tak spokojny i tak szczęśliwy po dobrze odespanej nocy. Wiecie doskonale, że oznacza to wasz/twój sukces. Udało się przegnać jego demony przeszłości. On sam pomógł swej psychice się odbudować na nowo. Dzięki temu, wszyscy jak jedna, zgrana drużyna, ruszacie w stronę Jerrathu, bez obaw o własne życie.")
    else:
        say("Jednak nie możesz uwierzyć w to, co się dzieje. Zamiast iść prosto na ciebie, z rządzą mordu w oczach, siedzący na posłaniu Kurta stwór… miota się. Jakby chciał coś wyrzucić ze swej głowy, ale nie mógł. A może to Kurt próbuje pozbyć się raz na zawsze bestii, która przejmuje go co noc? Wiesz jedno - jedynym podmiotem, który umrze tej nocy będzie przeszłość pasera. A tym, co wróci na jego miejsce będzie odzyskany spokój ducha. Nie masz co do tego żadnych wątpliwości. Z resztą, jak miałbyś je mieć, skoro doskonale wiesz co dolega Kurtowi i wiesz jak mu pomóc. I tak oto, od słowa do słowa, od wyznania do wyznania, od łzy do łzy, dzika magia zaczyna znikać, mieszczanin się uspokaja, aż w końcu zapada w kojący sen, zmęczony wrażeniami tej nocy. Aż do świtu czuwasz nad Kurtem, na wszelki wypadek.")
        say("Nazajutrz Kurt oznajmia, że dawno nie czuł się tak spokojny i tak szczęśliwy po dobrze odespanej nocy. Wiesz doskonale, że oznacza to twój sukces. Udało się przegnać jego demony przeszłości. On sam pomógł swej psychice się odbudować na nowo. Dzięki temu, wszyscy jak jedna, zgrana drużyna, ruszacie w stronę Jerrathu, bez obaw o własne życie.")
else:
    print(VARIBLES["angryMonster"])


say("&0To jest już koniec tej gry lecz pamiętaj, że ta gra ma więcej niż jedno zakończenie więc może spróbuj znaleźć jakieś lepsze.")
say("&0Wciśnij Enter, aby zakończyć przygodę:")
inp()
