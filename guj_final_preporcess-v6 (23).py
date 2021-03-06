# -*- coding: utf-8 -*-
"""guj_preprocess_modules.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gVCtIAx0l3hMwN1oec77kdT8B0Hf9ErJ
@author: NIKITA

"""
##!cp "/content/drive/My Drive/Colab Notebooks/guj_final_preporcess-v6.py" "guj_final_preporcess.py" 
# command to include this #file in the RE of colab 

def guj_web_scrap_multiplepage(seed,filename):
 import io

 

 import wikipedia as wk
 wk.set_lang('gu')
 firstpage=wk.page(1)
 try:
    #firstpage=wk.page("મુનશી પ્રેમચદ ")
    firstpage=wk.page(seed) #start scrapping wiki pages from this seed word
    data=firstpage.content

   # print('data is',data)
    with io.open(filename,'a+',encoding='utf8') as f:
                f.write(data) 
 except wk.exceptions.PageError:
    pass

 if firstpage:
    extralinks=firstpage.links
   

    for i in extralinks:
        #if count > 0:
    
                try:
                    newpage=wk.page(i)
                    data=newpage.content
                   # count=count-1
                    with io.open(filename,'a+',encoding='utf8') as f:#append to file if it exists otherwise create new one
                        f.write(data) 
            
                except wk.exceptions.PageError:
                    pass



 return(filename)
              
                



"""WEB SCRAPPING ::: FETCHING DATA FOR WORKING (FROM WIKIPEDIA)(small file)"""
def guj_web_scrap_singlepage(seed,filename):
 import io
 import wikipedia as wk

 wk.set_lang('gu')
 firstpage=wk.page(1)
 try:
	    firstpage=wk.page(seed) #get information about the given seed word in wiki
	    data=firstpage.content
   #print('data is',data)
	    with io.open(filename,'a+',encoding='utf8') as f:
        	        f.write(data) 
 except wk.exceptions.PageError:
      return(filename)
  #print("the name returned back is ",datafile)    
 return(filename)
 

       
   
     
 
def guj_clean_extra(originalfile,resultfile):
    #remove the extra marks like multiple exclamations, and quotes outside taken inside and puncutation placed outide.
  import re
  import io  
  
  with io.open(originalfile,'r',encoding='utf-8') as f: 
       lines=f.read()
  lines=re.sub(r"\![\!\.\?]+","!",lines) #exclamation followed by other punctuations 
 
  lines=re.sub(r"\?[\!\.\?]+","?",lines) # question mark followed by other punctuations 
 
  lines=re.sub(r"\.[\!\.\?]+",".",lines) # dot mark followed by other punctuations 
 #sequence of punctuations before quotes ,shud be removed .only the one before  shud be preserved.,which wud subsequently taken outside 
  lines=re.sub(r"\.[’][\!\.\?]+",".’",lines)
  lines=re.sub(r"\.['][\!\.\?]+",".'",lines)
  lines=re.sub(r'\.["][\!\.\?]+','."',lines)
  lines=re.sub(r"\.[’’][\!\.\?]+",".’’",lines)

 
 #remove redundant same symbols in sequence
  lines=re.sub(r"\n+"," ",lines) #remove  extra newlines 
  lines=re.sub(r"!+","!",lines) #replace multiple exclamations with single
  lines=re.sub(r" +"," ",lines) #replace extra whitespaces with single whitespace
  lines=re.sub(r"[ ]+\.",".",lines) #remove extra space between last symbol and dot 
  lines=re.sub(r"\?+","?",lines) #remove multiple question mark with single
  lines=re.sub(r"\.+",".",lines) #replace multiple dot marks with single
 
  lines=re.sub(r"\.\s*’","’.",lines)#.Pattern :- start with dot(escape the sp meaning)  followe by zero or more whitespace nd then quotes
  lines=re.sub(r"\.\s*'","'.",lines)#single quotes handled
  lines=re.sub(r'\.\s*"','".',lines)#double quotes handled
  lines=re.sub(r'\.\s*”','”.',lines)#double quotes handled
  lines=re.sub(r"\.\s*’’","’’.",lines)#single quotes written twice handled
 
  lines=re.sub(r"\?\s*’","’?",lines)#single quotes handled
  lines=re.sub(r"\?\s*'","'?",lines)#single quotes handled
  lines=re.sub(r'\?\s*"','"?',lines)#double quotes handled
  lines=re.sub(r'\?\s*”','”?',lines)#double quotes handled
  lines=re.sub(r"\?\s*’’","’’?",lines)#single quotes written twice handled
 
  lines=re.sub(r"!\s*’","’!",lines)#single quotes handled
  lines=re.sub(r"!\s*'","'!",lines)#single quotes handled
  lines=re.sub(r'!\s*"','"!',lines)#double quotes handled
  lines=re.sub(r'!\s*”','”!',lines)#double quotes handled
  lines=re.sub(r"\!\s*’’","’’!",lines)#single quotes written twice handled
 
 
 #sequence of puncutations replaced by only the first one. 
  lines=re.sub(r'\![\!\.\?]+',"!",lines) #exclamation followed by other punctuations 
 
  lines=re.sub(r"\?[\!\.\?]+","?",lines) # question mark followed by other punctuations 
 
  lines=re.sub(r"\.[\!\.\?]+",".",lines) # dot mark followed by other punctuations 
  lines=re.sub(r"[(].*[)]"," ",lines) # content in brackets only to elaborate point ,so directly removed from the source itself.
 
  with io.open(resultfile,'w',encoding='utf-8') as w:
   w.write(lines) 
               
  return(resultfile)
  
def guj_clean_html(originalfile,resultfile):
    #remove the html tags and update the given input file
  import re
  import io  
  
  with io.open(originalfile,'r',encoding='utf-8') as f: 
       lines=f.read()
  lines=re.sub('\<DOCNO\>.*\</DOCNO\>','',lines)# remove the document tags
  lines=re.sub('\<.*\>',' ',lines)#remove all other tags
  lines=re.sub(r'\ufeff','',lines) #replace the special encoding code mentioned at start of html files
  
  
  
  with io.open(resultfile,'w',encoding='utf-8') as w:
   w.write(lines) 
               
  return(resultfile)
  




def guj_clean_text(originalfile,resultfile):
    #replace the inconsistent usage of quotes after sentence end.
 from indicnlp.tokenize import sentence_tokenize
 import re
 import io        
 #list of generally found valid sentence boundary words which can be followd by dot .
 #For others,heuristic of lenght is used.(if length of word having dot as suffix is less than 3 , it is possibly an abbreviation )
 #the single and two symbol string with dot are considered abbreviations in indic nlp. so we override it.
 boundarylist=['હતાં','હતા','હતું','હતી','હતો','હતો','ગઈ','ગયો','ગઇ','છું','દે','નહિ','નથી','કરે','થયા','થઈ','થઇ','જશે','થતો','થશે','રહી','છે','છો','છુ','શકે','તે','જા','અહીં','થી','આવ','દો','કર','થાય','પર','જાય','માટે' ,'પરથી','આવ્યું','સુધી','થાય','હતો','થઈ','સાથે','લાગે','હોવા','છતાં','રહેલા','કર્યુ','જુઓ','જાઓ','શકો','નથી','થતો','નહી','હોત','હશે','હોવું','તો','લે'] 
 endquotes=["'",'"',"’","”"] #if ending with quotes then ignore it .
 numerals=["0","૧","૨","૩","૪","૫","૬","૭","૮","૯","0","o"]
 with io.open(originalfile,'r',encoding='utf-8') as r:
       lines=r.read() #get all the lines back from proper segmented lines  
 listlines=sentence_tokenize.sentence_split(lines, lang='gu')
 replacedict={}
 """
 vocablist=guj_makevocab(originalfile)#get all words in given file
 with io.open(resultfile,'w',encoding='utf-8') as w:
     for word in vocablist.key():
         possibleword=word+'.'
         
"""
     
 
 with io.open(resultfile,'w',encoding='utf-8') as w:
  for line in listlines: #find all dots for abbreviations .
   matchingwords=re.findall('[\S]+[\.]',line)  #find all prefix with dot at end in one line 
   #print("matching words are ",matchingwords)
   for m in matchingwords: #for each word having dot at end in the find is it abbreviation word
      basicword=m.strip('.') # get baseword by removing ending dot
      #print("basic word taken is ",basicword)
      if basicword.endswith(tuple(endquotes)) :
           continue                  
      if basicword.endswith(tuple(numerals)): #it is float number,so wud be handled by indicnlp 
          continue
      if  basicword not in boundarylist : # check is it allowed boundary word then dont modify the subsequent dot
        if len(basicword)<=2:# Check is length of word found is two small then it is  abbreviation
           originalword=' '+basicword+'.' #take original word,ensure it is standalone and not part of other word
           newword=' '+basicword+'*' #make the replacement word
           line=re.sub(originalword,newword,line) #direct replace all occurences.
         #  print("mathing orginal and replaced words are "+originalword+" "+newword)
         #  replacedict[originalword]=newword   #maintain the words which are found with abbreviations and their replacement strings with *
   w.write(line) #write the processed line in result file
 

 
 with io.open(resultfile,'r',encoding='utf-8') as r:
     lines=r.read()#get back now the updated contents after handling the abbreviations and handle rest data.
 #print("the updated lines in the resultfile are ",lines)
 #sequence of puncutations replaced by only the first one. 
 

 

 with io.open(resultfile,'w',encoding='utf-8') as w:
       w.write(lines)
       
    
 return(resultfile)

 


 
def guj_stopwordremoval(originalfile,resultfile):
#need to send the file name containing data to be tokenized. 
 import io
 import re
 #static words in stopword list
 from indicnlp.tokenize import indic_tokenize
 stoplist=['હતાં','એમ','છે','છો','છુ','હતા','હતું','હતી','હોય','હતો','તેમાં','અને','તથા','તો','છું']
 lines=guj_sentence_segmenter(originalfile)
 with io.open(resultfile,'w+',encoding='utf-8') as w:  
  for line in lines:
     newline=''
     #print("original line for stopword check is ",line) 
     alltokens=indic_tokenize.trivial_tokenize_indic(line)#get list of all tokens found from original sentence 
     wordtokens=guj_mytokenizer(line) #get only the words tokens 
     for tok in alltokens:
        # print("token recieved is ",tok)
         if tok in wordtokens:
         #  print("token is word - ",tok)
           if tok not in stoplist:
              newline=newline+tok+" "
         else:
          # print("got non word token ",tok)
           newline=newline+tok+" "
     #print("newline formed after removal of stopwords is ",newline)        
     w.write(newline)   
 #guj_clean_extra(resultfile,resultfile)    
 return(resultfile)  	  

 
  
 
def guj_makedictionary(dictionaryfile):
 #returns dictionary made using self made list

 import csv
 mydictionary=[]
 listall=[]
 with open(dictionaryfile, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
       listall.append(row)

 for line in listall:
  for word in line:
    
    mydictionary.append(word)
 mydictionary=set(mydictionary) 
 
 return mydictionary
 
def guj_stemmer_new(originalfile,resultfile,dictionary,focus_list):
#using the dictionary to stem and also focus list to stop stemming the proper names sent 
 import io
 import re
 with io.open(originalfile,'r',encoding='utf-8') as f: 
		  lines=f.read()#get all the lines from file

 stemmedresultfile='stemmingdata.csv' #to store the original word and stem word found for all words in given file . 
 vocablist=guj_makevocab(originalfile) # make vocabulary list of words for given file. 
 #to generate the modified file 
 stemmedwordslist=[]
 lemmawordslist=[]
 replacedict={}
 mycorpora=guj_sentence_segmenter(originalfile) #get the sentences in datafile 
 
 with io.open(stemmedresultfile,'a+',encoding='utf-8') as s: #store the stemmed word set ,  with original word
  for word in vocablist:
      
      isdict=0 #Flag to identify it is dictionary word or not 
      sword,isdict=guj_stem_withdict(word,dictionary,focus_list) #else find stemword and pass the dictionary of words and nouns-named entities available 
          #print('original word , stemmed word and flag ----> ',word,sword,isdict )
      if isdict==1:
              #print("got the dictionary word so adding in dictionary list ",sword)
              lemmawordslist.append(sword) # the dictionary word was found so it was lemma form
      else:
              stemmedwordslist.append(sword) #maintain list of all stemmings done
              
      if sword!=word:
          replacedict[word]=sword #make entry in replacement dictionary ,replace original word with this stemword
          s.write("{0},{1}\n".format(word,sword))
          

 from indicnlp.tokenize import indic_tokenize
 
 
 with io.open(resultfile,'w+',encoding='utf-8') as w: #store the stemmed sentences back in file
        #divide lines into sentences
   for line in mycorpora:
     alltokens=indic_tokenize.trivial_tokenize_indic(line)#get list of all tokens found from original sentence 
     wordtokens=guj_mytokenizer(line) #fetch only the words in line 
     newline=''  #newline to be formed after replacement 
     #print("original line for stemming was---",newline)
     for basictoken in alltokens:
       if basictoken in wordtokens:#the token is word 
           if basictoken in replacedict.keys(): #the basictoken is a word which was trimmed and so in dictionary
               stemword=replacedict[basictoken]
               newline=newline+stemword+" "
           else:
               newline=newline+basictoken+" "
       else:
           newline=newline+basictoken+" "
     #print("new line after stemming was ",newline)    
     w.write(newline)#write the modified line in result file 
 
 guj_clean_extra(resultfile,resultfile)      
 return(resultfile,stemmedwordslist,lemmawordslist)


 
def guj_spellcheck(word,dictionary): # check the word in dictionary ,make corrections if needed and return back correct word
    #returns back word and status , if valid dictinary word returned then status is 1 else 0
    import io
    import re
     
                 
    if word in dictionary:
        return (word,1) #valid word ,so return it back and "1" indicates it is valid dictionary word
    replacementcharacters={#frequently inconsistent replacements are directly replaced
    "્ઋ":"ૃ","ગ્ન":"જ્ઞ","ઋ":"ૠ","ઑ": "ઓ",':' : '', "ઇ":"ઈ" , "જિ":"જી","ઊ":"ઉ","િ":"ી","ી":"િ","ુ":"ૂ","ૂ":"ુ"}
    
    for key in replacementcharacters.keys():
                      
                      if word.find(key) !=-1:
                         nword=re.sub(key,replacementcharacters[key],word)#else do the replacment 
                         
                         if nword in dictionary:
                             return (nword,1) 
                              
             
    return(word,0)#no mathces found in dictionary,so return word back as it is.    
               
def guj_sentence_segmenter(originalfile):
 # input is original text file and returns back the list of sentences formed using punkt tokenizer 
 
 from indicnlp.tokenize import sentence_tokenize
 import io
 import re
 
 with io.open(originalfile,'r',encoding='utf-8') as f: #get the original file content
         lines=f.read()
 sentences=sentence_tokenize.sentence_split(lines, lang='gu') #divide lines into sentences
 return(sentences)



             
def guj_mytokenizer(line):
    #find word tokens in a given line 
 import re
 import io
 tokens=[]
 excludelist=["!",".","(",")","`",",","-","?",'"','”',";",":","’","'",'“','”','”',"‘","“","*",'\"']
 for word in line.split():#split based on whitespaces the words from given line 
        
        next=0
        for symbol in excludelist: 
           if word==symbol: #word is punctuation ,then dont include it as token and check  next word 
              next=1
              continue
           pos=word.find(symbol)
           if pos>-1 and len(word)>1: #symbol found in word and it is not the puntuation symbol
              word=word.strip(symbol)
              continue
           
        if next==0:
              tokens.append(word) #current word to be added as token
              
 return (tokens)
             
def guj_makevocab(datafile):
  import io
  mycorpora=[]
  mycorpora=guj_sentence_segmenter(datafile)
  #divide lines into sentences
  words=[]
  for line in mycorpora:
     for word in guj_mytokenizer(line):
        if word not in ['!',".","(",")","`",",","-","?",'"','”',";",":","’","‘","“","*"," ",")"]: #dont take punctutions in the vocabulory 
          words.append(word)
  words=set(words) #Get the unique words in entire text 
  vocab={} #store the words found in a dictionary 
  key=0
  for word in words:
    vocab[word]=key
    key=key+1
  
  return(vocab)      
           
    
 
def remove_salutes(word):
     import re
     
     salute_word_list=["સાહેબ","બહેન","ભાઈ","બેન","ભઈ","ભઇ","કુમાર","કૂમાર","કાકા","કાકી","માસી","માસા","દાદા","માતા"]
     for sword in salute_word_list:
        if  (word.find(sword)>0):#saluation is after some name of minimum 1 charachter then update the word
         word=re.sub(sword,"",word)
         return (word)
     return(word) #else return same word without any modification     

     
            
def guj_stem_withdict(word,dictionary,focus_list):      
 import io
 import re
 if(word.find('-')!=-1): #word is a multiword expression ,so dont stem it 
   return (word,0) 
   
 listwords=dictionary#all words in our dictionary stored
 
 word=remove_salutes(word)#words with bhai or bahen or saheb attached are stripped 
 
 dword,status=guj_spellcheck(word,dictionary)#check the word in dictionary,if found equivalent word ,return that as replacment word and also if found original word , send status as 1 
 if status==1:
    return (dword,1) #found dictionary word ,return it 
 
 nounword,status=guj_spellcheck(word,focus_list) #check is given word a valid Named entity sent,then also return back with status 1
 if status==1:
     return (nounword,1)
     
 suffixes ={  1: ["ો", "ી" ," ે", "ા" , "ૂ", "ે" , "ૢ", "ૄ" ,"ૈ" , "ૌ"  ,"ુ","્","ઈ","એ","ઇ"],
   2: ["ઓએ","ીઓ" ,"ીએ","ોએ" ,"ાઓ","ાઈ","ાઇ","થી","ના","ની","ને","નો" ,"નુ","મા","મી","મુ","શે" ,"ીશ","શો","મત","ઓ","એ" ,"ું","ંુ","ાં","ંા","ંૂ", "ૂં",
"તો","તી","તા","યા","યુજે","ાય","યો","કે","જો","જી","ેલ","વા","વી"] ,
            3: ["ાઓએ","ઓના", "ઓનુ","ઓમા","ઓનો","ઓની","ઓને","ઓથી","ઓના","નું","નાં","માં","તાં","યું","યાં","તું","મું","વાં","ોને" ,"ોની" ,"ાના","ાની" ,"ભરી","ાને",
"ાનો" ,"ોનુ","માન","ીતા", "કાળ","ોથી" ,"દાર", "જનો","ાવે","ાવી","ાવર","વું","ેથી","પણુ","ેલી","ેલા","નાર"],
            4: [ "ીઓની","ઓનું","ઓનાં","ઓમાં","ાઓની" ,"ોઓથી" , "ાઓનો", "ાઓને","ાઓનુ","ોનાં" ,"ોનું" ,"ાનાં", "ાનું", "વાળા","વાળી","પૂ઼ણઁ","વેરા","વાળો","પણું",
"માથી","ાવીશ", "ેલોરી",
"વાથી","વાના","વાનો","વાની","નારી","નારો","ીશુ","ેલાં","ેલું"] , 
            5: ["ાઓનું","માંથી" , "વાનાં","ીશું","પૂર્વક" ,"વામાં","વાનું" ,"વાળું","વવાની","વવાનો","યાનાં"],
   6:[ "વાળાએ","વાળાઓની", "વાળાઓનું","વાળાઓનુ", "વાળાની" , "વાળાનો","વાવાળા","ોમાંથી"  ]
   }

 prefixes =   ["બિન","ગેર","સર્વ", "અર્ધ","શ્રી"]
 replacementlist=    {"ન્યાં" :"ન","ન્યા" :"ન",
"ન્યાના": "ન","ન્યાની":"ન","ન્યાનો":"ન","ન્યા" :"ન",
"ન્યું":"ન", "ન્યુ":"ન", "ન્યો" :"ન", "વ્યાનાં" : "વ", "વ્યાના" : "વ","વ્યાની" : "વ", "વ્યો": "વ",
"વ્યાં" :"વ","વ્યા":"વ", "વ્યાના":"વ", "વ્યાનું":"વ", "વ્યાનુ":"વ",  "વ્યાનો" : "વ",
  "વ્યુ":"વ","વ્યે" :"વ", "પ્યા": "પ",
"પ્યું":"પ", "પ્યુ":"પ", "પ્યો":"પ" , "પ્યાં":"પ", "પ્યા":"પ","પ્યાની": "પ","પ્યાનો": "પ",
"પ્યુ" :"પ","ખ્યાનું":"ખ", "ખ્યાનુ":"ખ","ખ્યા":"ખ", "ખ્યું":"ખ","ખ્યુ":"ખ","ખ્યાં" :"ખ","ખ્યા" :"ખ",
"ખ્યાના":"ખ","ખ્યો":"ખ","ળ્યા":"ળ","ળ્યું" :"ળ","ળ્યુ" :"ળ","ળ્યાં" :"ળ","ળ્યા" :"ળ",
"ળ્યો": "ળ","લ્યાં" : "લ","લ્યા":"લ","લ્યું" :"લ","લ્યુ":"લ","લ્યો":"લ",
"લ્યે": "લ","વવુ":"વ","વવું":"વ","રું":"ર","વવો":"વ"

  }  # Extra similar replacements added to match the words without ending anusvar which are removed in normalizing
 
 while True:#infinite loop ,to continue for currentword only stop when no updation done 
  flag=0
  
  #step1 Check if a number ,then remove the extra word inflection at end 
  number=["૧","૨","૩","૪","૫","૬","૭","૮","૯","0","૦"]
  if word.startswith(tuple(number)): #check is the given word a number? 
    regex = re.compile('[^૧૨૩૪૫૬૭૮૯0૦]')#if yes then remove its non numeric suffix part
    word=regex.sub('',word)
    return (word,0) #now return back, no other processing needed. 
  
  #step2 check if prefix matches ,then remove it 
  for pref in prefixes:
        if word.startswith(pref) and word>pref:  #check the word is only starting with this and is not entire word
            word=re.sub("^{0}".format(pref),"",word,1)
            flag=1
            break #continue with next step 
  #step3 Check the subsitution rules ,if found match ,replace  it .
            
  for key in replacementlist.keys():
        
        if word.endswith(key) and word>key: #check the word is actually end of string and not directly the string. 
          word=re.sub("{0}".format(key),"{0}".format(replacementlist[key]),word,1)
          flag=1
          return (word,0) #return back now no need to do more stemming ,else wud get overstemmed
         
      
   #step4 Check the suffix , if found match , remove it.          
  
  
  start=len(word)#start checking from list with as per the extra symbols after 3 in source.
  start=start-2
  if start>6 : #as suffix of length 6 and less , so  we limit the start range from 6 
      start=6
   
  for L in  range(start,0,-1): #
           
            
            
          
            for suf in suffixes[L]:
            
                if word.endswith(suf):
                   
                    possibleword=re.sub("{0}$".format(suf),"",word)
                
                    if len(possibleword)>=2: #if trimmed word becomes smaller than 2 size ,it might not be proper stem ,so dont use it 
                        word=possibleword #else use the trimmedword as the stemword
                       
                        flag=1 #one replacement done ,maybe till end ..then try for other possible .
                        break
                    
            if flag==1:
              dword,status=guj_spellcheck(word,dictionary)#check the word in dictionary,if found equivalent word ,return that as replacment word
              if status==1:
                 return (dword,0) #found dictionary word after stemming ,so stop further trimming and return but keep flag off to indicate it was stemmed 
            if flag==1:
              nounword,status=guj_spellcheck(word,focus_list)
              if status==1:
                 return (nounword,0)#found the nounword after stemming,so dont continue further trimming.
  
  if flag==0:
     break
 return (word,0) #return word and flag as not dictionary word 

def guj_stem_withoutdict(word):      
 import io
 import re
 suffixes ={  1: ["ો", "ી" ," ે", "ા" , "ૂ", "ે" , "ૢ", "ૄ" ,"ૈ" , "ૌ"  ,"ુ","્","ઈ","એ","ઇ"],
   2: ["ઓએ","ીઓ" ,"ીએ","ોએ" ,"ાઓ","ાઈ","ાઇ","થી","ના","ની","ને","નો" ,"નુ","મા","મી","મુ","શે" ,"ીશ","શો","મત","ઓ","એ" ,"ું","ંુ","ાં","ંા","ંૂ", "ૂં",
"તો","તી","તા","યા","યુજે","ાય","યો","કે","જો","જી","ેલ","વા","વી"] ,
            3: ["ાઓએ","ઓના", "ઓનુ","ઓમા","ઓનો","ઓની","ઓને","ઓથી","ઓના","નું","નાં","માં","તાં","યું","યાં","તું","મું","વાં","ોને" ,"ોની" ,"ાના","ાની" ,"ભરી","ાને",
"ાનો" ,"ોનુ","માન","ીતા", "કાળ","ોથી" ,"દાર", "જનો","ાવે","ાવી","ાવર","વું","ેથી","પણુ","ેલી","ેલા","નાર"],
            4: [ "ીઓની","ઓનું","ઓનાં","ઓમાં","ાઓની" ,"ોઓથી" , "ાઓનો", "ાઓને","ાઓનુ","ોનાં" ,"ોનું" ,"ાનાં", "ાનું", "વાળા","વાળી","પૂ઼ણઁ","વેરા","વાળો","પણું",
"માથી","ાવીશ", "ેલોરી",
"વાથી","વાના","વાનો","વાની","નારી","નારો","ીશુ","ેલાં","ેલું"] , 
            5: ["ાઓનું","માંથી" , "વાનાં","ીશું","પૂર્વક" ,"વામાં","વાનું" ,"વાળું","વવાની","વવાનો","યાનાં"],
   6:[ "વાળાએ","વાળાઓની", "વાળાઓનું","વાળાઓનુ", "વાળાની" , "વાળાનો","વાવાળા","ોમાંથી"  ]
   }


 prefixes =   ["બિન","ગેર","સર્વ", "અર્ધ","શ્રી"]
 replacementlist=    {"ન્યાં" :"ન","ન્યા" :"ન",
"ન્યાના": "ન","ન્યાની":"ન","ન્યાનો":"ન","ન્યા" :"ન",
"ન્યું":"ન", "ન્યુ":"ન", "ન્યો" :"ન", "વ્યાનાં" : "વ", "વ્યાના" : "વ","વ્યાની" : "વ", "વ્યો": "વ",
"વ્યાં" :"વ","વ્યા":"વ", "વ્યાના":"વ", "વ્યાનું":"વ", "વ્યાનુ":"વ",  "વ્યાનો" : "વ",
  "વ્યુ":"વ","વ્યે" :"વ", "પ્યા": "પ",
"પ્યું":"પ", "પ્યુ":"પ", "પ્યો":"પ" , "પ્યાં":"પ", "પ્યા":"પ","પ્યાની": "પ","પ્યાનો": "પ",
"પ્યુ" :"પ","ખ્યાનું":"ખ", "ખ્યાનુ":"ખ","ખ્યા":"ખ", "ખ્યું":"ખ","ખ્યુ":"ખ","ખ્યાં" :"ખ","ખ્યા" :"ખ",
"ખ્યાના":"ખ","ખ્યો":"ખ","ળ્યા":"ળ","ળ્યું" :"ળ","ળ્યુ" :"ળ","ળ્યાં" :"ળ","ળ્યા" :"ળ",
"ળ્યો": "ળ","લ્યાં" : "લ","લ્યા":"લ","લ્યું" :"લ","લ્યુ":"લ","લ્યો":"લ",
"લ્યે": "લ","વવુ":"વ","વવું":"વ","રું":"ર","વવો":"વ"

  }  # Extra similar replacements added to match the words without ending anusvar which are removed in normalizing
 
 while True:#infinite loop ,to continue for currentword only stop when no updation done 
  flag=0
  #print("in process for stemming word - ",word)
  #step1 Check if a number ,then remove the extra word inflection at end 
  number=["૧","૨","૩","૪","૫","૬","૭","૮","૯","0","૦"]
  if word.startswith(tuple(number)): #check is the given word a number? 
    regex = re.compile('[^૧૨૩૪૫૬૭૮૯0૦]')#if yes then remove its non numeric suffix part
    word=regex.sub('',word)
    return (word) #now return back, no other processing needed. 
  
  #step2 check if prefix matches ,then remove it 
  for pref in prefixes:
        if word.startswith(pref) and word>pref:  #check the word is only starting with this and is not entire word
            word=re.sub("^{0}".format(pref),"",word,1)
            flag=1
            break #continue with next step 
  #step3 Check the subsitution rules ,if found match ,replace  it .
            
  for key in replacementlist.keys():
        
        if word.endswith(key) and word>key: #check the word is actually end of string and not directly the string. 
          word=re.sub("{0}".format(key),"{0}".format(replacementlist[key]),word,1)
          flag=1
          return (word) #return back now no need to do more stemming ,else wud get overstemmed
         
      
   #step4 Check the suffix , if found match , remove it.          
  
  
  start=len(word)#start checking from list with as per the extra symbols after 3 in source.
  start=start-2
  if start>6 : #as suffix of length 6 and less , so  we limit the start range from 6 
      start=6
  
  for L in  range(start,0,-1): #
            #print("word and L  and orginal word length is:: ",word,L,len(word))
            
            
         #   print("it entered suffix check of L--",L) 
            for suf in suffixes[L]:
               # print("the suffix considered is ",suf)
                if word.endswith(suf):
                    #print("the word was ending with this suffix*****",suf)
                    possibleword=re.sub("{0}$".format(suf),"",word)
                   # print("trimmed word and its length computed is ",possibleword,len(possibleword))
                    if len(possibleword)>=2: #if trimmed word becomes smaller than 2 size ,it might not be proper stem ,so dont use it 
                        word=possibleword #else use the trimmedword as the stemword
                        #print("new word formed after subsitution is ",word)
                        flag=1 #one replacement done ,maybe till end ..then try for other possible .
                        break
                    
            
  
  if flag==0:
     break
 return (word) #return word and flag as not dictionary word 

def guj_stem_to_lemma(datafile,stemmedlist,lemmalist): #to get back the stem to lemma form in the vocabolory found. 
    import io
    import re
    from indicnlp.tokenize import indic_tokenize
    stemtolemma='lemmatized.csv'
    mycorpora,totalsent=guj_corpus_generate(datafile)   
  
    mappings={}
    with io.open(stemtolemma,'a+',encoding='utf8') as wr: 
     #wr.write("stemmed word , lemmaword(replacement) \n")    
     for lemma in lemmalist: # search is a stemmed version of word in our stemmed list then update the words
      sword=guj_stem_withoutdict(lemma)
      if sword in stemmedlist and sword!=lemma:
       mappings[sword]=lemma
       wr.write("{0},{1}\n".format(sword,lemma))
   
   
    with io.open(datafile,'w+',encoding='utf-8') as w: #store the stemmed sentences back in file
        #divide lines into sentences
     for line in mycorpora:
      alltokens=indic_tokenize.trivial_tokenize_indic(line)#get list of all tokens found from original sentence 
      wordtokens=guj_mytokenizer(line) #fetch only the words in line 
      newline='' #newline to be formed after replacement 
      for basictoken in alltokens:
        if basictoken in wordtokens:
           if basictoken in mappings.keys(): #the basictoken is a word which was trimmed and so in dictionary
               lemmaword=mappings[basictoken]
               newline=newline+lemmaword+" " 
               #newline=re.sub(' '+basictoken+' ',' '+lemmaword+' ',newline)#to ensure only entire word is replaced not if partof word matches
           else:
               newline=newline+basictoken+" "
        else:
            newline=newline+basictoken+" "
      w.write(newline)#write the modified line in result file 
    return(datafile)  
    
def guj_remove_newlines(originalfile,resultfile):
 import io 
 import re
 
 
 with io.open(originalfile,'r+',encoding='utf8') as f:
     lines = f.read() 
 lines=lines.rstrip('\n')
 lines=lines.lstrip('\n')
 lines=lines.replace('\n','')
 with io.open(resultfile,'w+',encoding='utf8') as w:
     w.write(lines)
      
 return(resultfile)  


def guj_corpus_generate(filename):#returns the total lines and all lines in given file
 import io
 #get the individual lines corpora ready 
 corpora=[]
 corpora=guj_sentence_segmenter(filename)
 totalsentences=len(corpora)
 #for s in corpora:
  #  totalsentences=totalsentences+1
 #print("corpus now has sentences --> ",corpora)    
 return (corpora,totalsentences)


def anaphoraresolution(corpora): #take a corpus oflines and resolve the references      
 reference_words=['તે' , 'તેને', 'તેણે',  'તેનો' ,'તેની','તેણે'  ,  'તેનું' ,'તેનુ' , 'તેંનું' , 'તેની' ,'એ','એની','ઍની','એનિ','એણી','ઍનિ',  'એનું' ,'એનુ' ,'ઍનુ' ,'ઍનું' ,'એનૂ' ,'તેમની', 'તેમનિ','તૅમની','તેમને','તેમણે', 'તેમની', 'તેમનો',  'તેમનું' , 'તેમનુ' , 'તેમનૂ' , 'તેમનુઁ' ]


 import pyiwn
 iwn = pyiwn.IndoWordNet(lang=pyiwn.Language.GUJARATI)
 listnounwords=iwn.all_words(pos=pyiwn.PosTag.NOUN)#all words in wordnet ,store in a list 
 ref_count=0
 for line in corpora:
 
  words=guj_mytokenizer(line)
  print(words)
 """
for i, _ in enumerate(corpora[:-1]):
    line1 = corpora[i:i+1]
    line2= corpora[i+1:i+2]
    for word in guj_mytokenizer(line2):
      print(word)
      if word in reference_words:
        ref_count+=1
    print(ref_count) 
    
word="છોકરી"
s=iwn.synsets(word,pos=pyiwn.PosTag.NOUN) #gets only the noun sense words
print(s)

tag=s[0] #gets first word which is generally the original word itself, but not necessarily.
print(tag.pos()) # gets the part of speech of the word

print(tag.lemma_names())    #gets list of all lemma forms of synonyms of the given word
print(tag.gloss()) #gives the explanation of word 

    """
"""
def guj_get_tables_from_website:
# Library for opening url and creating  
# requests 
import urllib.request 
  
# pretty-print python data structures 
from pprint import pprint 
  
# for parsing all the tables present  
# on the website 
from html_table_parser import HTMLTableParser 
  
# for converting the parsed data in a 
# pandas dataframe 
import pandas as pd 
  
  
# Opens a website and read its 
# binary contents (HTTP Response Body) 
def url_get_contents(url): 
  
    # Opens a website and read its 
    # binary contents (HTTP Response Body) 
  
    #making request to the website 
    req = urllib.request.Request(url=url) 
    f = urllib.request.urlopen(req) 
  
    #reading contents of the website 
    return f.read() 
  
# defining the html contents of a URL. 
xhtml = url_get_contents('https://1000mostcommonwords.com/1000-most-common-gujarati-words/').decode('utf-8') 
  
# Defining the HTMLTableParser object 
p = HTMLTableParser() 
  
# feeding the html contents in the 
# HTMLTableParser object 
p.feed(xhtml) 
  
# Now finally obtaining the data of 
# the table required 
pprint(p.tables[0]) 
  
# converting the parsed data to 
# datframe 
print("\n\nPANDAS DATAFRAME\n") 
print(pd.DataFrame(p.tables[0]))
"""