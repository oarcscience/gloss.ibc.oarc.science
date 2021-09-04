## generates the file _data/indexv.csv to produce the navigation links


import pandas as pd
df=pd.read_csv("_data/bible.csv",sep="\t")


verseprev=[0]
versenext=[df.shape[0]-1]
chaptprev=[0]
chaptnext=[df.shape[0]-1]
boookprev=[0]
boooknext=[df.shape[0]-1]



lastbook=0
lastchapter=0
lastverse=0
for i  in range(1,df.shape[0]):
    if i%100==0:
        print('Indexing verses: {:.0%}'.format(i/2/df.shape[0]),"\r",end="")    
    chaptprev+=[lastchapter]
    boookprev+=[lastbook]
    verseprev+=[lastverse]
    if df.iloc[i,2]!=df.iloc[i-1,2]:
        lastbook=i
    if df.iloc[i,3]!=df.iloc[i-1,3]:
        lastchapter=i
    if df.iloc[i,4]!=df.iloc[i-1,4]:
        lastverse=i

nextbook=df.shape[0]-1
nextchapter=df.shape[0]-1
nextverse=df.shape[0]-1
for i  in range(df.shape[0]-2,-1,-1):
    if i%100==0:
        print('Indexing verses: {:.0%}'.format(1-i/2/df.shape[0]),"\r",end="")    
    if df.iloc[i,2]!=df.iloc[i+1,2]:
        nextbook=i+1
    if df.iloc[i,3]!=df.iloc[i+1,3]:
        nextchapter=i+1
    if df.iloc[i,4]!=df.iloc[i+1,4]:
        nextverse=i+1
    chaptnext=[nextchapter]+chaptnext
    boooknext=[nextbook]+boooknext
    versenext=[nextverse]+versenext

with open("_data/indexv.csv","w+") as fout:
    fout.write("\n".join(["{}	{}	{}	{}	{}	{}".format(verseprev[i]+1,boookprev[i]+1,chaptprev[i]+1,versenext[i]+1,boooknext[i]+1,chaptnext[i]+1) for i in range(23213)]))

