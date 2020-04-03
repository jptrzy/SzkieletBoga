from tkinter import *
import tkinter.font as TkFont
import os
import time



root = Tk()
root.title("Szkielet Boga")
root.geometry("500x200")

dFont=TkFont.Font(family="Arial", size=12)
#dFont=TkFont.Font(family="Verdana", size=12)

f = Frame()
f.pack(side=TOP, fill=BOTH, expand = 1)

text1 = Text(f, height=1, width=50, font=dFont, background="#000000", foreground="#00ff00", state="disabled", cursor="arrow")
text1.pack(side=LEFT, fill=BOTH, expand = 1)

yscrollbar=Scrollbar(f, orient=VERTICAL, command=text1.yview, bg="black", activebackground="#313131")
yscrollbar.pack(side=LEFT, fill=Y, expand = 0)
text1["yscrollcommand"]=yscrollbar.set

v = StringVar()
entry = Entry(root, textvariable=v, font=dFont, background="#000000", foreground="#00ff00")
entry.pack(side=TOP ,fill=X, expand = 0)


def say(x):
    text1.config(state="normal")
    text1.insert(INSERT,  "\n" + str(x))
    text1.config(state="disabled")

    text1.see(END)
    text1.edit_modified(0)

def send(event=None):
    say(v.get())
    v.set("")


def runGui(send):
    root.bind('<Return>', send)
    root.mainloop()
