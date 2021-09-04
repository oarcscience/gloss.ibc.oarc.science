def hover(x):
    index=x.find(".")
    if index==-1: return x
    else: return x[:index]

def morph(x):
    index=x.find(".")
    if index==-1: return ""
    else: return "+"+x[index+1:]


def stransform(inputw):
    if len(inputw)>0 and inputw[0]=="[":
        return " ʔăḏōnāy"
    elif len(inputw)>1 and inputw[0]==inputw[1]:
        return "-"+inputw[0]+"-"+inputw[1:]
    else:
        return inputw

def septransform(inputw):
    if inputw!="":
        return " "
    else:
        return inputw

def beautify(phon):
	if phon==" ":return "_"
	return phon.replace("ḏ","d").replace("ḡ","g").replace("ṯ","t").replace("ḵ","x").replace("ʔ","ʾ").replace("ʕ","ʿ").replace("ₐ","a").replace("î","ī").replace("ê","ē").replace("ô","ō").replace("û","ū").replace("ᵒ","ŏ").replace("ᵉ","ĕ").replace("ᵃ","ă").replace("ᵊ","ᵉ").replace("ʸ","").replace("ˈ",'<sub id="s">́</sub>').replace("  "," ").replace(" -","-")


def repl(inputw):
    text=beautify(inputw)
    return text

import pandas as pd
print('Loading verses...\r',end="")    
df=pd.read_csv("_data/bible.csv",sep="\t")
## df : hebtext	number	book	chapter	verse	trchapter	trverse	trtext	translit
##      0       1       2       3       4       5           6       7       8

ixv=pd.read_csv("_data/indexv.csv",sep="\t",header=None)
ixv.columns=["previous_verse","previous_book", "previous_chapter", "next_verse", "next_book", "next_chapter"]
## ixv : index file containing navigation. Format
## 1	1	1	2	1534	32
## previous_verse previous_book previous_chapter next_verse next_book next_chapter
## 0              1             2                3          4         5


print('Loading words...\r',end="")    
dfw=pd.read_csv("_data/byword.csv",sep="\t").fillna(" ")
dfwt=dfw["trans1"].apply(stransform)

dfw["wordcat"]=dfwt +dfw["separ"].apply(septransform)
words=dfw.fillna("").groupby("WLCverse")["wordcat"].apply(list).apply("".join).apply(repl)

glosstr0=pd.DataFrame()
collist=["extendedStrongNumber","trans1","morphology","gloss","BSBsort","BSB"]
for col in collist:
    glosstr0[col]=dfw.fillna("").groupby("WLCverse")[col].apply(list)
glosstr0["zip"]=glosstr0.apply(lambda x: zip(*[x[col] for col in collist]),axis=1).apply(list)
template1="""<span id="word"><ol class=word><li lang=he><a href="https://strong.seveleu.com/w/{}" target="_blank">{}</a></li><li title="{}" lang=en_MORPH>{}<span style="font-variant:small-caps;font-size:114%;">{}</span></li><li lang=en_MORPH><sup style="color: lightgray;">{}</sup>{}</li></ol></span>"""
glosstr0["generated"]=glosstr0["zip"].apply(lambda y: "".join([template1.format(strn[1:],beautify(trs1),hover(mor),gl,morph(mor),(lambda x: int(float(x)) if x!=" " else "")(bsbs),bsb) for strn,trs1,mor,gl,bsbs,bsb in  y ]))

joinedt=pd.read_csv("_data/syntax/syntax.csv",index_col=[0,1,2])
curr=pd.read_csv("_data/syntax/curr.csv",index_col=[0,1])["ctype"]
ckind=pd.read_csv("_data/syntax/ckind.csv",index_col=[0,1])["ckind"]

ptyp_dic={"<det>Demonstrative pronoun phrase</det>, <prela>Resumption</prela>":"(det) Demonstrative pronoun phrase; (prela) Resumption", "<det>Demonstrative pronoun phrase</det>":"(det) Demonstrative pronoun phrase", "<det>Nominal phrase</det>, <prela>Predicative adjunct</prela>":"(det) Nominal phrase; (prela) Predicative adjunct", "<det>Nominal phrase</det>, <prela>Resumption</prela>":"(det) Nominal phrase; (prela) Resumption", "<det>Nominal phrase</det>":"(det) Nominal phrase", "<det>Personal pronoun phrase</det>, <prela>Resumption</prela>":"(det) Personal pronoun phrase; (prela) Resumption", "<det>Personal pronoun phrase</det>":"(det) Personal pronoun phrase", "<det>Prepositional phrase</det>, <prela>Predicative adjunct</prela>":"(det) Prepositional phrase; (prela) Predicative adjunct", "<det>Prepositional phrase</det>, <prela>Resumption</prela>":"(det) Prepositional phrase; (prela) Resumption", "<det>Prepositional phrase</det>":"(det) Prepositional phrase", "<det>Proper-noun phrase</det>, <prela>Resumption</prela>":"(det) Proper-noun phrase; (prela) Resumption", "<det>Proper-noun phrase</det>":"(det) Proper-noun phrase", "<undet>Interrogative pronoun phrase</undet>, <prela>Resumption</prela>":"(undet) Interrogative pronoun phrase; (prela) Resumption", "<undet>Interrogative pronoun phrase</undet>":"(undet) Interrogative pronoun phrase", "<undet>Nominal phrase</undet>, <prela>Predicative adjunct</prela>":"(undet) Nominal phrase; (prela) Predicative adjunct", "<undet>Nominal phrase</undet>, <prela>Resumption</prela>":"(undet) Nominal phrase; (prela) Resumption", "<undet>Nominal phrase</undet>":"(undet) Nominal phrase", "<undet>Prepositional phrase</undet>, <prela>Predicative adjunct</prela>":"(undet) Prepositional phrase; (prela) Predicative adjunct", "<undet>Prepositional phrase</undet>":"(undet) Prepositional phrase", "Adjective phrase, <prela>Predicative adjunct</prela>":"Adjective phrase; (prela) Predicative adjunct", "Adjective phrase":"Adjective phrase", "Adverbial phrase, <prela>Resumption</prela>":"Adverbial phrase; (prela) Resumption", "Adverbial phrase":"Adverbial phrase", "Conjunctive phrase, <prela>Resumption</prela>":"Conjunctive phrase; (prela) Resumption", "Conjunctive phrase":"Conjunctive phrase", "Interjectional phrase, <prela>Resumption</prela>":"Interjectional phrase; (prela) Resumption", "Interjectional phrase":"Interjectional phrase", "Interrogative phrase, <prela>Resumption</prela>":"Interrogative phrase; (prela) Resumption", "Interrogative phrase":"Interrogative phrase", "Negative phrase, <prela>Resumption</prela>":"Negative phrase; (prela) Resumption", "Negative phrase":"Negative phrase", "Prepositional phrase, <prela>Resumption</prela>":"Prepositional phrase; (prela) Resumption", "Prepositional phrase":"Prepositional phrase", "Verbal phrase, <prela>Resumption</prela>":"Verbal phrase; (prela) Resumption", "Verbal phrase":"Verbal phrase"}

templatep="""<span style=""><span style="font-family: sans-serif;background: #ffd42a;padding: 9px;">{}</span><span style="font-family: sans-serif;background: #d35f5f;padding: 9px;">{}</span> <span style="/*font-family:sans-serif;font-weight:bold;*/">{}</span></span>"""

def generateqtree(s):
    return templatep.format(s["pfunction"],ptyp_dic[s["ptyp"]],s["trans1"])

print("Generating syntax info...")

phrasesjoinedt=joinedt.apply(generateqtree,axis=1).groupby(["WLCverse","curr"]).apply("\n".join)


templateclause="""<div class=wrapper><p style="font-family: sans-serif;font-size: 125%;">{}: {}</p><p>{}</p></div>"""


def generateqtree2(s):
    return templateclause.format(s["ckind"],s["clausefunction"],s["phrasesjoined"])

print("Generating syntax info 2 ...")



groupedbyverse=pd.DataFrame({'phrasesjoined':phrasesjoinedt , 'clausefunction':curr, 'ckind':ckind }).apply(generateqtree2,axis=1).groupby("WLCverse").apply(" ".join)

print("Done.")
###############################
## End of syntax generation ###
###############################

books=["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "Isaiah", "Jeremiah", "Ezekiel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi", "Psalms", "Proverbs", "Job", "Song of Songs", "Ruth", "Lamentations", "Ecclesiastes", "Esther", "Daniel", "Ezra", "Nehemiah", "1 Chronicles", "2 Chronicles"]


###############################
## Joint table with all info ##
###############################

joinedTable = pd.DataFrame()
joinedTable["book"]       = df["book"].apply(lambda x: books[x-1])
joinedTable["chapter"]    = df["chapter"].apply(str)
joinedTable["verse"]      = df["verse"].apply(str)
joinedTable["trtext"]     = df["trtext"]
joinedTable["previous_book"]     = ixv["previous_book"]
joinedTable["next_book"]     = ixv["next_book"]
joinedTable["previous_chapter"]     = ixv["previous_chapter"]
joinedTable["next_chapter"]     = ixv["next_chapter"]
joinedTable["previous_verse"]     = ixv["previous_verse"]
joinedTable["next_verse"]     = ixv["next_verse"]
joinedTable["hebtext"]     = df["hebtext"]
joinedTable["trchapter"]     = df["trchapter"]
joinedTable["trverse"]     = df["trverse"]
joinedTable["number"]     = df["number"].apply(str)

words.index = joinedTable["book"].index
glosstr0["generated"].index = joinedTable["book"].index
groupedbyverse.index        = joinedTable["book"].index

joinedTable["glossTranslation"]     = glosstr0["generated"]
joinedTable["syntax"]               = groupedbyverse
joinedTable["words"]                = words
df=None
ixv=None
glosstr0=None
groupedbyverse=None



joinedTable["book_no_spaces"]       = joinedTable["book"].apply(lambda x: x.replace(" ",""))
joinedTable["trtext_prepared"]       = joinedTable["trtext"].apply(lambda x: x.replace("LORD", """<span style="font-variant:small-caps;font-size:114%;">lord</span>"""))

filenameTemplate = "v/{}.{}.{}.html"

joinedTable["currentFilename"] = joinedTable[["book_no_spaces", "chapter", "verse"]].apply(lambda x: filenameTemplate.format(x["book_no_spaces"], x["chapter"], x["verse"]) , axis=1)

with open("verseTemplate.html", "r") as fin:
    verseTemplate = fin.read()

joinedTable["currentContent"]  = joinedTable.apply(lambda x: verseTemplate.format(x["book"], x["chapter"], x["verse"], x["trtext"], x["previous_book"], x["book"], x["next_book"], x["previous_chapter"], x["chapter"], x["next_chapter"], x["previous_verse"], x["verse"], x["next_verse"], x["hebtext"], x["book"], x["trchapter"], x["trverse"], x["number"], x["trtext_prepared"], x["words"], x["previous_verse"], x["next_verse"], x["glossTranslation"], x["previous_verse"], x["next_verse"], x["syntax"], x["previous_verse"], x["next_verse"]), axis=1)

redirectTemplate = """<html><head><meta http-equiv="refresh" content="0; URL=/v/{}.{}.{}.html"></head></html>"""

redirectFilenameTemplate = "v/{}.html"

joinedTable["currentRedirectionFilename"] = joinedTable["number"].apply(redirectFilenameTemplate.format)

joinedTable["currentRedirectionContent"] = joinedTable[["book_no_spaces", "chapter", "verse"]].apply(lambda x: redirectTemplate.format(x["book_no_spaces"], x["chapter"], x["verse"]), axis=1)

###############################
## Joint table constructed   ##
###############################


###############################
## File generation           ##
###############################

def writeToFile(dfline):
    with open(dfline["currentFilename"], 'w+') as fout1:
        fout1.write(dfline["currentContent"])
    with open(dfline["currentRedirectionFilename"], 'w+') as fout2:
        fout2.write(dfline["currentRedirectionContent"])

print("Generating files : ")


joinedTable[["currentFilename", "currentContent", "currentRedirectionFilename", "currentRedirectionContent"]].apply(writeToFile, axis=1)

print("Done.")


