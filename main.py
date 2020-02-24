#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog
import chinese
import english

# Text reduction
def Simplify():
    import string

    # Stop words
    stoplist = set('i me my we our you he she him his her it its them for a of the and to in have had has is was are were'.split())

    # Special characters
    remove = str.maketrans('', '', string.punctuation)
    for t in txt_name:
        file = open(t, 'r')
        lines = file.readlines()
        texts = [[word.translate(remove) for word in line.lower().split() if word not in stoplist] for line in lines]
        txt_new.append(texts)
    Sort()

# Processing by language
def Sort():
    eng = []
    lang = []
    flag = 1

    for t in txt_new:
        word = str(t)
        punctions = [',', '[', ']', "'", '‘', '’', '“', '”']
        for mot in punctions:
            word = word.replace(mot, '')

        # Determine if it is all English
        if word.replace(' ', '').isalnum():
            lang.append('0')
            eng.append(word)
        else:
            lang.append('1')

    # Determine if the file types are the same
    for n in lang[1:]:
        if int(lang[0]) ^ int(n):
            flag = 0
            Error()
            break

    # Classification processing
    if int(flag):
        if eval(lang[0]):
            sims = chinese.Chinese(txt_name)
        else:
            sims = english.English(eng)
        Result(sims)

# Error
def Error():
    print('Error')
    root.withdraw()
    top = tk.Toplevel()
    top.title('Error')
    top.geometry('250x30')
    tk.Label(top, text="Text in different languages exists in the input file!").grid(row=0, column=0)
    tk.Button(top, text="Return", command=Return).grid(row=0, column=1)

# Return
def Return():
    root.destroy()
    Init()

# Result
def Result(sims):
    for n in range(len(sims)):
        num_lab = 1 + n * 2
        sim = sims[n]
        tk.Label(root, width=50, text=sim).grid(row=num_lab + 1, column=1)

# Interface
# Select the file
def SelectFile():
    global num_add
    root.withdraw()
    fn = tk.StringVar()
    fn = filedialog.askopenfilename(title="Select reference text file")
    tk.Label(root, width=50, text=fn).grid(row=num_add, column=1)
    root.update()
    root.deiconify()
    txt_name.append(fn)
    if num_add == 0:
        num_add = 1
    else:
        num_add += 2

# Add files
def AddFile():
    global num_lab
    num_lab += 2
    Lab(num_lab)
    But(num_lab)

# Controls
# Button
def But(num_lab):
    tk.Button(root, text="Select", command=SelectFile).grid(row=num_lab, column=2)
    tk.Button(root, text="Add reference file", command=AddFile).grid(row=num_lab + 2, column=0)

# Label
def Lab(num_lab):
    tk.Label(root, text="Please select a reference text file:").grid(row=num_lab, column=0)
    tk.Label(root, text="Text similarity calculation results:").grid(row=num_lab + 1, column=0)
    tk.Label(root, width=50).grid(row=num_lab, column=1)
    tk.Label(root, width=50).grid(row=num_lab + 1, column=1)

# Init
def Init():
    global root
    global txt_name
    global txt_new
    global num_lab
    global num_add

    # Setting interface properties
    root = tk.Tk()
    root.title('Text similarity detection system')
    root.geometry('700x600')

    txt_name = []
    txt_new = []
    num_lab = 1
    num_add = 0
    But(num_lab)
    Lab(num_lab)
    tk.Button(root, text="Select", command=SelectFile).grid(row=0, column=2)
    tk.Label(root, text="Please select a target text file:").grid(row=0, column=0)
    tk.Label(root, width=50).grid(row=0, column=1)
    tk.Button(root, text="Calculate similarity", command=Simplify).grid(row=100, column=1)
    tk.Button(root, text="Reset", command=Return).grid(row=100, column=2)

    # Run
    root.mainloop()

Init()
