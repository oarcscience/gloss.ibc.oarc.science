# -*-coding: utf-8 -*-
## This script generates verses and redirections in the folder passed as a parameter
## Parameters : (1) deploy folder (2) language subfolder (3) verse limit for debug

import yaml
import pandas as pd
import sys

# Read config
with open("_config.yml", "r") as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

deployfolder = sys.argv[1]
lang = sys.argv[2]
nrows = int(sys.argv[3]) ## Decimate table for faster deploy in development

books = config["booknames"][lang]

df = pd.read_csv("_data/bible_he.csv", sep="\t", nrows = nrows, usecols = ["hebtext", "number", "book", "chapter", "verse", "mm_chapter", "audio_start", "audio_stop"], dtype = {"chapter": str, "verse": str, "number": str})
df["trtext"] = pd.read_csv(f"_data/bible_{lang}.csv", sep="\t", nrows = nrows, usecols = ["trtext"])["trtext"]
df["book"] = df["book"].apply(lambda x: books[x-1])
df["book_no_spaces"] = df["book"].apply(lambda x: x.replace(" ",""))

ixv = pd.read_csv("_data/indexv.csv", sep="\t", nrows = nrows) # navigation
gloss_translation = pd.read_csv(f"_data/gloss_translation_{lang}.csv", nrows = nrows, usecols = ['zip']) # gloss translation
gloss_translation["zip"] = gloss_translation["zip"].apply(eval)

link_template = "//lex.ibc.oarc.science/{}/w".format(lang)
gloss_template="""<span id="wd"><ol class="wd"><li lang="he"><a href="{link_template}/{strong}">{phonemes}</a></li><li lang="{lang}">{gloss}</li><li lang="{lang}"><span class="mA">{morpho}</span></li></ol></span>"""

gloss_translation["glossTranslation"] = gloss_translation["zip"].apply(lambda y: "".join([gloss_template.format(
    link_template = link_template,
    strong = strong[1:],
    phonemes = phonemes,
    morpho = morpho,
    gloss = gloss,
    lang = lang,
    ) for strong, phonemes, morpho, gloss in  y ]))


phonemes = pd.read_csv("_data/phonemes.csv", nrows = nrows, usecols = ['wordcat']).rename(columns={'wordcat': 'words'}) # gloss translation

syntax = pd.read_csv(f"_data/syntax/syntax_{lang}.csv", nrows = nrows, usecols = ["clause"]).rename(columns={"clause": "syntax"}) #syntax
syntax["syntax"] = syntax["syntax"].apply(eval)

from templateVerse import format_syntax, template_lines
syntax["rendered"] = syntax["syntax"].apply(format_syntax)

lines_to_dict = lambda syntax: { phrase["pnum"]: clause["curr"]  for clause in syntax for phrase in clause["phrase"]}
syntax["drawlines"] = syntax["syntax"].apply(lines_to_dict) # extract verse syntax tree lines

draw_lines_template = lambda dic: "\n".join(
    [
        template_lines.format(from_ = p, to = dic[p]) + "\n" + \
        template_lines.format(from_ = "text"+p, to = p) \
        for p in dic.keys()
    ])

syntax["drawlines"] = syntax["drawlines"].apply(draw_lines_template)

## Combine all the info in one table
df = pd.concat([df, ixv, gloss_translation, phonemes, syntax], axis = 1)

filenameTemplate = f"{deployfolder}/{lang}/{{}}.{{}}.{{}}.html"
df["currentFilename"] = df.apply(lambda x: filenameTemplate.format(x["book_no_spaces"], x["chapter"], x["verse"]) , axis=1)


## Generate files from templates
from templateVerse import templateVerse, templateRedirect
from templateFooter import templateFooter

### Generate and html for every verse
df["currentContent"]  = df.apply(lambda x: templateVerse.format(
    footer = templateFooter.format(config["navigreminder"][lang]),
    lang = lang,
    sitename = config["sitename"][lang],
    sitesubname =  config["sitesubname"][lang],
    book = x["book"],
    chapter = x["chapter"],
    glossTranslation = x["glossTranslation"],
    hebtext = x["hebtext"],
    next_book = x["next_book"],
    next_chapter = x["next_chapter"],
    next_verse = x["next_verse"],
    number = x["number"],
    previous_book = x["previous_book"],
    previous_chapter = x["previous_chapter"],
    previous_verse = x["previous_verse"],
    syntax = x["rendered"],
    drawlines = x["drawlines"],
    trtext = x["trtext"],
    trtext_prepared = x["trtext"].replace("LORD", '<span class="lord">lord</span>'),
    verse = x["verse"],
    words = x["words"],
    mm_chapter = x["mm_chapter"],
    audio_start = x["audio_start"],
    audio_stop = x["audio_stop"],
    backword = config["words"]["back"][lang],
    forthword = config["words"]["forth"][lang],
    gloss_header = config["words"]["gloss_header"][lang],
    syntax_header = config["words"]["syntax_header"][lang]
    ), axis=1)

### Generate redirect file for each verse
redirectFilenameTemplate = f"{deployfolder}/{lang}/{{}}.html"
df["currentRedirectionFilename"] = df["number"].apply(redirectFilenameTemplate.format)
df["currentRedirectionContent"] = df.apply(lambda x: templateRedirect.format(
    lang,
    x["book_no_spaces"],
    x["chapter"],
    x["verse"]
    ), axis=1)


## Generate files from df
def writeToFile(dfline):
    with open(dfline["currentFilename"], 'w+') as fout1:
        fout1.write(dfline["currentContent"])
    with open(dfline["currentRedirectionFilename"], 'w+') as fout2:
        fout2.write(dfline["currentRedirectionContent"])

# Generate files
df[["currentFilename", "currentContent", "currentRedirectionFilename", "currentRedirectionContent"]].apply(writeToFile, axis=1)
