# -*-coding: utf-8 -*-
## This script generates gloss translation dictionaries by verbs for a given language
## Parameters : (1) language ("en", "it" etc)

import pandas as pd
import sys

byword = pd.read_csv("byword.csv",sep="\t", usecols = ["extendedStrongNumber","trans1","morphocode", "separ", "WLCverse"]).fillna(" ")

lang = sys.argv[1]

language_gloss = pd.read_csv(f"byword_{lang}.csv",sep="\t", usecols = ["gloss"]).fillna(" ")

byword = pd.concat([byword, language_gloss], axis = 1)

def stransform(inputw):
    if inputw.startswith("["):
        return " ʔăḏōnāy"
    elif len(inputw)>1 and inputw[0]==inputw[1]:
        return "-"+inputw[0]+"-"+inputw[1:]
    else:
        return inputw
byword["trans1"] = byword["trans1"].apply(stransform)

# Rendering morphology
morphocodes = pd.read_csv(f"morphocodes_{lang}.csv")
morpho_dict = dict(zip(morphocodes["key"], morphocodes["value"]))
byword["morphocode"] = byword["morphocode"].apply(morpho_dict.get)

print('septransforming words...\r',end="")    
byword["wordcat"]=byword["trans1"] +byword["separ"].apply(lambda x: " " if x!="" else x)
print('Groupbying words...\r',end="")    

def beautify(phon):
	if phon==" ":return "_"
	return phon.replace("ḏ","d").replace("ḡ","g").replace("ṯ","t").replace("ḵ","x").replace("ʔ","ʾ").replace("ʕ","ʿ").replace("ₐ","a").replace("î","ī").replace("ê","ē").replace("ô","ō").replace("û","ū").replace("ᵒ","ŏ").replace("ᵉ","ĕ").replace("ᵃ","ă").replace("ᵊ","ᵉ").replace("ʸ","").replace("ˈ",'<sub id="s">́</sub>').replace("  "," ").replace(" -","-")

words=byword.fillna("").groupby("WLCverse")["wordcat"].apply(list).apply("".join).apply(beautify)
words.to_csv("phonemes.csv", index = None)

print('Preparing gloss translations...\r',end="")    
glosstr0=pd.DataFrame()
collist=["extendedStrongNumber","trans1","morphocode","gloss"]
print('FillNa ...\r',end="")    
byword["trans1"] = byword["trans1"].apply(beautify)
for col in collist:
    glosstr0[col] = byword.fillna("").groupby("WLCverse")[col].apply(list)
glosstr0
print('Apply list...\r',end="")

glosstr0["zip"]=glosstr0.apply(lambda x: zip(*[x[col] for col in collist]),axis=1).apply(list)
glosstr0["zip"].to_csv(f"gloss_translation_{lang}.csv", index = None)