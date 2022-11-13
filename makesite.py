import yaml
import os

# Read config
with open("_config.yml", "r") as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# Create folder structure
folders_to_create = ["", "/en", "/css", "/fonts", "/assets/img", "/assets/js"]
for folder in folders_to_create:
    if not os.path.exists(config["deployfolder"] + folder):
        # Create a new directory because it does not exist
        os.makedirs(config["deployfolder"] + folder)


# Generate index
os.system("python {} {} {}".format("generateIndex.py", config["deployfolder"], "en"))


# Generate morphology lexicon
os.system("cd _data/ ; python {} {} ; cd ..".format("render_morphology.py", "en"))
# Prepare gloss translation files
os.system("cd _data/ ; python {} {} ; cd ..".format("from_words.py", "en"))
# Prepare gloss translation files
os.system("cd _data/syntax/ ; python {} {} ; cd ../..".format("generateSyntax.py", "en"))

# Generate verses
os.system("python {} {} {} {}".format("generateVerses.py", config["deployfolder"], "en", config["verselimit"]))

# Copy assets
os.system("cp -t _site/css/ css/*.css")
os.system("cp -t _site/fonts/ fonts/SILEOT.ttf")
os.system("cp -t _site/assets/img/ assets/img/flower.svg assets/img/horse.svg assets/img/favicon.png")
os.system("cp -t _site/assets/js/ assets/js/treelines.js")
os.system("cp -t _site/ index.html")