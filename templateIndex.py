templateIndex = """<!DOCTYPE html lang="{lang}">
<head>
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" type="image/png" href="/assets/img/favicon.png"/>

<title>Westminster Leningrad Codex for Linguists</title>
<meta name="description" content="{largedescription}">

<!-- Google Fonts loaded here depending on setting in _data/options.yml true loads font, blank does not-->
<link href='//fonts.googleapis.com/css?family=Lato:400,400italic&amp;subset=cyrillic,latin-ext' rel='stylesheet' type='text/css'>
<link href='//fonts.googleapis.com/css?family=EB+Garamond:400,400italic&amp;subset=cyrillic,latin-ext' rel='stylesheet' type='text/css'>


<link rel="stylesheet" type="text/css" href="/css/tufte.css">
<link rel="stylesheet" type="text/css" href="/css/print.css" media="print">

</head>

<body>
<header>
<nav class="group"><a href="">
<h3>{sitename}</h3><h4>{sitesubname}</h4></a></nav>
</header>

<article class="group">
<p style="margin: 0px;background-color: #ffd42a;padding: 5px;width:33%;"></p>

<div style="display: flex;"><p style="margin-bottom:27px;"><span id="toc" style="font-family:sans-serif;">{heading_part1}</span>{links1}
</p></div>

<p style="margin: 0px;background-color: #ff7f2a;padding: 5px;width:38%;"></p>

<div style="display: flex;"><p style="margin-bottom:27px;"><span id="toc" style="font-family:sans-serif;">{heading_part2}</span>{links2}
</p></div>

<p style="margin: 0px;background-color: #7296cc;padding: 5px;width:27%;"></p>


<div style="display: flex;"><p style="margin-bottom:27px;"><span id="toc" style="font-family:sans-serif;">{heading_part3}</span>{links3}
</p></div>

<p style="margin: 0px;background-color: #ffd42a;padding: 5px;width:33%;"></p>

<div style="display: flex;"><p style="margin-bottom:27px;"><span id="toc" style="font-family:sans-serif;">Lexicon</span>
<span id="toc"><a class="shadow" href="/lexicon.html">Lexicon</a></span>
</p></div>

<p style="margin: 0px;background-color: #ff7f2a;padding: 5px;width:25%;"></p>

<div style="display: flex;"><p style="margin-bottom:27px;"><span id="toc" style="font-family:sans-serif;">Preparatory materials for the Belarusian translation</span>
<span id="toc"><a class="shadow" href="/translatoraid/index.html">Gloss translations</a></span>
</p></div></article>{footer}</body></html>"""

templateIndexLink = """<span id="toc"><a class="shadow" href="/{}/{}.1.1.html">{}</a></span>"""