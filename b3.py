import string
import numpy as np
import pandas as pd
import sys
from sklearn.linear_model import LinearRegression

_bigrams = []

def get_sorted_bigram_list():
    src_file = "train-set.csv"
    src_stream = open(src_file,'r')
    bigram_list = []
    for ln in src_stream:
        name = ln.lower().strip().replace(" ",'').split(",")[0]
        for i in range(len(name)-1):
            if len(name) > 1 and name[i:i+2] not in bigram_list:
                bigram_list.append(name[i:i+2])
    
    bigram_list.sort()
    return bigram_list
    
_bigrams = get_sorted_bigram_list() + ['OOV']

def makeDict():
    #add all bigrams to dict and set initial count to 0
    bigrams = dict.fromkeys(_bigrams, 0)
    return bigrams



def makeNgrams(ngramsDict, surname, N):
    #this method assumes that the possible combinations of our ngrams are already in
    #our dict
    ngrams =  [surname[i: j] for i in range(len(surname)) for j in range(i + 1, len(surname) + 1) if len(surname[i:j]) == N]
    for i in ngrams:
        if i in ngramsDict:
            ngramsDict[i] +=1
        else:
            ngramsDict['OOV']+=.01
    return ngramsDict
    
def bigram_dict_to_array(bigram_dict):
    return np.array([list(bigram_dict.values())])

def name_to_vec(name):
    return bigram_dict_to_array(makeNgrams(makeDict(), name, 2))

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
    
    X = np.empty((1,len(_bigrams)))
    y = np.empty((1,1))
    
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
        
        
        X1 = name_to_vec(names[0])
        
        #X1 = normalizeMat(X1)
        
        X = np.concatenate((X,X1))
    
    regr = LinearRegression(copy_X=(True),fit_intercept=(True)).fit(np.asarray(X),np.asarray(y.transpose()))
    
    return regr


if __name__ == "__main__":
    np.random.seed(0x33)
    #uncomment to initialize the files
    #trainTestSplit()
    regr = train_reg()
    
    THRESHOLD = .5
    
    eval_name = 'dev-set.csv'
    print("Predicting on file" + eval_name)
    
    #tp - true positives
    #fp - false positives
    #tn - true negatives
    #fn - false negatives
    tp,fp,tn,fn = 0,0,0,0
    #keep track of the max and minimum model predictions.
    max_pred,min_pred = 0,0
    eval_results = []
    eval_file = open(eval_name,'r')
    
    for eval_ln in eval_file:
        ln_data = eval_ln.strip().replace(" ",'').split(",")
        expected = int(ln_data[1] == "Russian")
        name_vec = name_to_vec(ln_data[0].lower())
        #Returns a nested array, this unwraps it.
        pred = regr.predict(name_vec)[0][0]
        actual = int(pred > THRESHOLD)
        max_pred = {True:pred,False:max_pred}[pred > max_pred]
        min_pred = {True:pred,False:min_pred}[pred < min_pred]
        #Use bool -> int cast to figure out place on confusion table.
        tp += expected == 1 and actual == 1
        fp += expected == 0 and actual == 1
        fn += expected == 1 and actual == 0
        tn += expected == 0 and actual == 0
        #Use this line if you want to store the prediction
        #eval_results.append((ln_data[0],expected,actual,pred))
        #Else, use this line
        eval_results.append((ln_data[0],expected,actual,pred))
    eval_file.close()
    total = tp + tn + fp + fn
    
    print((tp,tn,fp,fn))
    acc = (tp+tn)/total
    recall = tp / (tp + fn)
    precision = tp / (tp + fp)
    print((tp,tn,fp,fn))
    print("accuracy: ",acc)
    print("recall: ",recall)
    print("precision: ", precision)
    
    
    