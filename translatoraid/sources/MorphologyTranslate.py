#!/usr/bin/env python
# coding: utf-8

def deletenull(l):
    return [o if o!="" for o in l]

import pandas as pd
master = pd.read_csv("mlexiconmaster.csv",sep="\t")
dictio = pd.read_csv("morpholex.csv",index_col="full").to_dict()["short"]
splitcomma  = lambda x: [t.strip() for t in x.split(",")]
applydictio = lambda x: list(map(dictio.get, x))
master["value"]=master["morphologyDetail"].apply(splitcomma).apply(deletenull).apply(applydictio).apply(", ".join)
master[["key","value"]].to_csv("mlexicon.csv",index=False)
