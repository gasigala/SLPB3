import string
import numpy as np

def makeDict():
    #make string of all letters
    letters = list(string.ascii_lowercase)

    #add all bigrams to string 
    letters.extend([i+b for i in letters for b in letters])

    #add all bigrams to dict and set initial count to 0
    bigrams = dict.fromkeys(letters, 0)
    return bigrams

def makeNgrams(ngramsDict, surname, N):
    #this method assumes that the possible combinations of our ngrams are already in
    #our dict
    ngrams =  [surname[i: j] for i in range(len(surname)) for j in range(i + 1, len(surname) + 1) if len(surname[i:j]) == N]
    for i in ngrams:
        ngramsDict[i] +=1

