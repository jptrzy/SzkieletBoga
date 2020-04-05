import os, struct
system = 0

try:

    import color_console as cons
    import sys

    system = 1

    default_colors = cons.get_text_attr()
    default_bg = default_colors & 0x0070
    default_fg = default_colors & 0x0007

    GREY      = 0x0000
    BLUE      = 0x0001
    GREEN     = 0x0002
    CYAN      = 0x0003
    RED       = 0x0004
    MAGENTA   = 0x0005
    YELLOW    = 0x0006
    WHITE     = 0x0007

except:
    system = 2

def _get_terminal_size_windows():
    from ctypes import windll, create_string_buffer
    # stdin handle is -10
    # stdout handle is -11
    # stderr handle is -12
    h = windll.kernel32.GetStdHandle(-12)
    csbi = create_string_buffer(22)
    res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
    if res:
        (bufx, bufy, curx, cury, wattr,
         left, top, right, bottom,
         maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
        sizex = right - left + 1
        sizey = bottom - top + 1
        return( sizex, sizey )


def say(x):
    columns,_  = _get_terminal_size_windows()
    columns -= 5
    x = x.split("\n")
    for xx in x:
        data = xx.split()
        str = ""
        for i in data:
            if( len(str) + len(i) + 1 > columns):
                colSay(str)
                str = i + " "
            else:
                str += (i + " ")
        colSay(str)

    return(0)

def colSay(x):
    data = x.split("&")
    print(data[0], end='')
    sys.stdout.flush()
    for i in data[1:]:
        cons.set_text_attr( [GREY, BLUE, GREEN, CYAN, RED, MAGENTA, YELLOW, WHITE ][int(i[0])] | cons.FOREGROUND_INTENSITY)
        print(i[1:], end='')
        sys.stdout.flush()
    print('')
    return(0)

def inp():
    return(input())

def ERROR(x):
    say("&4{}".format(x))

def WAR(x):
    say("&6 !!! {} !!! ".format(x))
