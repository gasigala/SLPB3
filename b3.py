import string
import numpy as np
import pandas as pd
import sys
from sklearn.linear_model import LinearRegression

def makeDict():
    #make string of all letters
    letters = string.ascii_lowercase + "áéíóúüöß'ìã"

    #add all bigrams to string 
    b_list = [i+b for i in letters for b in letters]

    #add all bigrams to dict and set initial count to 0
    bigrams = dict.fromkeys(b_list, 0)
    return bigrams



def makeNgrams(ngramsDict, surname, N):
    #this method assumes that the possible combinations of our ngrams are already in
    #our dict
    ngrams =  [surname[i: j] for i in range(len(surname)) for j in range(i + 1, len(surname) + 1) if len(surname[i:j]) == N]
    for i in ngrams:
        ngramsDict[i] +=1
    
    
def bigram_dict_to_matrix(bigram_dict):
    return np.matrix(list(bigram_dict.values()))

def name_to_vec(name):
    

def trainTestSplit():
  #this will give us a count of the nationalities
  surname_dict = dict()
  surname_lst = []
  with open('surnames-dev.csv', mode="r", encoding="utf-8") as input_file:
            # open(sys.argv[2], mode="w", encoding="utf-8") as output_file:
          for surname in input_file:
              surname = surname.strip()
              #find the surnames count in a dict and make a list representation for easier count
              temp = surname.split(",")
              if temp[1] not in surname_dict:
                surname_dict[temp[1]] =1
              else:
                surname_dict[temp[1]] +=1
              surname_lst.append(temp[0])

  #make the file names were gonna write to
  #this popsup as a singular value for some reason
  #surname_dict.pop('"')
  trainset = 'train-set.csv'
  devset = 'dev-set.csv'
  testset = 'test-set.csv'
  
  count_total = 0
  with open(trainset, mode = "w",encoding = 'utf-8') as output_file,\
      open(devset, mode = "w",encoding = 'utf-8') as output_file2,\
      open(testset, mode = "w",encoding = 'utf-8') as output_file3:
    for nationality,count in surname_dict.items():
      #get the first 60% into out train-set.csv
      for i in range(count_total, int(count_total+(count*.6))):
        output_file.write(surname_lst[i])
        output_file.write(",")
        output_file.write(nationality)
        output_file.write("\n")
      #get the 60-80% range into out dev-set.csv
      for j in range(int(count_total+(count*.6)), int(count_total+(count*.8))):
        if '"' in surname_lst[j]:
          surname_lst[j] = surname_lst[j].replace('"', '')
        output_file2.write(surname_lst[j])
        output_file2.write(",")
        output_file2.write(nationality)
        output_file2.write("\n")
      #get 80-100% into our test-set.csv
      for k in range(int(count_total+(count*.8)), count_total+ count):
        output_file3.write(surname_lst[k])
        output_file3.write(",")
        output_file3.write(nationality)
        output_file3.write("\n")
      count_total += count   
        
    
def normalizeCounts(bigramDict):
  #this assumes our dictionary is all bigrams
  letters = string.ascii_lowercase
  dictCount = dict()
  #get the count of all bigrams that start with the letter a-z
  for i in bigramDict.keys():
    if i[0] not in dictCount:
      dictCount[i[0]] = bigramDict[i]
    else:
      dictCount[i[0]] += bigramDict[i]
#divide each bigram by the # of bigrams that start with a letter by the total number of bigrams that start with the same letter
  for i in bigramDict.keys():
    if bigramDict[i] != 0:
      bigramDict[i] = bigramDict[i]/ dictCount[i[0]]

  print(bigramDict)

def normalizeMat(bigramMat):
    if bigramMat.sum() == 0:
        print(bigramMat.sum())
    
    return bigramMat/bigramMat.sum()

def train_reg():
    train_file = open("train-set.csv",'r',encoding = 'utf-8')
    
    train_list = train_file.read().split()
    
    base_dict = makeDict()
    
    name = train_list[0]
    
    name = name.replace(" ", '')
    
    names = name.split(",")
    names[0] = names[0].lower()
    if "Russian" == names[1]:
        y = np.matrix([1])
    else:
        y = np.matrix([0])
    
    name_dict = dict.copy(base_dict)
    
    makeNgrams(name_dict, names[0], 2)
    
    X = bigram_dict_to_matrix(name_dict)
    
    X = normalizeMat(X)
    
    for l in train_list:
        l = l.replace(" ",'')
        l = l.replace("-",'')
        
        names = l.split(',')
        names[0] = names[0].lower()
        
        if len(names[0]) < 2:
            continue
        
        if len(names) == 2 and "Russian" == names[1]:
            y = np.concatenate((y,[[1]]),1)
        else:
            y = np.concatenate((y,[[0]]),1)
        
        name_dict = dict.copy(base_dict)
        
        makeNgrams(name_dict, names[0], 2)
        
        X1 = bigram_dict_to_matrix(name_dict)
        
        X1 = normalizeMat(X1)
        
        X = np.concatenate((X,X1))
    
    regr = LinearRegression().fit(np.asarray(X),np.asarray(y.transpose()))
    
    return regr


if __name__ == "__main__":
    trainTestSplit()
    train_file = open("train-set.csv",'r',encoding = 'utf-8')
    r = train_file.read()
    train_file.close()
    regr = train_reg()
    c = regr.coef_
    for i in range(32):
        print(c[0][i])
    