#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 09:26:31 2019

@author: ikhwan
"""

from tkinter import Label,mainloop, Tk, Entry, Frame, Button, BOTTOM

master = Tk()
Label(master, text='First Name').grid(row=0)
e1 = Entry(master)
e1.grid(row=0, column=1) 

frame = Frame(master) 
frame.pack() 
bottomframe = Frame(master)
bottomframe.pack(side=BOTTOM)
redbutton = Button(frame, text = 'Red', fg ='red').grid(row=1)
mainloop()