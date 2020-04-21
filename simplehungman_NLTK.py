# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 18:36:30 2020

@author: pssiv
"""
import string
import random
from nltk.corpus import words

def Get_word():
    wordlist = words.words()
    wordTobeGuessed = random.choice(wordlist)
    return wordTobeGuessed

def Get_difficulty():
    difficulties = ['easy','medium','hard']
    attempts = {'easy': 15, 'medium': 10,'hard':6}
    
    for index, difficulty in enumerate(difficulties):
        print('Select {0} for {1}'.format(index+1,difficulty))
    try : 
        inputDifficulty = int(input('Enter the difficulty level: '))
        if str(inputDifficulty) in str(123):
            return attempts[difficulties[inputDifficulty-1]]
        else:
            Get_difficulty()
    except ValueError:
        print('Invalid input: Enter a integer')
        
        
def Check_guess(charInp,word,wordSoFar,charFound,attempt):
    wordFound = False
    if charInp in word:
        print('Correct guess')
        charFound += word.count(charInp)
        for index, character in enumerate(word):
            if character == charInp:
                wordSoFar[index] = charInp
                wordFound = True if charFound == len(word) else False                
    else:
        print('Wrong guess')
        attempt-=1
    return wordFound,wordSoFar,attempt,charFound

def Guess(attempt, word):
   remainingLetters = list(string.ascii_lowercase)
   wordFound = False
   wordSoFar = ['_']*len(word)
   charFound = 0
   while attempt>0:
       print('\n{0} attempts remaining'.format(attempt))
       for ele in wordSoFar:
           print(ele, end=" ")
       charInp = str(input('\nGuess a char: ')).lower()
       if len(charInp) != 1:
           print('Guess only one character')
           continue
       if charInp not in remainingLetters:
           print('Guessed already!')
           continue
       else:
           wordFound,wordSoFar,attempt,charFound = Check_guess(charInp,word,wordSoFar,charFound,attempt)           
                          
           remainingLetters.remove(charInp)
           
           if wordFound:
               print('\n\nYou won!')
               break
   else:
       print('\n\nYou Lost.')
       print('Word is {0}'.format(word))

def Hungman():
   attempt  = Get_difficulty()
   word = Get_word()
   
   print('Total Attempts: {0}'.format(attempt))
   print('Length of the word: {0}'.format(len(word)))
   #print('_ '*len(word))
   
   Guess(attempt, word)

                     
Hungman()