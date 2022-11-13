The source files used to generate syntax trees are taken from : https://github.com/eliranwong/OpenHebrewBible/tree/master/017-BHS-linguistic-annotations

The file `clause-phrase-start-end.csv` is the combined verion of the files `{clause|phrase}_{start|end}.txt`. The files `BHSA-{clause|phrase}-data-cleared.csv` are the cleared version of the files `BHSA-{clause|phrase}-data.csv`. Those three files are used as source data by the script `genSyntax.py` which generates the files `syntax.csv` used by the main verse generator.

The folder `dataviz` contains several exploratory analyses as for the file `BHSA-phrase-data-cleared.csv`.


#### ToDo:
- use dictionaries to replace terms (CP, PP, VP ...)
- order phrases within clause (Object → Verb ...)
- order clauses if subordinated
