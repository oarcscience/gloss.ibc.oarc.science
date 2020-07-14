import pandas as pd

#################################
# Generate syntactic structures #
#################################

print("Generating syntactic structures...")
cdata = pd.read_csv("BHSA-clause-data-cleared.csv",sep="\t")
pdata = pd.read_csv("BHSA-phrase-data-cleared.csv",sep="\t")
ldata = pd.read_csv("clause-phrase-start-end.csv",sep="\t")
support = pd.read_csv("../byword.csv",sep="\t",usecols=["BHSsort", "WLCverse", "BHS", "gloss", "morphology", "trans1"])

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

trans1=joncture.groupby(["WLCverse","curr","pnum"])["trans1"].apply(" ".join)
print("3...")
ptyp=joncture.groupby(["WLCverse","curr","pnum"])["ptyp"].first()
print("3...")
pfunction=joncture.groupby(["WLCverse","curr","pnum"])["pfunction"].first()
print("4...")
curr=joncture.groupby(["WLCverse","curr"])["ctype"].first()
print("5...")
ckind=joncture.groupby(["WLCverse","curr"])["ckind"].first()
print("6...")
joinedt=pd.DataFrame(trans1).merge(ptyp,left_index=True,right_index=True).merge(pfunction,left_index=True,right_index=True)
joinedt.to_csv("syntax.csv")
pd.DataFrame(curr).to_csv("curr.csv")
pd.DataFrame(ckind).to_csv("ckind.csv")

print("Done.")

