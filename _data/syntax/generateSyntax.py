# -*-coding: utf-8 -*-
## This script generates syntactic structures for a given language
## Parameters : (1) language ("en", "it" etc)

import pandas as pd
import sys
import yaml

lang = sys.argv[1]

print("Generating syntactic structures...")
clause_data = pd.read_csv("BHSA-clause-data-cleared.csv", sep="\t").rename(columns={"cloc": "curr"})
clause_data["curr"] = clause_data["curr"].apply(lambda s: s.split(".")[0])
phrase_data = pd.read_csv("BHSA-phrase-data-cleared.csv", sep="\t")
starts_ends = pd.read_csv("clause-phrase-start-end.csv", sep="\t")
wordgrid = pd.read_csv("../byword.csv", sep="\t", usecols=  ["WLCverse", "trans1"])

wordgrid = wordgrid.merge(starts_ends, left_index = True, right_index = True).merge(phrase_data, how = 'left').merge(clause_data[["num", "curr"]], how = 'left').drop(list(starts_ends.columns), axis = 1)
cols_propag=["pnum", "ptyp", "pfunction", "curr"]
wordgrid[cols_propag]=wordgrid[cols_propag].fillna(method="ffill")
wordgrid["trans1"] = wordgrid["trans1"].fillna("")

with open(f"syntax_terms_{lang}.yaml", "r") as stream:
    try:
        terms = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

phrase_cols = ["ptyp", "pfunction"] # i18n for phrases
for p in phrase_cols:
    wordgrid[p] = wordgrid[p].apply(lambda x: terms[p][x])

byphrase = wordgrid.groupby(["WLCverse","curr","pnum"]).agg({"trans1": " ".join, "ptyp": 'first', "pfunction": 'first'}).reset_index() # gather phrases for each clause
phrase_cols = ["pnum", "ptyp", "pfunction", "trans1"]

def beautify(phon):
	if phon==" ":return "_"
	return phon.replace("ḏ","d").replace("ḡ","g").replace("ṯ","t").replace("ḵ","x").replace("ʔ","ʾ").replace("ʕ","ʿ").replace("ₐ","a").replace("î","ī").replace("ê","ē").replace("ô","ō").replace("û","ū").replace("ᵒ","ŏ").replace("ᵉ","ĕ").replace("ᵃ","ă").replace("ᵊ","ᵉ").replace("ʸ","").replace("ˈ",'<sub id="s">́</sub>').replace("  "," ").replace(" -","-")

byphrase["trans1"] = byphrase["trans1"].apply(beautify)
byphrase["phrase"] = byphrase[phrase_cols].apply(dict, axis = 1)
byphrase = byphrase.drop(phrase_cols, axis = 1)
clause_data["crela"] = clause_data["crela"].fillna("")

byclause = byphrase.groupby(["WLCverse","curr"])["phrase"].apply(list).reset_index().merge(clause_data[["curr", "ckind", "ctype", "crela"]]) # fetch clause info

clause_cols = ['ckind', 'ctype', 'crela'] # i18n for clauses
for c in clause_cols:
    byclause[c] = byclause[c].apply(lambda x: terms[c][x])

clause_cols = ['curr', 'ckind', 'ctype', 'crela', 'phrase'] # gather columns for each verse
byclause["clause"] = byclause[clause_cols].apply(dict, axis = 1)
byclause = byclause.drop(clause_cols, axis = 1)
syntax = byclause.groupby("WLCverse")["clause"].apply(list).reset_index()

syntax.to_csv(f"syntax_{lang}.csv", index=False)
print("Done.")

