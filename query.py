import pandas as pd
import numpy as np
import sklearn as sk
import nltk
import streamlit as st
from translate import Translator
trans=Translator(from_lang="hindi", to_lang="English")
from nltk .stem.porter import PorterStemmer
ps = PorterStemmer()

law = pd.read_csv("/Users/jaykataria/Desktop/Data hack/jay/pages/law_words.csv")
df1 = pd.read_csv("/Users/jaykataria/Desktop/Data hack/jay/pages/LawyerInfo.csv")
df2=pd.read_csv("/Users/jaykataria/Desktop/Data hack/jay/PS_2_Test_Dataset.csv")

df=pd.DataFrame()
df["Lawyer Names"]=list(df1["Lawyer Names"])+list(df2["Name"])
df["Information"]=list(df1["Information"])+list(df2["Information"])

def stem(text):
  y=[]

  for i in text.split():
   y.append(ps.stem(i))
  return " ".join(y)

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
cv= CountVectorizer(max_features=5000,stop_words='english')
def recommendCV(query):
    temp = pd.concat([law["words"], pd.Series(query)])
    temp = temp.apply(stem)
    vectors=cv.fit_transform(temp).toarray()
    similarity=cosine_similarity(vectors)
    law_index=-1
    diatance= similarity[law_index]
    names_list=sorted(list(enumerate(similarity[law_index])),reverse=True,key=lambda x:x[1])[1:6]
    li = []
    for i in names_list:
        li.append([law.iloc[i[0]]["cat"], round(i[1]*100)])
    return(li)

from sklearn.feature_extraction.text import TfidfVectorizer
tf=TfidfVectorizer()
def recommendTF(query):
    temp = pd.concat([law["words"], pd.Series(query)])
    temp = temp.apply(stem)
    vectors=tf.fit_transform(temp)
    similarity=cosine_similarity(vectors)
    law_index=-1
    diatance= similarity[law_index]
    names_list=sorted(list(enumerate(similarity[law_index])),reverse=True,key=lambda x:x[1])[1:6]
    li=[]
    for i in names_list:
        li.append([law.iloc[i[0]]["cat"], round(i[1]*100)])
    return(li)

def common_member(a, b):    
    a_set = set(a)
    b_set = set(b)
     
    # check length 
    if len(a_set.intersection(b_set)) > 0:
        return(a_set.intersection(b_set))  
    else:
        return([a[0], b[0]])

def categorize(query):

    rcv = recommendCV(query)
    rtf = recommendTF(query)
    rcv1 = []
    rtf1 = []
    for i in range(5):
        rcv1.append(rcv[i][0])
        rtf1.append(rtf[i][0])

    cat =common_member(rtf1[:3], rcv1[:3])
    return(list(cat))

def recommend(query):
    cat=categorize(query)
    query = " ".join(cat) + " "+query
    df_temp=df
    temp = pd.concat([df_temp["Information"], pd.Series(query)])
    temp = temp.apply(stem)
    vectors=cv.fit_transform(temp).toarray()
    similarity=cosine_similarity(vectors)
    law_index=-1
    diatance= similarity[law_index]
    names_list=sorted(list(enumerate(similarity[-1])),reverse=True,key=lambda x:x[1])[1:-1]
    rno = []
    for i in range(len(names_list)-2):
      rno.append(names_list[i][0])
    return(df_temp.iloc[rno][["Lawyer Names", "Information"]])


st.title("Lawyer Query")
st.markdown("###")
on = st.toggle("Hindi")
st.markdown("###")

query=st.text_input("Enter your query here👇")

if on:
    q=[]
    for x in query.split( ):
        q.append(trans.translate(x))
    query = " ".join(q)

st.dataframe(recommend(query))


