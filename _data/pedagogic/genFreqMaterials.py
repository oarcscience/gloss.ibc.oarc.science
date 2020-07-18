import pandas as pd

df=pd.read_csv("FrequentLemmas.csv",sep="\t")

template="{}. {} — {} (Strong {})"
applyTemplate = lambda x: template.format(x["internalOrd"], x["hebLemma"], x["transLemma"], x["StrongNo"])

df["text"]=df.apply(applyTemplate, axis=1)
df_gr1=pd.DataFrame(df.groupby(["subheader","header","headerNumber"])["text"].apply("\n".join))
template1="### {}\n\n{}\n"
df_gr1["text_1"]=df_gr1.apply(lambda x: template1.format(x.name[0], x["text"]), axis=1)
df_gr2=pd.DataFrame(df_gr1.groupby(["headerNumber","header"])["text_1"].apply("\n".join))
template2="## {}\n\n{}\n"
df_gr2["text_2"]=df_gr2.apply(lambda x: template2.format(x.name[1], x["text_1"]), axis=1)

with open("generated.md","w+") as fin:
    fin.write("\n".join(df_gr2["text_2"]))
