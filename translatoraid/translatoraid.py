## This script generates the gloss translation support files in /translatoraid/

def beautify(phon):
	if phon=="  ":return "_"
	return phon.replace("ḏ","d").replace("ḡ","g").replace("ṯ","t").replace("ḵ","x").replace("ʔ","ʾ").replace("ʕ","ʿ").replace("ₐ","a").replace("î","ī").replace("ê","ē").replace("ô","ō").replace("û","ū").replace("ᵒ","ŏ").replace("ᵉ","ĕ").replace("ᵃ","ă").replace("ᵊ","ᵉ").replace("ʸ","").replace("ˈ",'<sub id="s">́</sub>').replace("  "," ").replace(" -","-")


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
"""+"""<li><span style="font-size:100%;">{}</span></li>"""+"""
<li><span style="font-size:80%;color=gray;"><a href="/w/{}">{}</a></span></li>
</ol>
</span>"""


applyglosstemplate = lambda x: glosstemplate.format(beautify(x[0]),x[1],x[2],x[3],x[4])

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
stringend="""</article>
<span class="print-footer"> - Seveleu-Dubrovnik's copy of the BH sources. <a href="https://seveleu.com/pages/bh-resource">About</a> | <a href="https://www.mechon-mamre.org/p/pt/ptmp3prq.htm" target="_blank">Listen audio.</a></span>

<footer><hr class="slender"><div class="credits"><span><svg xmlns="https://www.w3.org/2000/svg"   width="15px" height="15px" viewBox="0 0 980 980"><circle cx="490" cy="490" r="440" fill="none" stroke="#000" stroke-width="100"/><path d="M219,428H350a150,150 0 1 1 0,125H219a275,275 0 1 0 0-125z"/></svg> 2020 Seveleu-Dubrovnik's copy of the BH sources. <a href="https://seveleu.com/pages/bh-resource" target="_blank">About</a> | <a href="https://www.mechon-mamre.org/p/pt/ptmp3prq.htm" target="_blank">Listen audio</a> | <a title="GitHub" href="https://github.com/wlcling/wlcling.github.io" target="_blank"><svg height="17" class="octicon octicon-mark-github" viewBox="0 0 16 16" version="1.1" width="24" aria-hidden="true"><path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg></a> </div></footer>

</body></html>""" 
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
   
    with open(books[b].replace(" ","")+".html","w+") as fout:
        fout.write(groupedbybook.iloc[b])

print("Generating gloss translation file...")

fullGlossTr = pd.concat([ixv["book"], ixv["chapter"], ixv["verse"],  ixv["number"],  glosstr0["lexiconfetched"].apply(" ".join), separator["one"].apply(lambda x: x if x!=" " else "")],  axis=1)

stingrecurr="""{} {}:{} ({}) {} {}"""

verseformat = lambda x: stingrecurr.format(books[x["book"]-1], x["chapter"], x["verse"], x["number"], x["lexiconfetched"], x["one"])
fullGlossTr["generatedtext"]=fullGlossTr.apply(verseformat, axis=1)

groupedbybook=fullGlossTr.groupby("book")["generatedtext"].apply("\n".join)


for b  in range(len(books)):
    print("Book ",b,"\r",end="")    
   
    with open("Trans"+books[b]+".txt","w+") as fout:
        fout.write(groupedbybook.iloc[b])




print("Done.")
