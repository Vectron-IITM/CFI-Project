from tkinter import *
from tkinter import filedialog

import mysql.connector

from threading import *

from nltk.tokenize import word_tokenize, sent_tokenize
from string import punctuation

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        #print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return
  
    
    
    
    
    
def EditDistDP(str1, str2):
    
    len1 = len(str1); 
    len2 = len(str2);
    
    #To fill the DP array with 0
    
    DP = [[0 for i in range(len1 + 1)] for j in range(2)]
    #Base condition when second string is empty then we remove all characters
    
    for i in range(len1 + 1):
        DP[0][i] = i
    #Start filling the DP This loop run for every character in second string
        
    for i in range(1,len2 + 1):

    #This loop compares the char from second string with first string characters 
        
        for j in range(len1 + 1):

    #if first string is empty then we have to perform add character operation to get second string
			
            if(j == 0):
                DP[i % 2][j] = i

    #if character from both string is same then we do not perform any operation . here i % 2 is for bound the row number. 
                
            elif(str1[j-1] == str2[i-1]):
                DP[i % 2][j] = DP[(i - 1) % 2][j - 1]

    #if character from both string is not same then we take the minimum from three specified operation 
                
            else:
                DP[i % 2][j] = 1 + min(DP[(i - 1) % 2][j], min(DP[i % 2][j - 1], DP[(i - 1) % 2][j - 1]))
	
    #after complete fill the DP array if the len2 is even then we end up in the 0th row else we end up 
    #in the 1th row so we take len2 % 2 to get row
    S = (1 - (DP[len2 % 2][len1])/(max(len1,len2)))*100
    return(S)

def Sentencing(sent1,sent2):
    #Extracting words from the sentences
    words1 = [w.lower() for w in word_tokenize(sent1) if w not in punctuation] 
    words2 = [w.lower() for w in word_tokenize(sent2) if w not in punctuation]

    #Common words giving zero edit distance
    words = set(words1) & set(words2)
    common_words = [w for w in words]
    common_words.sort()
    sen = " ".join(common_words)

    #Sentence 1 with alphabetically arranged words excluding common words
    sen1 = [w for w in words1 if w not in words]
    sen1.sort()
    sent1 = " ".join(sen1)

    #Similarly sentence 2
    sen2 = [w for w in words2 if w not in words]
    sen2.sort()
    sent2 = " ".join(sen2) 

    #Sentences with common words at the beginning followed by alphabetically arranged words
    sent1 = sen + ' ' + sent1
    sent2 = sen + ' ' + sent2
    return(EditDistDP(sent1,sent2))

def stripComments(sent):
    #When flag =1 indicates the characters part of comment which need to be omitted
    flag = 0
    sentence = ''
    for token in sent:
        if token == '#':
             flag = 1
        if '\n' in token :
            flag = 0
        if flag == 1:
            token = ''
        sentence = sentence + token
    return sentence

    
    

root = Tk()

root.title("Content Similarity")

myLabel = Label(root, text="CFI Programming Club")
myLabel1 = Label(root, text="Please Enter the MySQL Password")
#myLabel.grid(row=0, column=0)
myLabel.pack()
myLabel1.pack()

entryField = Entry(root, width=50)
entryField.pack()



def myClick():
    global pw
    pw = entryField.get()
    #myLabel2 = Label(root, text=pw)
    #myLabel.grid(row=0, column=0)
    try:
        mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = pw  #Enter your sql password
        )
    
        
        
        
        myLabel2 = Label(root, text="Connection to DataBase is successful")
        myLabel2.pack()
        
        myLabel1 = Label(root, text="Select the file to be inspected")
        myLabel1.pack()
        
        myButton = Button(root, text="Select", command=openFile)
        myButton.pack()

        
        
    except:
         myLabel2 = Label(root, text="Wrong Password")
         myLabel2.pack()
         

def openFile1():
        global filesTotal
        files=[]
        filename=[]
        
        
        pw = entryField.get()
        mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = pw  #Enter your sql password
        )
        
        mycursor = mydb.cursor()  #Used to establish connection with sql server

        #Creating database and table
        mycursor.execute("CREATE DATABASE IF NOT EXISTS plagirismcheck") 
        mycursor.execute("USE plagirismcheck")
        mycursor.execute("CREATE TABLE IF NOT EXISTS DATAS (FILENAME VARCHAR(255), SIMILARITY FLOAT(10))")
        mycursor.execute("DELETE FROM DATAS")
        
        
        filesTotal = filedialog.askopenfilenames(parent=root,title='Choose a file')
        filesTotal = list(filesTotal)    
        for i in filesTotal:
        
            inp = (i,0)
            mycursor.execute(sqlcmd, inp)     #Entering the names of files into the database
            filename.append(i)               #Store the file contents
            with open (i) as f:
                tokens2 = sent_tokenize(f.read())
                sent2 = ' '.join(tokens2)
                sent2 = stripComments(sent2)
                files.append(sent2)
                f.close()
        print()
        
        mydb.commit()
        
        Tobj=[]     #To store the returned percentages
        for fil in files:
            a = ThreadWithReturnValue(target=Sentencing, args=(sent1,fil))
            a.start()
            Tobj.append(a)
    
    #Entering the returned %ofsimilarity into the database
        for (val,fname) in zip(Tobj,filename):
            perc=val.join()
            sql = "UPDATE DATAS SET SIMILARITY = "+str(perc)+" WHERE FILENAME = '"+fname+"'"
            mycursor.execute(sql)
            mydb.commit()
        
    #Retrieving data from database to be displayed to user
        mycursor.execute("SELECT * FROM DATAS")
        data = mycursor.fetchall()
        for row in data:
            print(row)
            label = Label(root, text= str(row))
    # this creates x as a new label to the GUI
            label.pack()
    
def openFile(): 
    global sent1
    global sqlcmd
         #To store file contents in the list
       #To store file names in the list
    
    f1 = filedialog.askopenfilenames(parent=root,title='Choose a file')
    f1 = list(f1)
    listToStr = ' '.join([str(elem) for elem in f1])
    with open (listToStr) as f:
        tokens1 = sent_tokenize(f.read())
        f.close()
    sent1 = ' '.join(tokens1)
    sent1 = stripComments(sent1)
    
    myLabel1 = Label(root, text="Select all files needed to be checked with")
    myLabel1.pack()
    

    
    myButton1 = Button(root, text="Select", command=openFile1)
    myButton1.pack()
    
    sqlcmd = "INSERT INTO DATAS (FILENAME, SIMILARITY) VALUES (%s,%s)"
    
    
    
    #Opening the files
    
    
    
        
    
    
    
    
myButton = Button(root, text="Submit", command=myClick)
myButton.pack()
#myButton.grid()
    

root.mainloop()

