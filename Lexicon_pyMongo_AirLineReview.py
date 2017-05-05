import pandas as pd
import csv
# Import NTLK package 
from nltk import sent_tokenize,word_tokenize

# ### **Lexicon-based Approach**

positive=[]
negative=[]
keys_to_ignore = ['Entry','Source','Defined']

with open('general_inquirer_dict.txt') as fin:
    reader = csv.DictReader(fin,delimiter='\t')
    for i,line in enumerate(reader):
        if line['Negativ']=='Negativ':
            if line['Entry'].find('#')==-1:
                negative.append(line['Entry'].lower())
            if line['Entry'].find('#')!=-1: #In General Inquirer, some words have multiple senses. Combine all tags for all senses.
                negative.append(line['Entry'].lower()[:line['Entry'].index('#')]) 
        if line['Positiv']=='Positiv':
            if line['Entry'].find('#')==-1:
                positive.append(line['Entry'].lower())
            if line['Entry'].find('#')!=-1: #In General Inquirer, some words have multiple senses. Combine all tags for all senses.
                positive.append(line['Entry'].lower()[:line['Entry'].index('#')])

fin.close()

# Store positive words and negative words from the dictionary in two lists
pvocabulary=sorted(list(set(positive))) 
nvocabulary=sorted(list(set(negative))) 

# Data Import till 2300 rows
review=pd.read_csv('C:/MSIS/UnStructuredData/reviewsTest.csv')

# See data columns
review['poswdcnt']=0
review['negwdcnt']=0
review['lsentiment']=0
review_index=0


# Tokenize the words from the review documents to a word list
def getWordList(text,word_proc=lambda x:x):
    word_list=[]
    for sent in sent_tokenize(text):
        for word in word_tokenize(sent):
            word_list.append(word)
    return word_list
    

# The lists are used for storing the # of positive words, the # of negative words, 
# and the overall sentiment level for all the documents
# The length of each list is equal to the total number of review document
pcount_list=[]
ncount_list=[]
lsenti_list=[]

# Iterate all review documents
# For each word, look it up in the positive word list and the negative word list
# If found in any list, update the corresponding counts 
for text in review['reviewcontent']:
    vocabulary=getWordList(text,lambda x:x.lower())
    
    pcount=0
    ncount=0
    for pword in pvocabulary:
        pcount += vocabulary.count(pword)
    for nword in nvocabulary:
        ncount += vocabulary.count(nword)
    
    pcount_list.append(pcount)
    ncount_list.append(ncount)
    lsenti_list.append(pcount-ncount)    
    
    
    review_index += 1
    


# Storing word counts and overall sentiment into the dataframe
# So that we know the # of positive words, # of negative words, and sentiment
# for each review document
#create test and train data

review['poswdcnt']=pd.Series(pcount_list)
review['negwdcnt']=pd.Series(ncount_list)
review['lsentiment']=pd.Series(lsenti_list)
#creating training set and test set
train = review[:2000] 
test = review[2000:] 

review.to_csv('C:/MSIS/UnStructuredData/demo_data_review_airline_out.csv')

#Run a logistic regression
import statsmodels.api as sm2

#predicted test recommendation
col= ['lsentiment']
train = train.fillna(0)
train[col]
logit=sm2.Logit(train['recommended'],train[col])
result=logit.fit() 
print(result.summary())
pre = result.predict(test[col])

pre = (pre > 0.75).astype(int)

print("Confusion Matrix")

from sklearn.metrics import confusion_matrix

print(confusion_matrix(test['recommended'],pre))





        
        
    
    
    
    





















