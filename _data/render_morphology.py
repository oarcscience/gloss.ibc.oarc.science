# -*-coding: utf-8 -*-
## This script prepares html moirphology snippets for a given language
## Parameters : (1) language ("en", "it" etc)

import pandas as pd
import sys

lang = sys.argv[1]

sets = pd.read_csv("morpho/morpho_sets.csv",sep="\t")
basic_codes = pd.read_csv(f"morpho/basic_codes_{lang}.csv", index_col="full").to_dict()["short"]

x = sets["morphologyDetail"]
x = x.apply(lambda x: [t.strip() for t in x.split(",")]) #split into individual codes, strip
#x = x.apply(lambda l: [o for o in l if o not in [" ", ""] ]) # delete void elements 
x = x.apply(lambda x: list(map(basic_codes.get, x))) # map dictionary conversion onto lists
x = x.apply(" ".join) # concatenate

sets["value"] = x
sets[["key","value"]].to_csv(f"morphocodes_{lang}.csv", index = False)