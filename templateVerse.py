templateVerse = """<!DOCTYPE html lang="{lang}">
<head>
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" type="image/png" href="/assets/img/favicon.png"/>

<title>{book} {chapter}:{verse} — {sitename}</title>
<meta name="description" content="{trtext}">

<link href='//fonts.googleapis.com/css?family=Lato:400,400italic&amp;subset=cyrillic,latin-ext' rel='stylesheet' type='text/css'>
<link href='//fonts.googleapis.com/css?family=EB+Garamond:400,400italic&amp;subset=cyrillic,latin-ext' rel='stylesheet' type='text/css'>

<link rel="stylesheet" type="text/css" href="/css/tufte.css">
<link rel="stylesheet" type="text/css" href="/css/print.css" media="print">
<script type="text/javascript" src="/assets/js/treelines.js"></script>

<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.8/jquery.min.js"></script>
<script type="text/javascript">
document.onkeydown = function(evt) {{
    evt = evt || window.event;
    switch (evt.keyCode) {{
        case 37:
            window.location = $('#prev').attr('href');
            break;
        case 39:
            window.location = $('#next').attr('href');
            break;
    }}
}};
</script>
</head>

<body>
<header>
<nav class="group"><a href="/{lang}/">
<h3>{sitename}</h3><h4>{sitesubname}</h4></a></nav>
</header>

<article class="group">
<p style="margin: 0px;background-color: #ffd42a;padding: 5px;width:33%;"></p>
<p style="margin: 0px;background-color: #ff7f2a;padding: 5px;width:38%;"></p>
<p style="margin: 0px;background-color: #7296cc;padding: 5px;width:27%;"></p>

<div style="display: flex;"><p style="font-size:100%"><span style="float: left;"><a class="shadow" href="/{lang}/{previous_book}.html">«</a>  {book} <a class="shadow" href="/{lang}/{next_book}.html">»</a></span>  <span style="float: right;"><a class="shadow" href="/{lang}/{previous_chapter}.html">«</a>  {chapter} <a class="shadow" href="/{lang}/{next_chapter}.html">»</a> : <a class="shadow" href="/{lang}/{previous_verse}.html">«</a>  {verse} <a class="shadow" href="/{lang}/{next_verse}.html">»</a>  </span></p></div>

<p id="bh" dir="rtl">{hebtext}</p>
<p><span class="marginnote" style="background:lightsteelblue;padding:0.8rem;"><!---<a href="https://biblehub.com/bsb/" target="_blank"><i>BSB</i></a> --->We are looking for the possibility to fetch an audio widget here.<br><em>Here would appear its copyright credit.</em><br><span style="color:lightsteelblue;">Debug: verse number {number}</span></span>{trtext_prepared}</p><p id="tr">/{words}/
<script>function playAudio(){{var e=document.getElementById("audio-player");e.currentTime={audio_start},e.play(),e.addEventListener("timeupdate",(function(){{e.currentTime>={audio_stop}&&(e.currentTime={audio_start},e.pause())}}))}}</script><audio id="audio-player" src="https://mechon-mamre.org/mp3/{mm_chapter}.mp3#t={audio_start},{audio_stop}"></audio><a style="color:white" onclick="playAudio()">▶</a></p>


<p style="text-align:center"><a class="shadow" id="prev" style="float:left;" href="/{lang}/{previous_verse}.html">« {backword}</a><a class="shadow" id="next" style="float:right;" href="/{lang}/{next_verse}.html">{forthword} »</a></p>

<h3 style="text-align:center;">{gloss_header}</h3><div class=wrapper><ol class=sentence>{glossTranslation}</ol></div><p style="text-align:center"><a class="shadow" style="float:left;" href="/{lang}/{previous_verse}.html">« {backword}</a><a class="shadow" style="float:right;" href="/{lang}/{next_verse}.html">{forthword} »</a></p>

<h3 style="text-align:center;">{syntax_header}</h3><div class=wrapper>{syntax}</div><p style="text-align:center"><a class="shadow" style="float:left;" href="/{lang}/{previous_verse}.html">« {backword}</a><a class="shadow" style="float:right;" href="/{lang}/{next_verse}.html">{forthword} »</a></p>

</div></article>{footer}</body><script>{drawlines}</script></html>"""

format_syntax = lambda syntax: "".join([ f"""<ul class='tree'><li><span> <span class="grt" id='{clause['curr']}'><div class='y'>{clause['ckind']}</div>{clause['ctype']}<br><strong style:'font-family:sans-serif;'>{clause['crela']}</strong></span> <ul>{ "".join([ f"<li><span> <span style='padding: 9px;font-size:80%;' id='{p['pnum']}'><strong style='font-family:sans-serif;'>{p['pfunction']}</strong><br>{p['ptyp']}</span> <ul><li><span style='font-family:sans-serif;font-weight:bold;' id='text{p['pnum']}'>{p['trans1']}</span></li></ul></span></li>".format(p) for p in clause["phrase"] ]) }</ul> </span></li></ul>""" for clause in syntax])

template_lines = """window.addEventListener('load', (event) => {{connect(getId("{from_}"), getId("{to}"), "black", 2 ); }})"""

templateRedirect = """<html><head><meta http-equiv="refresh" content="0; URL=/{}/{}.{}.{}.html"></head></html>"""
