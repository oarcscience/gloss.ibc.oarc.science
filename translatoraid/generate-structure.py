import pandas as pd

ixv=pd.read_csv("sources/idx.csv",sep="\t")
separator=pd.read_csv("sources/lastssepar.csv",header=None,names=["one"],sep="\t",skip_blank_lines=False)
joinedtable = pd.concat([ixv["book"], ixv["chapter"], ixv["verse"],  ixv["number"],  separator["one"].apply(lambda x: x if x!=" " else "")],axis=1)

books=["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "Isaiah", "Jeremiah", "Ezekiel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi", "Psalms", "Proverbs", "Job", "Song of Songs", "Ruth", "Lamentations", "Ecclesiastes", "Esther", "Daniel", "Ezra", "Nehemiah", "1 Chronicles", "2 Chronicles"]



stingrecurr="""{}:{} ({}) {}"""

verseformat = lambda x: stingrecurr.format(x["chapter"], x["verse"], x["number"], x["one"])
joinedtable["generatedtext"]=joinedtable.apply(verseformat, axis=1)


groupedbybook=joinedtable.groupby("book")["generatedtext"].apply("\n".join)


for b  in range(len(books)):
    print("Book ",b,"\r",end="")    
   
    with open("Trans"+books[b]+".txt","w+") as fout:
        fout.write(groupedbybook.iloc[b])




