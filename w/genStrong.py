## This script generates dictionary entries in the folder w/

def list_notnull(l):
    if "" in l: l.remove("")
    return l


def lang_full(x):
    if x=="H": return "Hebrew"
    if x=="A": return "Aramaic"

def stn(x):
    if x=="":return ""
    else: return str(int(float(x)))

import pandas as pd
print('Loading verses...\r',end="")    
df=pd.read_csv("../_data/TBESH_formatted.csv",sep="\t").fillna("")

print('Loading indexing information...\r',end="")    
index=pd.read_csv("../_data/temp.csv",sep="\t")

def plur_linear(s):
    lis=s.split("|")
    if len(lis)==1: return s
    return " ".join(["""<sup style="color:gray;">{}</sup>""".format(str(i))+word for i,word in zip(range(1,len(lis)+1),lis)])
        
def plur_vertical(s):
    lis=s.split("|")
    if len(lis)==1: return s
    return "<br>".join(["""<strong>{}</strong> """.format(chr(ord('A')-1+i))+word for i,word in zip(range(1,len(lis)+1),lis)])


def wrapper(line, arg):
    if arg=="":return ""
    else: return line.format(arg)

def wrapper2(line, arg1, arg2):
    if arg2=="":return ""
    else: return line.format(arg1, arg2)

def nav_next(ind):
    if ind==8674: return 9000
    if ind==9012: return 1
    return ind+1

def nav_prev(ind):
    if ind==9000: return 8674
    if ind==1: return 9012
    return ind-1

books=["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "Isaiah", "Jeremiah", "Ezekiel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi", "Psalms", "Proverbs", "Job", "Song of Songs", "Ruth", "Lamentations", "Ecclesiastes", "Esther", "Daniel", "Ezra", "Nehemiah", "1 Chronicles", "2 Chronicles"]

def force_to_int(value):
    """Given a value, returns the value as an int if possible.
    Otherwise returns None.
    """
    try:
        return int(value)
    except ValueError:
        return -1

def intell_links(arg):
#    print(arg)
    local_index=pd.DataFrame({"entry":list(map(force_to_int, arg))}).merge(index,left_on="entry",right_on="number").dropna(axis=0)
    if local_index.shape[0]==0: return ""
    local_index["textlink"]=local_index.apply(lambda x: """<span id="toc"><span style="color:darkgray;"> </span><a class="shadow" href="/v/{}.html">{}:{}</a></span>""".format(x["entry"],x["chapter"],x["verse"]), axis=1)
    local_index_by_book=pd.DataFrame({"textlink":local_index.groupby("book")["textlink"].apply(", ".join)}).reset_index()
    local_index_by_book["bookname"]=local_index_by_book["book"]
#    print ("----------------------------")
#    print (local_index_by_book)
    local_index_by_book["bookname"]=local_index_by_book["book"].apply(lambda x: """<span id="toc" style="font-family:sans-serif;">{}</span>""".format(books[int(x-1)]))
    local_index_by_book["booklinks"]=local_index_by_book["bookname"]+local_index_by_book["textlink"]
    return " ".join(local_index_by_book["booklinks"])




for i  in range(df.shape[0]):
    if i%100==0:
        print('Generating verses: {:.0%}'.format(i/df.shape[0]),"\r",end="")    
    with open(str(int(df.iloc[i,0][1:]))+".html","w+") as fout:
        fout.write("""<!DOCTYPE html>
<head>
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" type="image/png" href="/assets/img/favicon.png"/>

<title>Strong's lexeme """+df.iloc[i,0][1:]+""" — Westminster Leningrad Codex for Linguists</title>
<meta name="description" content=""""+df.iloc[i,7]+"""">

<!-- Google Fonts loaded here depending on setting in _data/options.yml true loads font, blank does not-->
<link href='//fonts.googleapis.com/css?family=Lato:400,400italic&amp;subset=cyrillic,latin-ext' rel='stylesheet' type='text/css'>
<link href='//fonts.googleapis.com/css?family=EB+Garamond:400,400italic&amp;subset=cyrillic,latin-ext' rel='stylesheet' type='text/css'>


<link rel="stylesheet" type="text/css" href="/css/tufte.css">
<link rel="stylesheet" type="text/css" href="/css/print.css" media="print">

<!---  <link rel="canonical" href="https://bh.seveleu.com/16"> ---->

  <link rel="alternate" type="application/rss+xml" title="Belarusian Arabic script" href="https://bh.seveleu.com/feed.xml" /><style>#s{font-size:132%;color:cadetblue;font-style: italic;}</style>
</head>

<body>
<header>
<nav class="group"><a href="/">
<h3>Biblical Hebrew for linguists</h3><h4>Westminster Leningrad Codex</h4></a></nav>
</header>

<p style="text-align:center;display:flow-root;"><a class="shadow" style="float:left;" href="/w/"""+str(nav_prev(int(df.iloc[i,0][1:])))+".html"+""" ">&laquo; Back</a>
<a class="shadow" style="float:right;" href="/w/""" +str(nav_next(int(df.iloc[i,0][1:])))+".html" +""" ">Forth &raquo;</a></p>



<article class="group">
<p style="margin: 0px;background-color: #ffd42a;padding: 5px;width:33%;"></p>
<p style="margin: 0px;background-color: #ff7f2a;padding: 5px;width:38%;"></p>
<p style="margin: 0px;background-color: #7296cc;padding: 5px;width:27%;"></p>

"""+"""<h1>{} <span id="bh" dir="rtl">{}</span> ‘{}’ <span style="color: rgba(0, 0, 0, 0.75);font-size: 65%; font-family: EB Garamond;font-weight: normal;">({})</span></h1>""".format(df.iloc[i,22], df.iloc[i,2], plur_linear(df.iloc[i,20]), lang_full(df.iloc[i,3]))+"""
<p><span style="color: rgba(0, 0, 0, 0.75)">Etymology:</span> {}""".format(df.iloc[i,15])+wrapper(""" | <span style="color: rgba(0, 0, 0, 0.75)">Roots:</span> {} """, wrapper2("""
<a class="shadow" href="/w/{}"><span id="bh">{}</span></a>""", stn(df.iloc[i,8] ), df.iloc[i,9])+wrapper2("""
<a class="shadow" href="/w/{}"><span id="bh">{}</span></a>""", stn(df.iloc[i,10]), df.iloc[i,11])+wrapper2("""
<a class="shadow" href="/w/{}"><span id="bh">{}</span></a>""", stn(df.iloc[i,12]), df.iloc[i,13]))+wrapper("""
 | In another language: {}  
""", wrapper("""<strong><span id="bh">{}</span></strong> """, df.iloc[i,6]))+wrapper("""({})""", stn(df.iloc[i,7]))+wrapper(""" | <span style="color: rgba(0, 0, 0, 0.75)">Variants:</span> {}
""", df.iloc[i,18])+wrapper(""" | <span style="color: rgba(0, 0, 0, 0.75)">Morphology:</span> {} """, plur_linear(df.iloc[i,19]))+wrapper("""</p><p>{}</p>
""", plur_vertical(df.iloc[i,21]))+"""

</article>

<p style="text-align:center;display:flow-root;"><a class="shadow" style="float:left;" href="/w/"""+str(nav_prev(int(df.iloc[i,0][1:])))+".html"+""" ">&laquo; Back</a>
<a class="shadow" style="float:right;" href="/w/""" +str(nav_next(int(df.iloc[i,0][1:])))+".html" +""" ">Forth &raquo;</a></p>

<div style="display: flex;"><p style="margin-bottom:27px;"><span id="toc" style="font-family:sans-serif;">Mentioned in </span>"""+intell_links(sorted(list_notnull(df.iloc[i,17].split(",")),key=lambda x: float(x)))+ """
</p></div>


<span class="print-footer"> - Seveleu-Dubrovnik's copy of the BH sources. <a href="https://seveleu.com/pages/bh-resource">About</a> | <a href="https://www.mechon-mamre.org/p/pt/ptmp3prq.htm" target="_blank">Listen audio.</a></span>

<footer><hr class="slender"><div class="credits"><span><svg xmlns="https://www.w3.org/2000/svg"   width="15px" height="15px" viewBox="0 0 980 980"><circle cx="490" cy="490" r="440" fill="none" stroke="#000" stroke-width="100"/><path d="M219,428H350a150,150 0 1 1 0,125H219a275,275 0 1 0 0-125z"/></svg> 2020 Seveleu-Dubrovnik's copy of the BH sources. <a href="https://seveleu.com/pages/bh-resource" target="_blank">About</a> | <a href="https://www.mechon-mamre.org/p/pt/ptmp3prq.htm" target="_blank">Listen audio</a> | <a title="GitHub" href="https://github.com/wlcling/wlcling.github.io" target="_blank"><svg height="17" class="octicon octicon-mark-github" viewBox="0 0 16 16" version="1.1" width="24" aria-hidden="true"><path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg></a> </div></footer>

</body></html>"""  )


df=df.sort_values(by=[df.columns[0]], axis=0)

with open("../lexicon.html","w+") as fout:
    fout.write("""<!DOCTYPE html>
<head>
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" type="image/png" href="/assets/img/favicon.png"/>

<title>Westminster Leningrad Codex for Linguists</title>
<meta name="description" content="Biblical Hebrew samples for linguists. Strong's lexicon">

<!-- Google Fonts loaded here depending on setting in _data/options.yml true loads font, blank does not-->
<link href='//fonts.googleapis.com/css?family=Lato:400,400italic&amp;subset=cyrillic,latin-ext' rel='stylesheet' type='text/css'>
<link href='//fonts.googleapis.com/css?family=EB+Garamond:400,400italic&amp;subset=cyrillic,latin-ext' rel='stylesheet' type='text/css'>


<link rel="stylesheet" type="text/css" href="/css/tufte.css">
<link rel="stylesheet" type="text/css" href="/css/print.css" media="print">

<!---  <link rel="canonical" href="https://bh.seveleu.com/16"> ---->

  <link rel="alternate" type="application/rss+xml" title="Belarusian Arabic script" href="https://bh.seveleu.com/feed.xml" /><style>span#toc{padding: 9px;padding-left: 0px;display:inline-block;}</style>
</head>

<body>
<header>
<nav class="group"><a href="">
<h3>Biblical Hebrew for linguists</h3><h4>Strong's Lexicon</h4></a></nav>
</header>

<article class="group">
<p style="margin: 0px;background-color: #ffd42a;padding: 5px;width:33%;"></p>
<p style="margin: 0px;background-color: #ff7f2a;padding: 5px;width:38%;"></p>
<p style="margin: 0px;background-color: #7296cc;padding: 5px;width:27%;"></p>


<div style="display: flex;"><p style="margin-bottom:27px;"><span id="toc" style="font-family:sans-serif;">Lexemes</span>""" + "".join(
["""<span id="toc"><span style="color:darkgray;">"""+str(int(df.iloc[i,0][1:]))+"""</span><a class="shadow" href="/w/"""+str(int(df.iloc[i,0][1:]))+""".html">""" +df.iloc[i,22]+""" <span id="bh">"""+df.iloc[i,2]+"</span></a></span>" for i in range(df.shape[0]) ])+ """
</p></div>
 
</article>

<span class="print-footer"> - Seveleu-Dubrovnik's copy of the BH sources. <a href="https://seveleu.com/pages/bh-resource">About</a> | <a href="https://www.mechon-mamre.org/p/pt/ptmp3prq.htm" target="_blank">Listen audio.</a></span>

<footer><hr class="slender"><div class="credits"><span><svg xmlns="https://www.w3.org/2000/svg"   width="15px" height="15px" viewBox="0 0 980 980"><circle cx="490" cy="490" r="440" fill="none" stroke="#000" stroke-width="100"/><path d="M219,428H350a150,150 0 1 1 0,125H219a275,275 0 1 0 0-125z"/></svg> 2020 Seveleu-Dubrovnik's copy of the BH sources. <a href="https://seveleu.com/pages/bh-resource" target="_blank">About</a> | <a href="https://www.mechon-mamre.org/p/pt/ptmp3prq.htm" target="_blank">Listen audio</a>  | <a title="GitHub" href="https://github.com/wlcling/wlcling.github.io" target="_blank"><svg height="17" class="octicon octicon-mark-github" viewBox="0 0 16 16" version="1.1" width="24" aria-hidden="true"><path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg></a></div></footer>

</body></html>""" )
