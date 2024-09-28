import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


df=pd.read_csv(r"D:\ex.csv")
df.dropna(inplace=True)
df=df.drop_duplicates()
l=[]
for i in df['User-Rating']:
    l.append(i[:3])
df['User-Rating']=l
df['Album/Movie']=df['Album/Movie'].str.replace(" ","")
df['Singer/Artists']=df['Singer/Artists'].str.replace(" ","")

def list_music():
    x=df['Song-Name']
    q=[]
    for i in x:
        q.append(i)
    return q
        
df['tags']=df['Singer/Artists']+' '+df['Genre']+' '+df['Album/Movie']+' '+df['User-Rating']
new_df=df[['Song-Name','tags']]
new_df['tags']=new_df['tags'].apply(lambda x:x.lower())
new_df['tags']=new_df['tags'].str.replace(","," ")
cv=CountVectorizer(max_features=2000)
vectors=cv.fit_transform(new_df['tags']).toarray()
similarity=cosine_similarity(vectors)
sorted(list(enumerate(similarity[0])),reverse=True,key=lambda x:x[1])
new_df.rename(columns={'Song-Name':'title'},inplace=True)
def recommend(music):
    music_index=new_df[new_df['title']==music].index[0]
    distances=similarity[music_index]
    music_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:11]
    m_l=[]
    for i in music_list:
        a=new_df.iloc[i[0]].title
        m_l.append(a)
    return m_l
        
