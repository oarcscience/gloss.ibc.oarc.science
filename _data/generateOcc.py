import pandas as pd                                                     

dfw=pd.read_csv("Desktop/sdfbsd/wlcling.github.io/_data/byword.csv",sep="\t").fillna(" ")                                                       
dfw["W2"]=dfw["WLCverse"].apply(str)                                                                                                                                                    
newf=dfw[["W2","extendedStrongNumber"]].groupby("extendedStrongNumber")["W2"].apply(",".join)                                                                                           
newf2=newf.apply(lambda x: ",".join(list(set(x.split(",")))))                                                                                                                           
newf2.to_csv("/home/maxwell/Desktop/sfbsDB.txt",sep="\t")                                                                                                                               

