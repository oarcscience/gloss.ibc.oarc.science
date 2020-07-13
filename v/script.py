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
df=pd.read_csv("../_data/bible.csv",sep="\t")
ixv=pd.read_csv("../_data/indexv.csv",sep="\t",header=None)


print('Loading words...\r',end="")    
dfw=pd.read_csv("../_data/byword.csv",sep="\t").fillna(" ")
dfwt=dfw["trans1"].apply(stransform)

dfw["wordcat"]=dfwt +dfw["separ"].apply(septransform)
words=dfw.fillna("").groupby("WLCverse")["wordcat"].apply(list).apply("".join).apply(repl)

glosstr0=pd.DataFrame()
collist=["extendedStrongNumber","trans1","morphology","gloss","BSBsort","BSB"]
for col in collist:
    glosstr0[col]=dfw.fillna("").groupby("WLCverse")[col].apply(list)
glosstr0["zip"]=glosstr0.apply(lambda x: zip(*[x[col] for col in collist]),axis=1).apply(list)
template1="""<span id="word"><ol class=word><li lang=he><a href="/w/{}" target="_blank">{}</a></li><li title="{}" lang=en_MORPH>{}<span style="font-variant:small-caps;font-size:114%;">{}</span></li><li lang=en_MORPH><sup style="color: lightgray;">{}</sup>{}</li></ol></span>"""
glosstr0["generated"]=glosstr0["zip"].apply(lambda y: "".join([template1.format(strn[1:],beautify(trs1),hover(mor),gl,morph(mor),(lambda x: int(float(x)) if x!=" " else "")(bsbs),bsb) for strn,trs1,mor,gl,bsbs,bsb in  y ]))

#################################
# Generate syntactic structures #
#################################

print("Generating syntactic structures...")
cdata = pd.read_csv("../_data/syntax/BHSA-clause-data-cleared.csv",sep="\t")
pdata = pd.read_csv("../_data/syntax/BHSA-phrase-data-cleared.csv",sep="\t")
ldata = pd.read_csv("../_data/syntax/clause-phrase-start-end.csv",sep="\t")
support = pd.read_csv("../_data/byword.csv",sep="\t",usecols=["BHSsort", "WLCverse", "BHS", "gloss", "morphology", "trans1"])

print("1...")
joncture=support.merge(ldata,left_index=True, right_index=True).merge(pdata,how='left').merge(cdata,how='left')
cols_propag=["pnum", "ptyp", "pfunction", "cloc", "cstruct", "ckind", "ctype", "crela"]
joncture[cols_propag]=joncture[cols_propag].fillna(method="ffill")
cols_void=["trans1"]
joncture[cols_void]=joncture[cols_void].fillna("")

def dotsplit(s):
    if not "." in  s: return [s,""];
    else: return s.split(".")

print("2...")

joncture["curr"]=joncture["cloc"].apply(dotsplit).apply(lambda x: x[0])
joncture["prev"]=joncture["cloc"].apply(dotsplit).apply(lambda x: x[1])
joncture["level"]=joncture["cstruct"].apply(len)
cdic=dict(zip(joncture["curr"], joncture["level"]))
cdic[""]=0
joncture["prevlevel"]=joncture["prev"].apply(lambda x: cdic[x])

print("3...")

words=joncture.groupby(["WLCverse","curr","pnum"])["trans1"].apply(" ".join)
print("3...")
ptyp=joncture.groupby(["WLCverse","curr","pnum"])["ptyp"].first()
print("3...")
pfunction=joncture.groupby(["WLCverse","curr","pnum"])["pfunction"].first()
print("4...")
curr=joncture.groupby(["WLCverse","curr"])["ctype"].first()
print("5...")
ckind=joncture.groupby(["WLCverse","curr"])["ckind"].first()
print("6...")
joinedt=pd.DataFrame(words).merge(ptyp,left_index=True,right_index=True).merge(pfunction,left_index=True,right_index=True)
print("7...")

ptyp_dic={"<det>Demonstrative pronoun phrase</det>, <prela>Resumption</prela>":"(det) Demonstrative pronoun phrase; (prela) Resumption", "<det>Demonstrative pronoun phrase</det>":"(det) Demonstrative pronoun phrase", "<det>Nominal phrase</det>, <prela>Predicative adjunct</prela>":"(det) Nominal phrase; (prela) Predicative adjunct", "<det>Nominal phrase</det>, <prela>Resumption</prela>":"(det) Nominal phrase; (prela) Resumption", "<det>Nominal phrase</det>":"(det) Nominal phrase", "<det>Personal pronoun phrase</det>, <prela>Resumption</prela>":"(det) Personal pronoun phrase; (prela) Resumption", "<det>Personal pronoun phrase</det>":"(det) Personal pronoun phrase", "<det>Prepositional phrase</det>, <prela>Predicative adjunct</prela>":"(det) Prepositional phrase; (prela) Predicative adjunct", "<det>Prepositional phrase</det>, <prela>Resumption</prela>":"(det) Prepositional phrase; (prela) Resumption", "<det>Prepositional phrase</det>":"(det) Prepositional phrase", "<det>Proper-noun phrase</det>, <prela>Resumption</prela>":"(det) Proper-noun phrase; (prela) Resumption", "<det>Proper-noun phrase</det>":"(det) Proper-noun phrase", "<undet>Interrogative pronoun phrase</undet>, <prela>Resumption</prela>":"(undet) Interrogative pronoun phrase; (prela) Resumption", "<undet>Interrogative pronoun phrase</undet>":"(undet) Interrogative pronoun phrase", "<undet>Nominal phrase</undet>, <prela>Predicative adjunct</prela>":"(undet) Nominal phrase; (prela) Predicative adjunct", "<undet>Nominal phrase</undet>, <prela>Resumption</prela>":"(undet) Nominal phrase; (prela) Resumption", "<undet>Nominal phrase</undet>":"(undet) Nominal phrase", "<undet>Prepositional phrase</undet>, <prela>Predicative adjunct</prela>":"(undet) Prepositional phrase; (prela) Predicative adjunct", "<undet>Prepositional phrase</undet>":"(undet) Prepositional phrase", "Adjective phrase, <prela>Predicative adjunct</prela>":"Adjective phrase; (prela) Predicative adjunct", "Adjective phrase":"Adjective phrase", "Adverbial phrase, <prela>Resumption</prela>":"Adverbial phrase; (prela) Resumption", "Adverbial phrase":"Adverbial phrase", "Conjunctive phrase, <prela>Resumption</prela>":"Conjunctive phrase; (prela) Resumption", "Conjunctive phrase":"Conjunctive phrase", "Interjectional phrase, <prela>Resumption</prela>":"Interjectional phrase; (prela) Resumption", "Interjectional phrase":"Interjectional phrase", "Interrogative phrase, <prela>Resumption</prela>":"Interrogative phrase; (prela) Resumption", "Interrogative phrase":"Interrogative phrase", "Negative phrase, <prela>Resumption</prela>":"Negative phrase; (prela) Resumption", "Negative phrase":"Negative phrase", "Prepositional phrase, <prela>Resumption</prela>":"Prepositional phrase; (prela) Resumption", "Prepositional phrase":"Prepositional phrase", "Verbal phrase, <prela>Resumption</prela>":"Verbal phrase; (prela) Resumption", "Verbal phrase":"Verbal phrase"}

templatep="""<span id="word"><ol class=word><li lang=he><a href="/w/" target="_blank">{}</a></li><li title="" lang=en_MORPH>{}<span style="font-variant:small-caps;font-size:114%;"></span></li><li lang=en_MORPH><sup style="color: lightgray;"></sup>{}</li></ol></span>"""

def generateqtree(s):
    return templatep.format(ptyp_dic[s["ptyp"]],s["pfunction"],s["trans1"])

phrasesjoinedt=joinedt.apply(generateqtree,axis=1).groupby(["WLCverse","curr"]).apply(" ".join)

print("8...")
templatec="""<div class=wrapper><h4 style="text-align:center;">{}</h4><h5 style="text-align:center;">{}</h5><ol class=sentence>{}</ol></div>"""


def generateqtree2(s):
    return templatec.format(s["ckind"],s["clausefunction"],s["phrasesjoined"])

groupedbyverse=pd.DataFrame({'phrasesjoined':phrasesjoinedt , 'clausefunction':curr, 'ckind':ckind }).apply(generateqtree2,axis=1).groupby("WLCverse").apply(" ".join)

print("9...")
###############################
## End of syntax generation ###
###############################

print("Done.")

books=["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "Isaiah", "Jeremiah", "Ezekiel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi", "Psalms", "Proverbs", "Job", "Song of Songs", "Ruth", "Lamentations", "Ecclesiastes", "Esther", "Daniel", "Ezra", "Nehemiah", "1 Chronicles", "2 Chronicles"]


for i  in range(df.shape[0]):
    if i%100==0:
        print('Generating verses: {:.0%}'.format(i/df.shape[0]),"\r",end="")    
   
    with open(books[df.iloc[i,2]-1].replace(" ","")+"."+str(df.iloc[i,3])+"."+str(df.iloc[i,4])+".html","w+") as fout:
        fout.write("""<!DOCTYPE html>
<head>
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" type="image/png" href="/assets/img/favicon.png"/>

<title>{} {}:{} — Biblical Hebrew for Linguists</title>
<meta name="description" content="{}">

<!-- Google Fonts loaded here depending on setting in _data/options.yml true loads font, blank does not-->
<link href='//fonts.googleapis.com/css?family=Lato:400,400italic&amp;subset=cyrillic,latin-ext' rel='stylesheet' type='text/css'>
<link href='//fonts.googleapis.com/css?family=EB+Garamond:400,400italic&amp;subset=cyrillic,latin-ext' rel='stylesheet' type='text/css'>

<link rel="stylesheet" type="text/css" href="/css/tufte.css">
<link rel="stylesheet" type="text/css" href="/css/print.css" media="print">

  <link rel="alternate" type="application/rss+xml" title="Biblical Hebrew for Linguists" href="https://bh.seveleu.com/feed.xml" /><style>#s{{font-size:132%;color:cadetblue;font-style: italic;}}</style>
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.8/jquery.min.js"></script>
<script type="text/javascript">
document.onkeydown = function(evt) {{
    evt = evt || window.event;
    switch (evt.keyCode) {{
        case 37:
            window.location = $('#prev').attr('href');
            break;
        case 39:
            window.location = $('#next').attr('href');
            break;
    }}
}};
</script>
</head>

<body>
<header>
<nav class="group"><a href="/">
<h3>Biblical Hebrew for linguists</h3><h4>Westminster Leningrad Codex</h4></a></nav>
</header>

<article class="group">
<p style="margin: 0px;background-color: #ffd42a;padding: 5px;width:33%;"></p>
<p style="margin: 0px;background-color: #ff7f2a;padding: 5px;width:38%;"></p>
<p style="margin: 0px;background-color: #7296cc;padding: 5px;width:27%;"></p>

<div style="display: flex;"><p style="font-size:100%"><span style="float: left;"><a class="shadow" href="/v/{}.html">&laquo;</a>  {} <a class="shadow" href="/v/{}.html">&raquo;</a></span>  <span style="float: right;"><a class="shadow" href="/v/{}.html">&laquo;</a>  {} <a class="shadow" href="/v/{}.html">&raquo;</a> : <a class="shadow" href="/v/{}.html">&laquo;</a>  {} <a class="shadow" href="/v/{}.html">&raquo;</a>  </span></p></div>

<p id="bh" dir="rtl">{}</p>

<p><span class="marginnote"><a href="https://biblehub.com/bsb/" target="_blank"><i>BSB</i></a> {} {}:{}. <span style="color:white;">Debug: verse number {}</span></span>{}</p>
  
<p id="tr">/{}/</p>


<p style="text-align:center"><a class="shadow" id="prev" style="float:left;" href="/v/{}.html">&laquo; Back</a>
<a class="shadow" id="next" style="float:right;" href="/v/{}.html">Forth &raquo;</a></p>

<h3 style="text-align:center;">Gloss translation</h3>

<div class=wrapper>
    <ol class=sentence>{}</ol></div>

<p style="text-align:center"><a class="shadow" style="float:left;" href="/v/{}.html">&laquo; Back</a>
<a class="shadow" style="float:right;" href="/v/{}.html">Forth &raquo;</a></p>

<h3 style="text-align:center;">Syntactic structures</h3>

{}


<p style="text-align:center"><a class="shadow" style="float:left;" href="/v/{}.html">&laquo; Back</a>
<a class="shadow" style="float:right;" href="/v/{}.html">Forth &raquo;</a></p>



</div>



 
</article>

<span class="print-footer"> - Seveleu-Dubrovnik's copy of the BH sources. <a href="https://seveleu.com/pages/bh-resource">About</a> | <a href="https://www.mechon-mamre.org/p/pt/ptmp3prq.htm" target="_blank">Listen audio.</a></span>

<footer><hr class="slender"><div class="credits"><span><svg xmlns="https://www.w3.org/2000/svg"   width="15px" height="15px" viewBox="0 0 980 980"><circle cx="490" cy="490" r="440" fill="none" stroke="#000" stroke-width="100"/><path d="M219,428H350a150,150 0 1 1 0,125H219a275,275 0 1 0 0-125z"/></svg> 2020 Seveleu-Dubrovnik's copy of the BH sources. <a href="https://seveleu.com/pages/bh-resource" target="_blank">About</a> | <a href="https://www.mechon-mamre.org/p/pt/ptmp3prq.htm" target="_blank">Listen audio</a> | <a title="GitHub" href="https://github.com/wlcling/wlcling.github.io" target="_blank"><svg height="17" class="octicon octicon-mark-github" viewBox="0 0 16 16" version="1.1" width="24" aria-hidden="true"><path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg></a><br>To navigate back- and forwards, use the arrow keys <span class="shadow">←</span> and <span class="shadow">→</span> on your keyboard</div></footer>

</body></html>""".format(books[df.iloc[i,2]-1], df.iloc[i,3], df.iloc[i,4], df.iloc[i,7], ixv.iloc[i,1], books[df.iloc[i,2]-1], ixv.iloc[i,4], ixv.iloc[i,2], df.iloc[i,3], ixv.iloc[i,5], ixv.iloc[i,0], df.iloc[i,4], ixv.iloc[i,3], df.iloc[i,0], books[df.iloc[i,2]-1], df.iloc[i,5], df.iloc[i,6], df.iloc[i,1], df.iloc[i,7].replace("LORD", """<span style="font-variant:small-caps;font-size:114%;">lord</span>"""), words[df.iloc[i,1]], ixv.iloc[i,0], ixv.iloc[i,3], glosstr0.iloc[i,7], ixv.iloc[i,0], ixv.iloc[i,3], groupedbyverse.iloc[i], ixv.iloc[i,0], ixv.iloc[i,3] ) )

#1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5 ))

    with open(str(df.iloc[i,1])+".html","w+") as fout2:
        fout2.write("""<html><head><meta http-equiv="refresh" content="0; URL=/v/"""+books[df.iloc[i,2]-1].replace(" ","")+"."+str(df.iloc[i,3])+"."+str(df.iloc[i,4])+""".html"></head></html>""")

print(" ".join(list(set("".join(list(dfwt))))))



