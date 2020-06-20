def hover(x):
    index=x.find(".")
    if index==-1: return x
    else: return x[:index]

def morph(x):
    index=x.find(".")
    if index==-1: return ""
    else: return x[index+1:]


def stransform(inputw):
    if len(inputw)>0 and inputw[0]=="[":
        return " ʔăḏōnāy"
    elif len(inputw)>1 and inputw[0]==inputw[1]:
        return "-"+inputw[0]+"-"+inputw[1:]
    else:
        return inputw

def septransform(inputw):
    if inputw=="":
        return ""
    if inputw=="־":
        return ""
    if inputw==" ":
        return " "
    if inputw=="׃ ":
        return ""
    else:
        return """<span style="font-size: 157%;padding:15px;background: blueviolet;">{}</span>""".format(inputw)

def beautify(phon):
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
dfw["trans1"]=dfw["trans1"].apply(beautify)


#dfw["wordcat"]=dfwt +dfw["separ"].apply(septransform)
#words=dfw.fillna("").groupby("WLCverse")["wordcat"].apply(list).apply("".join).apply(repl)

glosstr0=pd.DataFrame()
collist=["lexemeID","trans1","morphology"]
for col in collist:
    glosstr0[col]=dfw.fillna("").groupby("WLCverse")[col].apply(list)


#with open("sources/words.csv", "w") as text_file:
#    text_file.write("\n".join(words))

glosstr0[collist].to_csv("sources/glosstr0.csv",index=False,quotechar=" ")


