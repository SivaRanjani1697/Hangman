# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 17:30:26 2020

@author: pssiv
"""

import string
import time
import random
import pandas as pd
from tkinter import *

class HangMan:
    def __init__(self,window):
        self.canvas = Canvas()
        self.window = window
        self.window.geometry("600x400")
        self.window.title('HangMan')
        # create screen widget
        self.screen = Text(window, state='disabled', width=73, height=3,background="light gray", foreground="blue")
        self.screenlabel = Label(window,text='Hangman',font='Courier 18 bold',background="light gray")
        
        # position screen in window
        self.screen.place(x=5,y=5)#340)
        self.screenlabel.place(x=10,y=10)
        self.screen.configure(state='normal')
        
        #set difficulty level
        self.selected = IntVar()
        self.selected.set(1)
        self.rad1 = Radiobutton(window,text='Easy', value=1, variable=self.selected)
        self.rad2 = Radiobutton(window,text='Medium', value=2, variable=self.selected)
        self.rad3 = Radiobutton(window,text='Hard', value=3, variable=self.selected)

        self.btn = Button(window, text="Click Me",command=lambda:self.Get_Difficulty(window))

        self.rad1.place(x=310,y=60)
        self.rad2.place(x=360,y=60)
        self.rad3.place(x=430,y=60)
        self.btn.place(x=500,y=60)
        
        
        #initialize default values
        self.attempt = 0
        self.remainingLetters = list(string.ascii_lowercase)
        self.wordFound = False
        self.charFound = 0
        self.guess = Label(window,text='Select the difficulty level to proceed')
        self.guess.place(x=310,y=100)
        
        
    def Get_Difficulty(self,window):
        self.rad1.destroy()
        self.rad2.destroy()
        self.rad3.destroy()
        self.btn.destroy()
        self.guess.configure(text='')
        difOption = self.selected.get()
        difficulties = ['easy','intermediate','difficult']
        attempts = {'easy': 15, 'intermediate': 10,'difficult':5}
        
        self.attempt = attempts[difficulties[difOption-1]]
        self.totalAttempt = self.attempt
        diff ='Total Attempts     : {0}'.format(self.attempt)
        self.labeldiff = Label(window,text=diff)
        self.labeldiff.place(x=310,y=60)
        print('Total Attempts:     {0}'.format(self.attempt))
        
        self.word = self.Get_word()
        self.wordSoFar = ['_']*len(self.word)
        self.Display_GuessedWord()
        self.letterPanel()
        
        
    def letterPanel(self):
        buttons = [None]*26
        for index, ch in enumerate(list(string.ascii_lowercase)):
            buttons[index] = self.createButton(ch)
        
        idx=0
        x,y = 250,150
        for i in range(5):       
            for j in range(5):
                buttons[idx].place(x=x,y=y)
                x += 70
                idx+=1
                
            x,y = 250,y+40
            
        buttons[25].place(x=390,y=350)
    def Get_word(self):
        data = pd.read_csv('inputFile.txt',delim_whitespace=True)['wordform']
        word = random.choice(data)
        return word
    
    def createButton(self,ch,width=7):
        return Button(self.window, text=ch,width=width, command= lambda:self.CheckGuess(ch))
    
    def Display_GuessedWord(self):
        wordGuessed = ' '.join(self.wordSoFar)
        self.screenlabel.configure(text=wordGuessed)
    
    def CheckGuess(self,charInp):
        if self.attempt>0 and not self.wordFound:
            if charInp not in self.remainingLetters:
                print('Guessed already!')
                self.guess.configure(text= 'Guessed already!' )
                
            else:
                if charInp in self.word:
                    print('Correct guess')
                    self.guess.configure(text= 'Correct guess' )
                    self.charFound += self.word.count(charInp)
                    for index, character in enumerate(self.word):
                        if character == charInp:
                            self.wordSoFar[index] = charInp
                            self.wordFound = True if self.charFound == len(self.word) else False    
                    self.Display_GuessedWord()      
                else:
                    print('Wrong guess')
                    self.guess.configure(text= 'Wrong guess' )
                    self.attempt-=1
                    self.Draw_Hangman()
                    
                self.remainingLetters.remove(charInp)
                self.labeldiff.configure(text = 'Attempts Remaining    : {0}'.format(self.attempt))
                
                if self.wordFound:
                    print('\n\nYou won!')
                    self.guess.configure(text= 'You Won' )
                    window.after(2000,lambda:window.destroy())

        else:
            print('\n\nYou Lost.')
            print('Word is {0}'.format(self.word))
            self.guess.configure(text= 'You lost' )
            window.after(2000,lambda:window.destroy())
        
    def Draw_Hangman(self):
        hm = [None]*17
        
        hm[0] = (20,200, 200,200)#base
        hm[1] = (120,20, 120,200)#stand
        hm[2] = (120,20,170,20)# ceil 
        hm[3] = (170,20,170,40)#small vertical

        hm[4] = (155,40,185,70)#head
        hm[5] = (170,70,170,170)#body

        hm[6] = (170,80,150,100)#handleft
        hm[7] = (170,80,190,100)#handright

        hm[8] = (170,170,150,190)#legleft
        hm[9] = (170,170,190,190) #legright 

        hm[10] = (120,170,130,200) #bottom stand right
        hm[11] = (120,170,110,200)  #bottom stand left

        hm[12] = (130,20,120,40)  #top stand left
        hm[13] = (160,20,170,40)  # top stand right

        hm[14] = (165,50,165,50) #eyes left
        hm[15] = (175,50,175,50)#eyes right

        hm[16] = (165,60,175,60) #mouth
        
        hg = self.totalAttempt-self.attempt
        if self.totalAttempt ==15:
            if self.attempt == 10:
                self.canvas.create_oval(hm[4])
            elif self.attempt == 0:
                self.canvas.create_oval(hm[14])
                self.canvas.create_oval(hm[15])
                self.canvas.create_oval(hm[16])
            else:
                self.canvas.create_line(hm[hg-1])
        elif self.totalAttempt == 10:
            if hg ==5:
                self.canvas.create_oval(hm[hg-1])
            else:
                self.canvas.create_line(hm[hg-1])
                
        else:
            if hg==2:
                self.canvas.create_oval(hm[4])
            elif hg==1:
                for i in range(4):
                    self.canvas.create_line(hm[i])
            elif hg ==3:
                self.canvas.create_line(hm[5])
            elif hg ==4:
                self.canvas.create_line(hm[6])
                self.canvas.create_line(hm[7])
            elif hg ==5:
                self.canvas.create_line(hm[8])
                self.canvas.create_line(hm[9])
        self.canvas.place(x=5,y=150)
        


window = Tk()
hg = HangMan(window)
window.mainloop()