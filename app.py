import console
import tkinter

def run(**options):
    if options['platform'] == 'console':
        return console.init
    else:
        return tkinter.init
