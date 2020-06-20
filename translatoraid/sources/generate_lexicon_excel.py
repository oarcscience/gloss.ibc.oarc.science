#!/usr/bin/env python
# coding: utf-8

# prepares the excel file used to translate the lexicon

import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
byword=pd.read_csv("../../_data/byword.csv",sep="\t")
ixv=pd.read_csv("idx.csv",sep="\t")
books=["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "Isaiah", "Jeremiah", "Ezekiel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi", "Psalms", "Proverbs", "Job", "Song of Songs", "Ruth", "Lamentations", "Ecclesiastes", "Esther", "Daniel", "Ezra", "Nehemiah", "1 Chronicles", "2 Chronicles"]
booksdf=pd.DataFrame({"bookname":books,"booknumber":range(1,40)})
byword=byword.merge(ixv,left_on="WLCverse",right_on="number").merge(booksdf,left_on="book",right_on="booknumber")
byword["count"]=byword["morphology"]
lexemedf=byword.groupby("lexemeID").agg({"bookname":set,"extendedStrongNumber":min,"trans1":lambda x:x.value_counts().index[0],"morphology":lambda x:x.value_counts().index[0],"count":"count","gloss":min})
lexemedf=lexemedf.rename(columns={"bookname":"bookslist"})
lexemedf["engGloss"]=lexemedf["gloss"]
mlb = MultiLabelBinarizer()
lexemedf = lexemedf.join(pd.DataFrame(mlb.fit_transform(lexemedf.pop('bookslist')),
                          columns=mlb.classes_,
                          index=lexemedf.index))
lexemedf.to_excel("eng.EHglosses.xls")

