## This script generates the gloss translation support files in /translatoraid/

import pandas as pd

print(1)
heb=pd.read_csv("sources/heb.csv",sep="\t")
print(2)
ixv=pd.read_csv("sources/idx.csv",sep="\t")
print(3)
separator=pd.read_csv("sources/lastssepar.csv",header=None,names=["one"],sep="\t",skip_blank_lines=False)
print(separator["one"].isna().sum(), ", ",separator.shape[0])
print(4)
#l1=pd.read_csv("sources/lexicon.csv")
l1=pd.read_excel("sources/EHglosses.xls",usecols=["lexemeID","gloss","extendedStrongNumber"])
l1.columns=["key","H","value"]
l1["H"]=l1["H"].apply(lambda x: x[1:]) # deletes the first letter "H"
print(5)
lexicon=dict(zip(l1["key"],l1["value"]))
EtoH   =dict(zip(l1["key"],l1["H"]))
print(6)
m1=pd.read_csv("sources/mlexicon.csv")
print(7)
mdic=dict(zip(m1["key"],m1["value"]))
print(8)
glosstr0=pd.read_csv("sources/glosstr0-1.csv",sep="\t")
for col in glosstr0.columns:
    glosstr0[col]=glosstr0[col].str.split("¤")



print(9)

glosstr0["lexiconfetched"]=glosstr0["lexemeID"].apply(lambda x: map(lexicon.get, x)).apply(list)
print(10)


glosstr0["morphologyfetched"]=glosstr0["morphology"].apply(lambda x: map(mdic.get, x)).apply(list)
glosstr0["H"]=glosstr0["lexemeID"].apply(lambda x: map(EtoH.get, x)).apply(list)
		
glosstemplate="""<span id="word">
<ol class="word">
<li lang="he" style="color:darkblue">{}</li>
<li lang="en_MORPH">{}</li>
"""+"""<li><span style="font-variant:small-caps;font-size:100%;">{}</span></li>"""*0+"""
"""+"""<li><span style="font-style:italic;font-size:100%;">{}</span></li>"""+"""
<li><span style="font-size:80%;color=gray;"><a href="/w/{}">{}</a></span></li>
</ol>
</span>"""


applyglosstemplate = lambda x: glosstemplate.format(x[0],x[1],x[2],x[3],x[4])

glosstrans = lambda x : "\n".join(map(applyglosstemplate, list(zip(x["trans1"], x["lexiconfetched"], x["morphologyfetched"], x["H"], x["lexemeID"]))))

print(11)


glosstr0["glosstrans"]=glosstr0.apply(glosstrans,axis=1)
print(12)


separatortemplate="""<span style="padding: 8px;background-color:yellow;font-size: 155%;">{}</span>"""

glosstr0["trans1"]=glosstr0["trans1"].apply(" ".join) + separator["one"].apply(lambda x: separatortemplate.format(x) if x!=" " else "")

joinedtable = pd.concat([ixv["book"], ixv["chapter"], ixv["verse"],  ixv["number"],  glosstr0["trans1"] , heb["hebtext"] , glosstr0["glosstrans"]], axis=1)
print(13)

books=["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "Isaiah", "Jeremiah", "Ezekiel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi", "Psalms", "Proverbs", "Job", "Song of Songs", "Ruth", "Lamentations", "Ecclesiastes", "Esther", "Daniel", "Ezra", "Nehemiah", "1 Chronicles", "2 Chronicles"]

print(14)

stringbegin="""<!DOCTYPE html>
<head>
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" type="image/png" href="/assets/img/favicon.png"/>

<title>Westminster Leningrad Codex for Linguists</title>
<!-- Google Fonts loaded here depending on setting in _data/options.yml true loads font, blank does not-->
<link href='//fonts.googleapis.com/css?family=Lato:400,400italic&amp;subset=cyrillic,latin-ext' rel='stylesheet' type='text/css'>
<link href='//fonts.googleapis.com/css?family=EB+Garamond:400,400italic&amp;subset=cyrillic,latin-ext' rel='stylesheet' type='text/css'>

<link rel="stylesheet" type="text/css" href="../css/tufte.css">
<link rel="stylesheet" type="text/css" href="../css/print.css" media="print">

  <link rel="alternate" type="application/rss+xml" title="Belarusian Arabic script" href="https://bh.seveleu.com/feed.xml" /><style>#s{{font-size:132%;color:cadetblue;font-style: italic;}}</style>
<style>
@font-face {
    font-family: "Ezra SIL";
    src: url("/home/maxwell/Desktop/sdfbsd/wlcling.github.io/fonts/SILEOT.ttf");
}
</style>
</head>

<body>
<header>
<nav class="group"><a href="/translatoraid/index.html">
<h3>Biblical Hebrew for linguists</h3><h4>Westminster Leningrad Codex</h4></a></nav>
<h2>Preparatory materials for the Belarusian tranlation</h2>
<h2>Падрыхоўчыя матэрыялы для беларускага перакладу</h2>
<h3>Interlinear translations</h3>
<h3>Глосныя пераклады</h3>
</header>
<article class="group">
"""
print(15)

stingrecurr="""
<div class=wrapper><p id="tr"><stong>{}:{} ({})</strong> /{}/</p>
<p id="bh" dir="rtl">{}</p><ol class=sentence>{}</ol></div>

"""
print(16)
stringend="""</article></body></html>""" 
print(17)
verseformat = lambda x: stingrecurr.format(x["chapter"], x["verse"], x["number"], x["trans1"], x["hebtext"], x["glosstrans"])
print(18)

joinedtable["generatedtext"]=joinedtable.apply(verseformat, axis=1)
print(19)
bookformat = lambda x: stringbegin + x + stringend
print(20)
groupedbybook=joinedtable.groupby("book")["generatedtext"].apply("\n".join).apply(bookformat)
print(21)

for b  in range(len(books)):
    print("Book ",b,"\r",end="")    
   
    with open(books[b]+".html","w+") as fout:
        fout.write(groupedbybook.iloc[b])




