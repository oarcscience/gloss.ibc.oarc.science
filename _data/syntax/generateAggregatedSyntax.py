import pandas as pd

print('Read 3 syntax files...\r',end="")    
joinedt=pd.read_csv("syntax.csv",index_col=[0,1,2])
# WLCverse,curr,pnum,trans1,ptyp,pfunction
# 1,c1,p1,bᵊ rēšîˈṯ,<undet>Prepositional phrase</undet>,Time reference
# 1,c1,p2,bārāˈ,Verbal phrase,Predicate

curr=pd.read_csv("curr.csv",index_col=[0,1])["ctype"]
# WLCverse,curr,ctype
# 1,c1,x-qatal-X clause
# 2,c2,We-X-qatal clause

ckind=pd.read_csv("ckind.csv",index_col=[0,1])["ckind"]
# WLCverse,curr,ckind
# 1,c1,Verbal clauses
# 2,c2,Verbal clauses

print('Done.\r',end="")    
ptyp_dic={"<det>Demonstrative pronoun phrase</det>, <prela>Resumption</prela>":"(det) Demonstrative pronoun phrase; (prela) Resumption", "<det>Demonstrative pronoun phrase</det>":"(det) Demonstrative pronoun phrase", "<det>Nominal phrase</det>, <prela>Predicative adjunct</prela>":"(det) Nominal phrase; (prela) Predicative adjunct", "<det>Nominal phrase</det>, <prela>Resumption</prela>":"(det) Nominal phrase; (prela) Resumption", "<det>Nominal phrase</det>":"(det) Nominal phrase", "<det>Personal pronoun phrase</det>, <prela>Resumption</prela>":"(det) Personal pronoun phrase; (prela) Resumption", "<det>Personal pronoun phrase</det>":"(det) Personal pronoun phrase", "<det>Prepositional phrase</det>, <prela>Predicative adjunct</prela>":"(det) Prepositional phrase; (prela) Predicative adjunct", "<det>Prepositional phrase</det>, <prela>Resumption</prela>":"(det) Prepositional phrase; (prela) Resumption", "<det>Prepositional phrase</det>":"(det) Prepositional phrase", "<det>Proper-noun phrase</det>, <prela>Resumption</prela>":"(det) Proper-noun phrase; (prela) Resumption", "<det>Proper-noun phrase</det>":"(det) Proper-noun phrase", "<undet>Interrogative pronoun phrase</undet>, <prela>Resumption</prela>":"(undet) Interrogative pronoun phrase; (prela) Resumption", "<undet>Interrogative pronoun phrase</undet>":"(undet) Interrogative pronoun phrase", "<undet>Nominal phrase</undet>, <prela>Predicative adjunct</prela>":"(undet) Nominal phrase; (prela) Predicative adjunct", "<undet>Nominal phrase</undet>, <prela>Resumption</prela>":"(undet) Nominal phrase; (prela) Resumption", "<undet>Nominal phrase</undet>":"(undet) Nominal phrase", "<undet>Prepositional phrase</undet>, <prela>Predicative adjunct</prela>":"(undet) Prepositional phrase; (prela) Predicative adjunct", "<undet>Prepositional phrase</undet>":"(undet) Prepositional phrase", "Adjective phrase, <prela>Predicative adjunct</prela>":"Adjective phrase; (prela) Predicative adjunct", "Adjective phrase":"Adjective phrase", "Adverbial phrase, <prela>Resumption</prela>":"Adverbial phrase; (prela) Resumption", "Adverbial phrase":"Adverbial phrase", "Conjunctive phrase, <prela>Resumption</prela>":"Conjunctive phrase; (prela) Resumption", "Conjunctive phrase":"Conjunctive phrase", "Interjectional phrase, <prela>Resumption</prela>":"Interjectional phrase; (prela) Resumption", "Interjectional phrase":"Interjectional phrase", "Interrogative phrase, <prela>Resumption</prela>":"Interrogative phrase; (prela) Resumption", "Interrogative phrase":"Interrogative phrase", "Negative phrase, <prela>Resumption</prela>":"Negative phrase; (prela) Resumption", "Negative phrase":"Negative phrase", "Prepositional phrase, <prela>Resumption</prela>":"Prepositional phrase; (prela) Resumption", "Prepositional phrase":"Prepositional phrase", "Verbal phrase, <prela>Resumption</prela>":"Verbal phrase; (prela) Resumption", "Verbal phrase":"Verbal phrase"}

templatep="""<span style=""><span style="font-family: sans-serif;background: #ffd42a;padding: 9px;">{}</span><span style="font-family: sans-serif;background: #d35f5f;padding: 9px;">{}</span> <span style="/*font-family:sans-serif;font-weight:bold;*/">{}</span></span>"""

generateqtree = lambda s: templatep.format(s["pfunction"],s["ptyp"],s["trans1"])

print("Generating syntax info...")

joinedt["ptyp"]=joinedt["ptyp"].apply(ptyp_dic.get)
phrasesjoinedt=joinedt.apply(generateqtree,axis=1).groupby(["WLCverse","curr"]).apply("\n".join)

templateclause="""<div class=wrapper><p style="font-family: sans-serif;font-size: 125%;">{}: {}</p><p>{}</p></div>"""

generateqtree2 = lambda s: templateclause.format(s["ckind"],s["clausefunction"],s["phrasesjoined"])

print("Generating syntax info 2 ...")

groupedbyverse=pd.DataFrame({'phrasesjoined':phrasesjoinedt , 'clausefunction':curr, 'ckind':ckind }).apply(generateqtree2, axis=1).groupby("WLCverse").apply(" ".join)

groupedbyverse=pd.DataFrame(groupedbyverse)
groupedbyverse.columns=["aggregatedSyntax"]
groupedbyverse.to_csv("aggregatedSyntax.csv")
